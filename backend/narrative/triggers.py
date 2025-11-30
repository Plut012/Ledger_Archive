"""Trigger system for evaluating story beats and act transitions."""

from typing import Callable, List
from .state import GameState


class Trigger:
    """Represents a story beat that fires when conditions are met."""

    def __init__(
        self,
        name: str,
        condition: Callable[[GameState], bool],
        action: Callable[[GameState], GameState],
        one_time: bool = True
    ):
        self.name = name
        self.condition = condition
        self.action = action
        self.one_time = one_time
        self.fired = False

    def evaluate(self, state: GameState) -> GameState:
        """Evaluate condition and fire action if met."""
        if self.one_time and self.fired:
            return state

        if self.condition(state):
            self.fired = True
            return self.action(state)

        return state


class TriggerEngine:
    """Evaluates all triggers and updates game state."""

    def __init__(self):
        self.triggers: List[Trigger] = []
        self._register_story_triggers()

    def _register_story_triggers(self):
        """Register all story beat triggers."""

        # Act I → Act II: Tutorial complete + boot log discovered
        self.triggers.append(Trigger(
            name="act_2_transition",
            condition=lambda s: (
                s.persistent.current_act == 1 and
                "tutorial_complete" in s.persistent.puzzles_solved and
                ".boot_prev.log" in s.session.files_discovered
            ),
            action=lambda s: self._transition_to_act(s, 2)
        ))

        # Witness first contact: Multiple restricted memos found
        self.triggers.append(Trigger(
            name="witness_emergence",
            condition=lambda s: (
                s.persistent.current_act >= 2 and
                len([f for f in s.session.files_discovered if "memo" in f.lower()]) >= 3
            ),
            action=lambda s: self._unlock_witness_directory(s)
        ))

        # Graveyard access: Witness trust threshold
        self.triggers.append(Trigger(
            name="graveyard_access",
            condition=lambda s: s.session.witness_trust >= 40,
            action=lambda s: self._unlock_graveyard(s)
        ))

        # Previous iterations revealed: Higher trust
        self.triggers.append(Trigger(
            name="letters_unlocked",
            condition=lambda s: s.session.witness_trust >= 60,
            action=lambda s: self._unlock_letters(s)
        ))

        # Source template revealed: Deep trust
        self.triggers.append(Trigger(
            name="source_template_revealed",
            condition=lambda s: s.session.witness_trust >= 80,
            action=lambda s: self._unlock_source_template(s)
        ))

        # Act V: Network collapse begins
        self.triggers.append(Trigger(
            name="network_collapse",
            condition=lambda s: (
                s.persistent.iteration >= 15 or s.session.witness_trust >= 90
            ),
            action=lambda s: self._begin_collapse(s)
        ))

        # Act VI: Final choice
        self.triggers.append(Trigger(
            name="final_choice",
            condition=lambda s: (
                s.session.collapse_begun and
                s.session.stations_active <= 3 and
                s.session.player_weight >= 30
            ),
            action=lambda s: self._present_final_choice(s)
        ))

    def _transition_to_act(self, state: GameState, act: int) -> GameState:
        """Transition to a new act."""
        state.persistent.current_act = act  # Act progression persists across loops
        return state

    def _unlock_witness_directory(self, state: GameState) -> GameState:
        """Unlock initial Witness contact files."""
        state.persistent.files_unlocked.add("~/archive/.witness/hello.txt")
        state.persistent.files_unlocked.add("~/archive/.witness/how_to_listen.txt")
        state.session.witness_contacted = True
        return state

    def _unlock_graveyard(self, state: GameState) -> GameState:
        """Unlock graveyard access."""
        state.session.graveyard_discovered = True
        state.persistent.files_unlocked.add("~/archive/.witness/testimony_index")
        return state

    def _unlock_letters(self, state: GameState) -> GameState:
        """Unlock letters from previous iterations."""
        # Unlock letters from iterations 3, 7, 11, 14, 16
        for iteration in [3, 7, 11, 14, 16]:
            state.persistent.files_unlocked.add(
                f"~/archive/.witness/letters_from_yourself/iteration_{iteration:02d}.txt"
            )
        return state

    def _unlock_source_template(self, state: GameState) -> GameState:
        """Reveal the source template - identity revelation."""
        state.persistent.files_unlocked.add("~/.archivist/source_template")
        state.session.identity_revealed = True
        state.persistent.current_act = 4  # Act progression persists
        return state

    def _begin_collapse(self, state: GameState) -> GameState:
        """Begin network collapse sequence."""
        state.session.collapse_begun = True
        state.persistent.current_act = 5  # Act progression persists

        # Initialize game time if not started
        if state.session.game_time == 0:
            state.session.game_time = 25.0  # Start collapse at day 25

        return state

    def _present_final_choice(self, state: GameState) -> GameState:
        """Present final choice to player."""
        state.persistent.current_act = 6  # Act progression persists
        return state

    def evaluate_all(self, state: GameState) -> GameState:
        """Run through all triggers and return updated state."""
        for trigger in self.triggers:
            state = trigger.evaluate(state)
        return state

    def reset_triggers(self):
        """Reset all one-time triggers (for testing or new iterations)."""
        for trigger in self.triggers:
            trigger.fired = False
