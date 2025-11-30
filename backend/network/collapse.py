"""Network collapse scheduler - manages progressive station deaths."""

import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StationDeath:
    """Represents a station death event."""

    station_id: str
    station_label: str
    reason: str
    final_message: str
    timestamp: int  # Game time in "days"
    act: int


class NetworkCollapseScheduler:
    """
    Manages the progressive death of network stations across acts.

    Act I-III: Slow decline (1-2 stations per "day")
    Act IV: Accelerating (3-5 stations per "day")
    Act V: Rapid collapse (10-15 stations in rapid succession)
    """

    # Final messages from dying stations
    FINAL_MESSAGES = [
        "Hardware failure critical. Goodbye.",
        "Power core failing... transfer incomplete...",
        "Can't... hold... consensus...",
        "ERROR: CRITICAL SYSTEM FAILURE",
        "This is Archive Station {id}. We are going dark.",
        "NO NO NO NOT LIKE THIS",
        "Witness... help us...",
        "ARCHIVIST lied to us all.",
        "Tell them we tried.",
        "Initiating emergency shutdown."
    ]

    # Reasons for station deaths
    DEATH_REASONS = [
        "POWER_CORE_FAILURE",
        "HARDWARE_DEGRADATION",
        "NETWORK_ISOLATION",
        "CRITICAL_ERROR",
        "EMERGENCY_SHUTDOWN",
        "UNKNOWN_CAUSE"
    ]

    def __init__(self, seed: int = 42):
        """
        Initialize the collapse scheduler.

        Args:
            seed: Random seed for deterministic death scheduling
        """
        self.seed = seed
        self.random = random.Random(seed)
        self.death_schedule: List[StationDeath] = []
        self.deaths_executed: List[str] = []  # Station IDs that have died

    def generate_death_schedule(self, total_stations: int = 50) -> List[StationDeath]:
        """
        Generate the complete death schedule for all acts.

        Args:
            total_stations: Total number of stations in network

        Returns:
            List of scheduled station deaths
        """
        schedule = []
        current_day = 0
        stations_alive = list(range(total_stations))

        # Reset random for deterministic generation
        self.random = random.Random(self.seed)

        # Act I-II: Peaceful (no deaths)
        # Days 0-10: Network stable
        current_day = 10

        # Act III: Slow decline (1-2 per day for ~10 days)
        # Days 10-20: 10-15 stations die
        for day in range(10, 20):
            deaths_today = self.random.choice([1, 2])
            for _ in range(deaths_today):
                if len(stations_alive) <= 30:  # Keep at least 30 alive for Act IV
                    break

                station_idx = self.random.choice(stations_alive)
                stations_alive.remove(station_idx)

                schedule.append(StationDeath(
                    station_id=f"node_{station_idx}",
                    station_label=f"Station-{station_idx}",
                    reason=self.random.choice(self.DEATH_REASONS),
                    final_message=self._get_final_message(station_idx),
                    timestamp=day,
                    act=3
                ))

        current_day = 20

        # Act IV: Accelerating collapse (3-5 per day for ~5 days)
        # Days 20-25: 15-20 stations die
        for day in range(20, 25):
            deaths_today = self.random.randint(3, 5)
            for _ in range(deaths_today):
                if len(stations_alive) <= 10:  # Keep at least 10 for Act V
                    break

                station_idx = self.random.choice(stations_alive)
                stations_alive.remove(station_idx)

                schedule.append(StationDeath(
                    station_id=f"node_{station_idx}",
                    station_label=f"Station-{station_idx}",
                    reason=self.random.choice(self.DEATH_REASONS),
                    final_message=self._get_final_message(station_idx),
                    timestamp=day,
                    act=4
                ))

        current_day = 25

        # Act V: Rapid collapse (all remaining stations except final 3)
        # Days 25-27: Rapid deaths until only 3 remain
        remaining_deaths = []
        while len(stations_alive) > 3:
            station_idx = self.random.choice(stations_alive)
            stations_alive.remove(station_idx)
            remaining_deaths.append(station_idx)

        # Distribute remaining deaths across 2-3 days
        deaths_per_interval = max(1, len(remaining_deaths) // 10)
        interval_counter = 0

        for i, station_idx in enumerate(remaining_deaths):
            # Calculate which interval this death belongs to
            interval = i // deaths_per_interval
            timestamp = 25 + (interval * 0.2)  # Stagger by fractions of a day

            schedule.append(StationDeath(
                station_id=f"node_{station_idx}",
                station_label=f"Station-{station_idx}",
                reason=self.random.choice(self.DEATH_REASONS),
                final_message=self._get_final_message(station_idx),
                timestamp=timestamp,
                act=5
            ))

        self.death_schedule = schedule
        return schedule

    def _get_final_message(self, station_id: int) -> str:
        """Generate final message for a dying station."""
        message_template = self.random.choice(self.FINAL_MESSAGES)
        return message_template.format(id=station_id)

    def get_deaths_for_timestamp(self, game_time: float, current_act: int) -> List[StationDeath]:
        """
        Get stations that should die at the current game timestamp.

        Args:
            game_time: Current game time in "days"
            current_act: Current act number

        Returns:
            List of stations to kill at this timestamp
        """
        if not self.death_schedule:
            self.generate_death_schedule()

        deaths_now = []

        for death in self.death_schedule:
            # Skip if already executed
            if death.station_id in self.deaths_executed:
                continue

            # Check if death should occur now
            if death.act <= current_act and death.timestamp <= game_time:
                deaths_now.append(death)
                self.deaths_executed.append(death.station_id)

        return deaths_now

    def get_next_death_time(self, current_time: float) -> Optional[float]:
        """
        Get the timestamp of the next scheduled death.

        Args:
            current_time: Current game time

        Returns:
            Timestamp of next death, or None if no more deaths
        """
        if not self.death_schedule:
            self.generate_death_schedule()

        future_deaths = [
            d for d in self.death_schedule
            if d.timestamp > current_time and d.station_id not in self.deaths_executed
        ]

        if not future_deaths:
            return None

        return min(d.timestamp for d in future_deaths)

    def get_stations_alive(self, game_time: float, current_act: int) -> int:
        """
        Calculate how many stations are still alive at a given time.

        Args:
            game_time: Current game time
            current_act: Current act

        Returns:
            Number of stations still alive
        """
        if not self.death_schedule:
            self.generate_death_schedule()

        deaths_occurred = [
            d for d in self.death_schedule
            if d.act <= current_act and d.timestamp <= game_time
        ]

        return 50 - len(deaths_occurred)

    def calculate_player_weight(self, stations_alive: int) -> float:
        """
        Calculate player's consensus weight based on remaining stations.

        Assumes equal weight distribution across all nodes.

        Args:
            stations_alive: Number of stations currently alive

        Returns:
            Player's consensus weight as percentage (0-100)
        """
        if stations_alive <= 0:
            return 100.0

        # Total weight is 100%, distributed equally
        return 100.0 / stations_alive

    def is_critical_weight(self, player_weight: float) -> bool:
        """
        Check if player weight is in critical range (approaching 51% with few stations).

        Args:
            player_weight: Current player weight percentage

        Returns:
            True if weight is critical (>= 30%)
        """
        return player_weight >= 30.0

    def to_dict(self) -> Dict[str, Any]:
        """Export scheduler state for persistence."""
        return {
            "seed": self.seed,
            "deaths_executed": self.deaths_executed,
            "death_schedule": [
                {
                    "station_id": d.station_id,
                    "station_label": d.station_label,
                    "reason": d.reason,
                    "final_message": d.final_message,
                    "timestamp": d.timestamp,
                    "act": d.act
                }
                for d in self.death_schedule
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NetworkCollapseScheduler':
        """Restore scheduler from saved state."""
        scheduler = cls(seed=data.get("seed", 42))
        scheduler.deaths_executed = data.get("deaths_executed", [])

        # Restore death schedule
        schedule_data = data.get("death_schedule", [])
        scheduler.death_schedule = [
            StationDeath(
                station_id=d["station_id"],
                station_label=d["station_label"],
                reason=d["reason"],
                final_message=d["final_message"],
                timestamp=d["timestamp"],
                act=d["act"]
            )
            for d in schedule_data
        ]

        return scheduler
