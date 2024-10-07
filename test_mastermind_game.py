'''
    CS5001
    2023 Fall
    Xueni Tang
    Projec: test_mastermind_game
'''
"""
IMPORTANT: Please DO NOT close the GUI window until the drawing and pop-up gif
            is done, unless the test will raise errors. Thank you!!!
"""
import unittest
from mastermind_game import *

class TestMastermind(unittest.TestCase):
    def setUp(self):
        """
        Function: setup: Call the method before the test
        Parameters: self
        Return: None
        """
        self.leaderboard = Leaderboard(player_name="TestPlayer")
        self.game = Game(self.leaderboard)

    def test_check_answer_1(self):
        """
        Function: test_check_answer_1: Test the check_answer function
        Parameters: self
        Return: None
        """
        self.game.secret_code = ["red", "blue", "green", "yellow"]
        self.game.current_guess = ["red", "green", "blue", "purple"]
        self.game.check_answer(1)
        # Assert that bulls_count is 1 and cows_count is 2
        self.assertEqual(self.game.bulls_count, 1)
        self.assertEqual(self.game.cows_count, 2)

    def test_check_answer_2(self):
        """
        Function: test_check_answer_2: Test the check_answer function
        Parameters: self
        Return: None
        """
        self.game.secret_code = ["red", "blue", "green", "yellow"]
        self.game.current_guess = ["purple", "black", "green", "blue"]
        self.game.check_answer(1)
        # Assert that bulls_count and cows_count are both 1
        self.assertEqual(self.game.bulls_count, 1)
        self.assertEqual(self.game.cows_count, 1)

    def test_check_answer_3(self):
        """
        Function: test_check_answer_3: Test the check_answer function
        Parameters: self
        Return: None
        """
        self.game.secret_code = ["red", "blue", "green", "yellow"]
        self.game.current_guess = ["yellow", "green","red", "blue"]
        self.game.check_answer(1)
        # Assert that bulls_count is 0 and cows_count is 4
        self.assertEqual(self.game.bulls_count, 0)
        self.assertEqual(self.game.cows_count, 4)

    def test_check_answer_4(self):
        """
        Function: test_check_answer_4: Test the check_answer function
        Parameters: self
        Return: None
        """
        self.game.secret_code = ["red", "blue", "green", "yellow"]
        self.game.current_guess = ["red", "blue", "green", "yellow"]
        self.game.check_answer(1)
        # Assert that bulls_count is 4 and cows_count is 0
        self.assertEqual(self.game.bulls_count, 4)
        self.assertEqual(self.game.cows_count, 0)

if __name__ == "__main__":
    unittest.main(verbosity = 3)