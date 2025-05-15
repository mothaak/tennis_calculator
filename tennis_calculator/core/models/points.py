"""handles tennis point tracking"""

from dataclasses import dataclass


@dataclass
class PlayerPoints:
    """represents points for two players"""

    player_one: int = 0
    player_two: int = 0

    def __getstate__(self):
        """Return state for pickling."""
        return {
            'player_one': self.player_one,
            'player_two': self.player_two
        }

    def __setstate__(self, state):
        """Set state when unpickling."""
        self.player_one = state['player_one']
        self.player_two = state['player_two']

    def add_point(self, is_player_one: bool) -> None:
        """adds point for specified player"""
        if is_player_one:
            self.player_one += 1
        else:
            self.player_two += 1

    def reset(self) -> None:
        """resets points to zero"""
        self.player_one = 0
        self.player_two = 0
