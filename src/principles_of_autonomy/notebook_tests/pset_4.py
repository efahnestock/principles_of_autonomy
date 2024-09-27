import unittest
import numpy as np
import timeout_decorator
from gradescope_utils.autograder_utils.decorators import weight
from mdp_utils import MDP, build_mdp

from principles_of_autonomy.grader import get_locals


class TestPSet4(unittest.TestCase):
    def __init__(self, test_name, notebook_locals):
        super().__init__(test_name)
        self.notebook_locals = notebook_locals

    @weight(55)
    @timeout_decorator.timeout(5.0)
    def test_1_convergence(f_converge):
        # Test case 1: Exact match
        V1 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        V2 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        epsilon = 1e-5
        assert f_converge(V1, V2, epsilon) == True, "Function fails when tested on an exact match (V1 and V2 are identical)."

        # Test case 2: Small differences within epsilon
        V1 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        V2 = {'s1': 1.000001, 's2': 2.000001, 's3': 3.000001}
        epsilon = 1e-3
        assert f_converge(V1, V2, epsilon) == True, "Small differences within epsilon aren't passing."

        # Test case 3: Differences larger than epsilon
        V1 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        V2 = {'s1': 1.1, 's2': 2.2, 's3': 3.3}
        epsilon = 1e-2
        assert f_converge(V1, V2, epsilon) == False, "Differences larger than epsilon aren't failing."

        # Test case 4: Zero epsilon
        V1 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        V2 = {'s1': 1.000001, 's2': 2.000001, 's3': 3.000001}
        epsilon = 0
        assert f_converge(V1, V2, epsilon) == False, "The function can't handle epsilon=0 properly."

        # Test case 5: One state difference
        V1 = {'s1': 1.0, 's2': 2.0, 's3': 3.0}
        V2 = {'s1': 1.0, 's2': 2.5, 's3': 3.0}
        epsilon = 0.1
        assert f_converge(V1, V2, epsilon) == False, "All states should be within epsilon away between V1 and V2."

        test_ok()

        @weight(25)
        @timeout_decorator.timeout(5.0)
        def test_2_alpha_beta(self):
            fmin, fmax, game_state, tic_tac_toe_board = get_locals(
                self.notebook_locals, ["minimize_score_alpha_beta", "maximize_score_alpha_beta", "game_state", "tic_tac_toe_board"])

            test_state = game_state(tic_tac_toe_board(
                ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ', 'o']))
            result = fmax(test_state, -2, 2)
            assert isinstance(result, tuple) and len(
                result) == 3, "Result should be a 3-tuple"
            assert result[0] == 0, "From ['x','o','x','x','x','o','o',' ','o'] max score should be 0."
            assert result[1] == 2, "From ['x','o','x','x','x','o','o',' ','o'] number of explored states should be 2."
            assert len(
                result[2]) == 2, "From ['x','o','x','x','x','o','o',' ','o'] optimal play should have 2 states."
            assert result[2][0].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ',
                                                'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."
            assert result[2][1].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', 'x',
                                                'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."

            test_state = game_state(tic_tac_toe_board(
                ['x', 'o', 'x', 'x', ' ', 'o', 'o', ' ', 'o']))
            result = fmax(test_state, -2, 2)
            assert result[0] == 0, "From ['x','o','x','x',' ','o','o',' ','o'] max score should be 0."
            assert result[1] == 5, "From ['x','o','x','x',' ','o','o',' ','o'] number of explored states should be 5."
            assert len(
                result[2]) == 3, "From ['x','o','x','x',' ','o','o',' ','o'] optimal play should have 3 states."
            assert result[2][0].board.moves == ['x', 'o', 'x', 'x', ' ', 'o', 'o', ' ',
                                                'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."
            assert result[2][1].board.moves == ['x', 'o', 'x', 'x', ' ', 'o', 'o', 'x',
                                                'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."
            assert result[2][2].board.moves == ['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x',
                                                'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."

            test_state = game_state(tic_tac_toe_board(
                ['x', 'o', ' ', 'x', ' ', ' ', 'o', ' ', ' ']))
            result = fmax(test_state, -2, 2)
            assert result[0] == 1, "From ['x','o',' ','x',' ',' ','o',' ',' '] max score should be 1."
            assert result[1] == 89, "From ['x','o',' ','x',' ',' ','o',' ',' '] number of explored states should be 89."
            assert len(
                result[2]) == 4, "From ['x','o',' ','x',' ',' ','o',' ',' '] optimal play should have 4 states."
            assert result[2][0].board.moves == ['x', 'o', ' ', 'x', ' ', ' ', 'o', ' ',
                                                ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."
            assert result[2][1].board.moves == ['x', 'o', ' ', 'x', 'x', ' ', 'o', ' ',
                                                ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."
            assert result[2][2].board.moves == ['x', 'o', 'o', 'x', 'x', ' ', 'o', ' ',
                                                ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."
            assert result[2][3].board.moves == ['x', 'o', 'o', 'x', 'x', 'x', 'o', ' ',
                                                ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."

            test_state = game_state(tic_tac_toe_board(
                ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ', 'o']))
            test_state.player = 2
            result = fmin(test_state, -2, 2)
            assert isinstance(result, tuple) and len(
                result) == 3, "Result should be a 3-tuple"
            assert result[0] == - \
                1, "From ['x','o','x','x','x','o','o',' ','o'] min score should be -1."
            assert result[1] == 2, "From ['x','o','x','x','x','o','o',' ','o'] number of explored states should be 2."
            assert len(
                result[2]) == 2, "From ['x','o','x','x','x','o','o',' ','o'] optimal play should have 2 states."
            assert result[2][0].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ',
                                                'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."
            assert result[2][1].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', 'o',
                                                'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."

            test_state = game_state(tic_tac_toe_board(
                ['o', 'x', 'o', 'o', ' ', 'x', 'x', ' ', 'x']))
            test_state.player = 2
            result = fmin(test_state, -2, 2)
            assert result[0] == 0, "From ['o','x','o','o',' ','x','x',' ','x'] min score should be 0."
            assert result[1] == 5, "From ['o','x','o','o',' ','x','x',' ','x'] number of explored states should be 5."
            assert len(
                result[2]) == 3, "From ['o','x','o','o',' ','x','x',' ','x'] optimal play should have 3 states."
            assert result[2][0].board.moves == ['o', 'x', 'o', 'o', ' ', 'x', 'x', ' ',
                                                'x'], "From ['o','x','o','o',' ','x','x',' ','x'] incorrect optimal play."
            assert result[2][1].board.moves == ['o', 'x', 'o', 'o', ' ', 'x', 'x', 'o',
                                                'x'], "From ['o','x','o','o',' ','x','x',' ','x'] incorrect optimal play."
            assert result[2][2].board.moves == ['o', 'x', 'o', 'o', 'x', 'x', 'x', 'o',
                                                'x'], "From ['o','x','o','o',' ','x','x',' ','x'] incorrect optimal play."

    @weight(20)
    @timeout_decorator.timeout(5.0)
    def test_3_expectimax(self):
        fmax, fexpected, game_state, tic_tac_toe_board = get_locals(
            self.notebook_locals, ["maximize_score_expectimax", "expected_score_expectimax", "game_state", "tic_tac_toe_board"])
        test_state = game_state(tic_tac_toe_board(
            ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ', 'o']))
        result = fmax(test_state)
        assert isinstance(result, tuple) and len(
            result) == 3, "Result should be a 3-tuple"
        assert result[0] == 0, "From ['x','o','x','x','x','o','o',' ','o'] max score should be 0."
        assert result[1] == 2, "From ['x','o','x','x','x','o','o',' ','o'] number of explored states should be 2."
        assert len(
            result[2]) == 2, "From ['x','o','x','x','x','o','o',' ','o'] optimal play should have 2 states."
        assert result[2][0].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ',
                                            'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."
        assert result[2][1].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', 'x',
                                            'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."

        test_state = game_state(tic_tac_toe_board(
            ['x', 'o', 'x', 'x', ' ', 'o', 'o', ' ', 'o']))
        result = fmax(test_state)
        assert result[0] == 0, "From ['x','o','x','x',' ','o','o',' ','o'] max score should be 0."
        assert result[1] == 5, "From ['x','o','x','x',' ','o','o',' ','o'] number of explored states should be 5."
        assert len(
            result[2]) == 3, "From ['x','o','x','x',' ','o','o',' ','o'] optimal play should have 3 states."
        assert result[2][0].board.moves == ['x', 'o', 'x', 'x', ' ', 'o', 'o', ' ',
                                            'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."
        assert result[2][1].board.moves == ['x', 'o', 'x', 'x', ' ', 'o', 'o', 'x',
                                            'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."
        assert result[2][2].board.moves == ['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x',
                                            'o'], "From ['x','o','x','x',' ','o','o',' ','o'] incorrect optimal play."

        test_state = game_state(tic_tac_toe_board(
            ['x', 'o', ' ', 'x', ' ', ' ', 'o', ' ', ' ']))
        result = fmax(test_state)
        assert result[0] == 1, "From ['x','o',' ','x',' ',' ','o',' ',' '] max score should be 1."
        assert result[1] == 246, "From ['x','o',' ','x',' ',' ','o',' ',' '] number of explored states should be 246."
        assert len(
            result[2]) == 4, "From ['x','o',' ','x',' ',' ','o',' ',' '] optimal play should have 4 states."
        assert result[2][0].board.moves == ['x', 'o', ' ', 'x', ' ', ' ', 'o', ' ',
                                            ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."
        assert result[2][1].board.moves == ['x', 'o', ' ', 'x', 'x', ' ', 'o', ' ',
                                            ' '], "From ['x','o',' ','x',' ',' ','o',' ',' '] incorrect optimal play."

        test_state = game_state(tic_tac_toe_board(
            ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ', 'o']))
        test_state.player = 2
        result = fexpected(test_state)
        assert isinstance(result, tuple) and len(
            result) == 3, "Result should be a 3-tuple"
        assert result[0] == - \
            1, "From ['x','o','x','x','x','o','o',' ','o'] min score should be -1."
        assert result[1] == 2, "From ['x','o','x','x','x','o','o',' ','o'] number of explored states should be 2."
        assert len(
            result[2]) == 2, "From ['x','o','x','x','x','o','o',' ','o'] optimal play should have 2 states."
        assert result[2][0].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', ' ',
                                            'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."
        assert result[2][1].board.moves == ['x', 'o', 'x', 'x', 'x', 'o', 'o', 'o',
                                            'o'], "From ['x','o','x','x','x','o','o',' ','o'] incorrect optimal play."

        test_state = game_state(tic_tac_toe_board(
            ['o', 'x', 'o', 'o', ' ', 'x', 'x', ' ', 'x']))
        test_state.player = 2
        result = fexpected(test_state)
        assert result[0] == 0.5, "From ['o','x','o','o',' ','x','x',' ','x'] min score should be 0.5."
        assert result[1] == 5, "From ['o','x','o','o',' ','x','x',' ','x'] number of explored states should be 5."
        assert len(
            result[2]) == 3, "From ['o','x','o','o',' ','x','x',' ','x'] optimal play should have 3 states."
        assert result[2][0].board.moves == ['o', 'x', 'o', 'o', ' ', 'x', 'x', ' ',
                                            'x'], "From ['o','x','o','o',' ','x','x',' ','x'] incorrect optimal play."

    @weight(5)
    @timeout_decorator.timeout(1.0)
    def test_4_form_word(self):
        word = get_locals(self.notebook_locals, ['form_confirmation_word'])
        password_hash = hash("Casablanca".lower())
        if hash(word.strip().lower()) == password_hash:
            return
        else:
            raise RuntimeError(f"Incorrect form word {word}")
