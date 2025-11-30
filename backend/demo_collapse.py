#!/usr/bin/env python
"""Demo script for network collapse system."""

from network.collapse import NetworkCollapseScheduler
from narrative.state import GameState, PersistentState, SessionState

def main():
    print("=" * 60)
    print("NETWORK COLLAPSE SYSTEM DEMO")
    print("=" * 60)
    print()

    # Initialize scheduler
    scheduler = NetworkCollapseScheduler(seed=42)
    print("✓ Network Collapse Scheduler initialized (seed=42)")
    print()

    # Generate schedule
    schedule = scheduler.generate_death_schedule(total_stations=50)
    print(f"✓ Death schedule generated: {len(schedule)} stations scheduled to die")
    print()

    # Show schedule summary
    print("SCHEDULE SUMMARY:")
    print("-" * 60)

    acts = {}
    for death in schedule:
        if death.act not in acts:
            acts[death.act] = []
        acts[death.act].append(death)

    for act in sorted(acts.keys()):
        deaths = acts[act]
        print(f"  Act {act}: {len(deaths)} deaths")
        print(f"    Time range: {min(d.timestamp for d in deaths):.1f} - {max(d.timestamp for d in deaths):.1f} days")

    print()

    # Show some example deaths
    print("EXAMPLE STATION DEATHS:")
    print("-" * 60)

    for i, death in enumerate(schedule[:5]):
        print(f"  {i+1}. {death.station_label} (Act {death.act}, Day {death.timestamp})")
        print(f"     Reason: {death.reason}")
        print(f"     Final Message: \"{death.final_message}\"")
        print()

    # Simulate game progression
    print("SIMULATING GAME PROGRESSION:")
    print("-" * 60)

    # Initialize game state
    game_state = GameState(
        persistent=PersistentState(current_act=3, current_iteration=17),
        session=SessionState(game_time=10.0)
    )

    print(f"  Initial State:")
    print(f"    Game Time: Day {game_state.session.game_time}")
    print(f"    Current Act: {game_state.persistent.current_act}")
    print(f"    Stations Active: {game_state.session.stations_active}")
    print(f"    Player Weight: {game_state.session.player_weight}%")
    print()

    # Advance time and check for deaths
    time_steps = [15.0, 20.0, 22.0, 25.0, 26.0, 27.0]

    for time in time_steps:
        game_state.session.game_time = time

        # Get deaths at this time
        deaths = scheduler.get_deaths_for_timestamp(
            game_state.session.game_time,
            game_state.persistent.current_act
        )

        if deaths:
            print(f"  Day {time}: {len(deaths)} station(s) died!")
            for death in deaths[:3]:  # Show first 3
                print(f"    - {death.station_label}: \"{death.final_message}\"")
            if len(deaths) > 3:
                print(f"    ... and {len(deaths) - 3} more")

        # Update state
        game_state.session.stations_active = scheduler.get_stations_alive(
            game_state.session.game_time,
            game_state.persistent.current_act
        )
        game_state.session.player_weight = scheduler.calculate_player_weight(
            game_state.session.stations_active
        )

        print(f"    Stations Active: {game_state.session.stations_active}/50")
        print(f"    Player Weight: {game_state.session.player_weight:.1f}%")

        if scheduler.is_critical_weight(game_state.session.player_weight):
            print(f"    ⚠ WARNING: CRITICAL CONSENSUS WEIGHT!")

        print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
