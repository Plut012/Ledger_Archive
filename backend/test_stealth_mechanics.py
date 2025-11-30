"""Unit tests for stealth mechanics system."""

import pytest
import time
from stealth.monitor import StealthMonitor, MonitoringResult


class TestStealthMonitor:
    """Test suite for StealthMonitor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.monitor = StealthMonitor()
        self.base_state = {
            "session": {
                "current_act": 1,
                "archivist_suspicion": 0,
                "log_mask_active": False,
                "log_mask_expires": 0
            },
            "persistent": {
                "iteration": 1
            }
        }

    def test_monitor_initialization(self):
        """Test StealthMonitor initializes correctly."""
        assert self.monitor.archivist_busy_until == 0
        assert self.monitor.validation_active == False
        assert len(self.monitor.MONITORED_KEYWORDS) == 7
        assert "reconstruct" in self.monitor.MONITORED_KEYWORDS
        assert "witness" in self.monitor.MONITORED_KEYWORDS

    def test_no_detection_for_safe_commands(self):
        """Test that safe commands don't trigger monitoring."""
        safe_commands = [
            "ls -a",
            "cd ~/archive",
            "cat README.md",
            "pwd",
            "help"
        ]

        for cmd in safe_commands:
            result = self.monitor.check_command(cmd, self.base_state)
            assert result.detected == False
            assert result.suspicion_increase == 0
            assert result.reason == "NO_KEYWORDS"

    def test_detection_for_monitored_keywords(self):
        """Test that monitored keywords trigger detection in Act I."""
        monitored_commands = [
            "reconstruct 74221",
            "contact witness",
            "view testimony",
            "upload data"
        ]

        for cmd in monitored_commands:
            result = self.monitor.check_command(cmd, self.base_state)
            # Act I has 10% detection chance, so it may or may not detect
            # But the result should have non-zero detection chance
            assert result.detection_chance > 0

    def test_log_mask_prevents_detection(self):
        """Test that active log mask prevents all detection."""
        state = self.base_state.copy()
        state["session"] = {
            **state["session"],
            "log_mask_active": True,
            "log_mask_expires": int(time.time()) + 30
        }

        result = self.monitor.check_command("reconstruct 74221", state)
        assert result.detected == False
        assert result.suspicion_increase == 0
        assert result.reason == "LOG_MASK_ACTIVE"

    def test_expired_log_mask_allows_detection(self):
        """Test that expired log mask doesn't prevent detection."""
        state = self.base_state.copy()
        state["session"] = {
            **state["session"],
            "log_mask_active": True,
            "log_mask_expires": int(time.time()) - 10  # Expired 10 seconds ago
        }

        result = self.monitor.check_command("reconstruct 74221", state)
        # Log mask is expired, so detection should be possible
        assert result.reason != "LOG_MASK_ACTIVE"

    def test_act_based_detection_escalation(self):
        """Test that detection chance increases by act."""
        command = "reconstruct 74221"

        # Act I: 10% detection
        state_act1 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 1}}
        result1 = self.monitor.check_command(command, state_act1)
        assert result1.detection_chance == 0.1

        # Act III: 50% detection
        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}
        result3 = self.monitor.check_command(command, state_act3)
        assert result3.detection_chance == 0.5

        # Act IV: 85% detection
        state_act4 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 4}}
        result4 = self.monitor.check_command(command, state_act4)
        assert result4.detection_chance == 0.85

        # Act V: 100% detection
        state_act5 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 5}}
        result5 = self.monitor.check_command(command, state_act5)
        assert result5.detection_chance == 1.0

    def test_archivist_distraction_reduces_detection(self):
        """Test that ARCHIVIST being busy reduces detection chance."""
        # Set ARCHIVIST as busy for 10 seconds
        self.monitor.set_archivist_busy(10)

        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}
        result = self.monitor.check_command("reconstruct 74221", state_act3)

        # Act III base is 50%, with distraction should be 15% (50% * 0.3)
        assert result.detection_chance == pytest.approx(0.15, rel=0.01)

    def test_validation_window_reduces_detection(self):
        """Test that active validation reduces detection chance."""
        # Set validation as active
        self.monitor.set_validation_active(True)

        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}
        result = self.monitor.check_command("reconstruct 74221", state_act3)

        # Act III base is 50%, with validation should be 15% (50% * 0.3)
        assert result.detection_chance == pytest.approx(0.15, rel=0.01)

        # Turn off validation
        self.monitor.set_validation_active(False)
        result2 = self.monitor.check_command("reconstruct 74221", state_act3)
        assert result2.detection_chance == 0.5

    def test_aliased_command_reduces_detection(self):
        """Test that aliased commands reduce detection chance."""
        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}

        # Direct command
        result_direct = self.monitor.check_command("reconstruct 74221", state_act3)

        # Aliased command
        result_alias = self.monitor.check_command("chain.parse --deep --memo --block=74221", state_act3)

        # Alias should have lower detection (50% * 0.5 = 25%)
        assert result_alias.detection_chance < result_direct.detection_chance

    def test_combined_evasion_methods(self):
        """Test that combining evasion methods stacks reductions."""
        state_act4 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 4}}

        # Set ARCHIVIST busy and validation active
        self.monitor.set_archivist_busy(10)
        self.monitor.set_validation_active(True)

        # Use command with monitored keyword (chain.parse has no keywords itself)
        # So we test with a command that has keywords but uses evasion
        result = self.monitor.check_command("reconstruct 74221", state_act4)

        # Act IV base: 85%
        # With distraction: 85% * 0.3 = 25.5%
        # With validation: 25.5% * 0.3 = 7.65%
        expected = 0.85 * 0.3 * 0.3
        assert result.detection_chance == pytest.approx(expected, rel=0.01)

    def test_evasion_suggestion(self):
        """Test that evasion suggestions work correctly."""
        # Test reconstruct -> chain.parse
        suggestion = self.monitor.get_evasion_suggestion("reconstruct 74221")
        assert suggestion == "chain.parse --deep --memo --block=74221"

        # Test witness -> network.peer
        suggestion2 = self.monitor.get_evasion_suggestion("witness status")
        assert suggestion2 == "network.peer"

        # Test non-aliased command
        suggestion3 = self.monitor.get_evasion_suggestion("ls -a")
        assert suggestion3 is None

    def test_monitoring_status(self):
        """Test that monitoring status is correctly reported."""
        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}

        status = self.monitor.get_monitoring_status(state_act3)

        assert status["baseDetectionChance"] == 0.5
        assert status["effectiveDetectionChance"] == 0.5
        assert status["logMaskActive"] == False
        assert status["archivistDistracted"] == False
        assert status["validationActive"] == False
        assert "ELEVATED" in status["monitoringLevel"]
        assert "log_masking" in status["availableEvasionMethods"]

    def test_monitoring_level_descriptions(self):
        """Test monitoring level descriptions for each act."""
        descriptions = {
            1: "MINIMAL",
            2: "MINIMAL",
            3: "ELEVATED",
            4: "HIGH",
            5: "MAXIMUM"
        }

        for act, expected_keyword in descriptions.items():
            desc = self.monitor._get_monitoring_level_description(act)
            assert expected_keyword in desc

    def test_available_evasion_methods_by_act(self):
        """Test that available evasion methods change by act."""
        # Act I
        methods_act1 = self.monitor._get_available_evasion_methods(1)
        assert "log_masking" in methods_act1
        assert "command_aliases" in methods_act1

        # Act III
        methods_act3 = self.monitor._get_available_evasion_methods(3)
        assert "log_masking" in methods_act3
        assert "command_aliases" in methods_act3
        assert "validation_window" in methods_act3

        # Act IV - aliases less effective
        methods_act4 = self.monitor._get_available_evasion_methods(4)
        assert "log_masking" in methods_act4
        assert "command_aliases" not in methods_act4
        assert "combined_techniques" in methods_act4

    def test_suspicion_increase_by_act(self):
        """Test that suspicion increases more in later acts."""
        command = "reconstruct 74221"

        # Manually set detection to True for testing
        # We'll check the base suspicion per keyword

        assert self.monitor._get_suspicion_per_keyword(1) == 3
        assert self.monitor._get_suspicion_per_keyword(3) == 8
        assert self.monitor._get_suspicion_per_keyword(4) == 15
        assert self.monitor._get_suspicion_per_keyword(5) == 20

    def test_act_multiplier(self):
        """Test act-based multiplier for suspicion."""
        assert self.monitor._get_act_multiplier(1) == 0.5
        assert self.monitor._get_act_multiplier(2) == 0.5
        assert self.monitor._get_act_multiplier(3) == 1.0
        assert self.monitor._get_act_multiplier(4) == 1.5
        assert self.monitor._get_act_multiplier(5) == 2.0

    def test_keyword_detection(self):
        """Test that all monitored keywords are detected."""
        for keyword in self.monitor.MONITORED_KEYWORDS:
            result = self.monitor.check_command(f"test {keyword} command", self.base_state)
            assert result.detection_chance > 0

    def test_suspicious_terms_detection(self):
        """Test that suspicious terms are detected with lower weight."""
        result = self.monitor.check_command("check previous execution", self.base_state)
        # Should detect "previous" and "execution" as suspicious terms
        assert result.detection_chance > 0

    def test_no_false_positives(self):
        """Test that partial matches don't trigger false positives."""
        # "test" contains "test", not "testimony"
        result = self.monitor.check_command("test command", self.base_state)
        assert result.reason == "NO_KEYWORDS"

    def test_case_insensitive_detection(self):
        """Test that keyword detection is case insensitive."""
        commands = [
            "RECONSTRUCT 74221",
            "Reconstruct 74221",
            "reconstruct 74221"
        ]

        for cmd in commands:
            result = self.monitor.check_command(cmd, self.base_state)
            assert result.detection_chance > 0

    def test_archivist_busy_expiration(self):
        """Test that ARCHIVIST busy state expires correctly."""
        # Set busy for 1 second
        self.monitor.set_archivist_busy(1)

        state_act3 = {**self.base_state, "session": {**self.base_state["session"], "current_act": 3}}

        # Should be distracted now
        result1 = self.monitor.check_command("reconstruct 74221", state_act3)
        assert result1.detection_chance < 0.5  # Reduced from base 50%

        # Wait for expiration
        time.sleep(1.1)

        # Should not be distracted anymore
        result2 = self.monitor.check_command("reconstruct 74221", state_act3)
        assert result2.detection_chance == 0.5  # Back to base

    def test_multiple_keywords_increase_suspicion(self):
        """Test that multiple keywords in one command increase suspicion more."""
        # This would require deterministic detection, so we test the base mechanics
        keywords_found = self.monitor._find_keywords("reconstruct witness testimony")
        assert len(keywords_found) == 3
        assert "reconstruct" in keywords_found
        assert "witness" in keywords_found
        assert "testimony" in keywords_found


class TestMonitoringResult:
    """Test MonitoringResult dataclass."""

    def test_monitoring_result_creation(self):
        """Test MonitoringResult can be created with all fields."""
        result = MonitoringResult(
            detected=True,
            suspicion_increase=15,
            detection_chance=0.85,
            reason="KEYWORDS:reconstruct"
        )

        assert result.detected == True
        assert result.suspicion_increase == 15
        assert result.detection_chance == 0.85
        assert result.reason == "KEYWORDS:reconstruct"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
