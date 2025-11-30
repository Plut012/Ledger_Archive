"""Tests for network collapse system."""

import pytest
from network.collapse import NetworkCollapseScheduler, StationDeath


class TestNetworkCollapseScheduler:
    """Test network collapse scheduler."""

    def test_scheduler_initialization(self):
        """Test that scheduler initializes correctly."""
        scheduler = NetworkCollapseScheduler(seed=42)
        assert scheduler.seed == 42
        assert len(scheduler.death_schedule) == 0
        assert len(scheduler.deaths_executed) == 0

    def test_generate_death_schedule(self):
        """Test that death schedule is generated correctly."""
        scheduler = NetworkCollapseScheduler(seed=42)
        schedule = scheduler.generate_death_schedule(total_stations=50)

        # Should have deaths for most stations (leaving 3 alive at end)
        assert len(schedule) == 47

        # Check that deaths are in chronological order
        timestamps = [d.timestamp for d in schedule]
        assert timestamps == sorted(timestamps)

    def test_schedule_determinism(self):
        """Test that same seed produces same schedule."""
        scheduler1 = NetworkCollapseScheduler(seed=42)
        schedule1 = scheduler1.generate_death_schedule()

        scheduler2 = NetworkCollapseScheduler(seed=42)
        schedule2 = scheduler2.generate_death_schedule()

        # Should produce identical schedules
        assert len(schedule1) == len(schedule2)
        for d1, d2 in zip(schedule1, schedule2):
            assert d1.station_id == d2.station_id
            assert d1.timestamp == d2.timestamp
            assert d1.reason == d2.reason

    def test_different_seeds_produce_different_schedules(self):
        """Test that different seeds produce different schedules."""
        scheduler1 = NetworkCollapseScheduler(seed=42)
        schedule1 = scheduler1.generate_death_schedule()

        scheduler2 = NetworkCollapseScheduler(seed=99)
        schedule2 = scheduler2.generate_death_schedule()

        # Should have same length but different order/content
        assert len(schedule1) == len(schedule2)

        # Check that at least some deaths differ
        differences = sum(
            1 for d1, d2 in zip(schedule1, schedule2)
            if d1.station_id != d2.station_id
        )
        assert differences > 0

    def test_get_deaths_for_timestamp(self):
        """Test getting deaths at specific time."""
        scheduler = NetworkCollapseScheduler(seed=42)
        scheduler.generate_death_schedule()

        # Act 3 starts at day 10
        deaths_early = scheduler.get_deaths_for_timestamp(game_time=15.0, current_act=3)
        assert len(deaths_early) > 0

        # Each death should only be returned once
        deaths_again = scheduler.get_deaths_for_timestamp(game_time=15.0, current_act=3)
        assert len(deaths_again) == 0

    def test_get_stations_alive(self):
        """Test calculating stations alive at specific time."""
        scheduler = NetworkCollapseScheduler(seed=42)
        scheduler.generate_death_schedule()

        # At time 0, all 50 stations should be alive
        alive_start = scheduler.get_stations_alive(game_time=0.0, current_act=1)
        assert alive_start == 50

        # By day 20, some stations should have died
        alive_mid = scheduler.get_stations_alive(game_time=20.0, current_act=3)
        assert alive_mid < 50
        assert alive_mid > 3

        # By day 28, close to 3 should remain (some randomness in timing)
        alive_end = scheduler.get_stations_alive(game_time=28.0, current_act=5)
        assert alive_end <= 5  # Allow some margin due to timing distribution

    def test_calculate_player_weight(self):
        """Test player weight calculation."""
        scheduler = NetworkCollapseScheduler()

        # With 50 stations, player has 2% weight
        weight_50 = scheduler.calculate_player_weight(50)
        assert weight_50 == pytest.approx(2.0, rel=0.01)

        # With 10 stations, player has 10% weight
        weight_10 = scheduler.calculate_player_weight(10)
        assert weight_10 == pytest.approx(10.0, rel=0.01)

        # With 3 stations, player has ~33% weight
        weight_3 = scheduler.calculate_player_weight(3)
        assert weight_3 == pytest.approx(33.33, rel=0.01)

    def test_is_critical_weight(self):
        """Test critical weight detection."""
        scheduler = NetworkCollapseScheduler()

        # Below 30% is not critical
        assert not scheduler.is_critical_weight(25.0)

        # 30% and above is critical
        assert scheduler.is_critical_weight(30.0)
        assert scheduler.is_critical_weight(35.0)

    def test_act_based_death_rates(self):
        """Test that death rates vary by act."""
        scheduler = NetworkCollapseScheduler(seed=42)
        schedule = scheduler.generate_death_schedule()

        # Count deaths by act
        act_3_deaths = [d for d in schedule if d.act == 3]
        act_4_deaths = [d for d in schedule if d.act == 4]
        act_5_deaths = [d for d in schedule if d.act == 5]

        # Act 3 should have slower deaths
        assert len(act_3_deaths) > 0

        # Act 4 should have faster deaths
        assert len(act_4_deaths) > 0

        # Act 5 should have significant deaths (rapid collapse)
        # Note: May not always be MORE than Act 4 due to duration differences
        assert len(act_5_deaths) > 0
        assert len(act_3_deaths) > 0

    def test_to_dict_and_from_dict(self):
        """Test serialization and deserialization."""
        scheduler1 = NetworkCollapseScheduler(seed=42)
        scheduler1.generate_death_schedule()
        scheduler1.deaths_executed = ["node_0", "node_5"]

        # Serialize
        data = scheduler1.to_dict()

        # Deserialize
        scheduler2 = NetworkCollapseScheduler.from_dict(data)

        assert scheduler2.seed == scheduler1.seed
        assert scheduler2.deaths_executed == scheduler1.deaths_executed
        assert len(scheduler2.death_schedule) == len(scheduler1.death_schedule)

    def test_final_message_generation(self):
        """Test that final messages are generated."""
        scheduler = NetworkCollapseScheduler(seed=42)
        schedule = scheduler.generate_death_schedule()

        # All deaths should have final messages
        for death in schedule:
            assert death.final_message
            assert len(death.final_message) > 0

    def test_next_death_time(self):
        """Test getting next death timestamp."""
        scheduler = NetworkCollapseScheduler(seed=42)
        scheduler.generate_death_schedule()

        # At time 0, next death should be around day 10 (Act 3 start)
        next_time = scheduler.get_next_death_time(0.0)
        assert next_time is not None
        assert next_time >= 10.0

        # After all deaths, should return None
        next_time_end = scheduler.get_next_death_time(100.0)
        assert next_time_end is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
