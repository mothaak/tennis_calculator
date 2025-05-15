"""verifies player points functionality"""

from tennis_calculator.core.models.points import PlayerPoints


class TestPlayerPoints:
    """validates player points behavior"""

    def test_initial_state(self):
        """verifies initial points state"""
        points = PlayerPoints()
        assert points.player_one == 0
        assert points.player_two == 0

    def test_add_point_player_one(self):
        """verifies point addition for player one"""
        points = PlayerPoints()
        points.add_point(True)
        assert points.player_one == 1
        assert points.player_two == 0

    def test_add_point_player_two(self):
        """verifies point addition for player two"""
        points = PlayerPoints()
        points.add_point(False)
        assert points.player_one == 0
        assert points.player_two == 1

    def test_reset(self):
        """verifies points reset functionality"""
        points = PlayerPoints()
        points.add_point(True)
        points.add_point(False)
        points.reset()
        assert points.player_one == 0
        assert points.player_two == 0
