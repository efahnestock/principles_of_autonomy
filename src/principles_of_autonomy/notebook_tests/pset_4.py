import unittest
import numpy as np
import timeout_decorator
from gradescope_utils.autograder_utils.decorators import weight
from mdp_utils import MDP, build_mdp
# from nose.tools import assert_equal

from principles_of_autonomy.grader import get_locals

# Function for tests
def test_ok():
    try:
        from IPython.display import display_html
        display_html("""<div class="alert alert-success">
        <strong>Test passed!!</strong>
        </div>""", raw=True)
    except:
        print("test ok!!")

class TestPSet4(unittest.TestCase):
    def __init__(self, test_name, notebook_locals):
        super().__init__(test_name)
        self.notebook_locals = notebook_locals

    # problem 1, total score 55
    @weight(5)
    @timeout_decorator.timeout(5.0)
    def test_1_convergence(self):
        f_converge  = get_locals(
            self.notebook_locals, ["value_convergence"])
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
    def test_2_value_iteration(self):
        f_value_iteration = get_locals(self.notebook_locals, ["value_iteration"])
        # Test Case 1: Simple MDP (2x2 Grid)
        n = 2
        goal = (1, 1)
        obstacles = []
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        V = f_value_iteration(mdp, epsilon=1e-3)

        expected_V = {(0, 0): 73.02, (0, 1): 93.31, (1, 0): 93.31, (1, 1): 0.0}
        for s in V:
            assert abs(V[s] - expected_V[s]) < 0.1, f"Test Case 1 failed for state {s}: {V[s]} vs {expected_V[s]}"

        # Test Case 2: 3x3 Grid with Obstacles and Goal
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        V = f_value_iteration(mdp, epsilon=1e-3)

        expected_V = {
            (0, 1): 0.0, (1, 2): 93.17, (0, 0): 15.60,
            (2, 1): 93.17, (2, 0): 69.56, (1, 1): 71.45,
            (2, 2): 0.0, (1, 0): 54.60, (0, 2): 26.62
        }
        
        for s in V:
            assert abs(V[s] - expected_V[s]) < 0.1, f"Test Case 2 failed for state {s}: {V[s]} vs {expected_V[s]}"

        # Test Case 3: Larger Grid (5x5 Grid)
        n = 5
        goal = (4, 4)
        obstacles = [(2, 2), (1, 3), (3, 1)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.9)
        V = f_value_iteration(mdp, epsilon=1e-3)

        expected_V = {
            (1, 3): 0.0, (3, 0): 9.42, (0, 2): 3.76, (2, 1): -97.92, (0, 3): 9.42,
            (4, 0): 25.56, (1, 2): -97.92, (3, 3): 73.43, (4, 4): 0.0, (2, 2): 0.0,
            (0, 4): 25.56, (4, 1): 31.12, (1, 1): -6.96, (3, 2): -40.72, (0, 0): 2.03,
            (1, 4): 31.12, (2, 3): -40.72, (4, 2): 71.28, (1, 0): 2.29, (0, 1): 2.29,
            (3, 1): 0.0, (2, 0): 3.76, (4, 3): 95.17, (3, 4): 95.17, (2, 4): 71.28
        }
        
        for s in V:
            assert abs(V[s] - expected_V[s]) < 0.1, f"Test Case 3 failed for state {s}: {V[s]} vs {expected_V[s]}"

        # Test Case 4: Discount Factor Edge Case (gamma=0)
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.0)  # gamma=0, ignore future rewards
        V = f_value_iteration(mdp, epsilon=1e-3)

        expected_V = {
            (0, 0): 0.0,  (0, 1): 0.0, (0, 2): 0.0,
            (1, 0): 0.0,  (1, 1): 0.0, (1, 2): 80.0,
            (2, 0): 0.0,  (2, 1): 80.0,(2, 2): 0.0
        }
        for s in V:
            assert abs(V[s] - expected_V[s]) < 0.1, f"Test Case 4 failed for state {s}: {V[s]} vs {expected_V[s]}"

        # Test Case 5: High Stochasticity (Low p)
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        mdp = build_mdp(n, 0.1, obstacles, goal, 0.9)  # p=0.1 introduces high stochasticity
        V = f_value_iteration(mdp, epsilon=1e-3)

        expected_V = {
            (0, 1): 0.0, (1, 2): 76.90, (0, 0): 39.01,
            (2, 1): 76.90, (2, 0): 61.67, (1, 1): 57.77,
            (2, 2): 0.0, (1, 0): 48.65, (0, 2): 61.67
        }

        for s in V:
            assert abs(V[s] - expected_V[s]) < 0.1, f"Test Case 5 failed for state {s}: {V[s]} vs {expected_V[s]}"
        
        test_ok()

    @weight(15)
    @timeout_decorator.timeout(5.0)
    def test_3_extract_policy(self):
        f_value_iteration, f_extract_policy = get_locals(self.notebook_locals, ["value_iteration", "extract_policy"])
        # Test Case 1: 2x2 Grid, No Obstacles, Simple Goal
        n = 2
        goal = (1, 1)
        obstacles = []
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        
        V = f_value_iteration(mdp, epsilon=1e-3)
        Pi = f_extract_policy(mdp, V)
        
        # Expected optimal policy should lead to the goal efficiently
        assert Pi[(0, 1)] == 'right', "Test Case 1 failed: Expected optimal policy should lead to the goal efficiently"
        assert Pi[(1, 0)] == 'up', "Test Case 1 failed: Expected optimal policy should lead to the goal efficiently"
        
        # Test Case 2: 3x3 Grid, One Obstacle, One Goal
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        
        V = f_value_iteration(mdp, epsilon=1e-3)
        Pi = f_extract_policy(mdp, V)
        
        # Check that the policy leads to the goal and avoids the obstacle
        assert Pi[(1, 2)] == 'right', "Test Case 2 failed: Need to lead to goal."
        assert Pi[(0, 0)] == 'down', "Test Case 2 failed: Need to avoid obstacle."
        assert Pi[(2, 1)] == 'up', "Test Case 2 failed: Need to lead to goal."
        assert Pi[(2, 0)] == 'up', "Test Case 2 failed: Need to lead to goal."
        assert Pi[(1, 1)] == 'right', "Test Case 2 failed: Need to avoid obstacle."
        assert Pi[(1, 0)] == 'right', "Test Case 2 failed: Need to avoid obstacle."
        assert Pi[(0, 2)] == 'up', "Test Case 2 failed: Need to avoid obstacle."

        # Test Case 3: Larger Grid (4x4), Multiple Obstacles
        n = 4
        goal = (3, 3)
        obstacles = [(1, 1), (2, 2)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.9)
        
        V = f_value_iteration(mdp, epsilon=1e-3)
        Pi = f_extract_policy(mdp, V)
            
        # Check the policy near the goal and obstacles
        assert Pi[(2, 1)] == 'right', "Test Case 3 failed: Need to lead to goal AND away from obstacle (as best as you can)."
        assert Pi[(1, 2)] == 'up', "Test Case 3 failed: Need to lead to goal AND away from obstacle (as best as you can)."
        assert Pi[(3, 2)] == 'right', "Test Case 3 failed: Need to lead to goal (as best as you can) AND away from obstacle."
        assert Pi[(2, 3)] == 'up', "Test Case 3 failed: Need to lead to goal (as best as you can) AND away from obstacle."
        
        # Test Case 4: Deterministic MDP (p=1), Simple 3x3 Grid
        n = 3
        goal = (2, 2)
        obstacles = []
        mdp = build_mdp(n, 1.0, obstacles, goal, 0.8)  # Deterministic transitions (p=1)
        
        V = f_value_iteration(mdp, epsilon=1e-3)
        Pi = f_extract_policy(mdp, V)
        
        # Check that the policy moves directly to the goal
        assert Pi[(1, 2)] == 'right', "Test Case 4 failed: The policy should move right towards the goal."
        assert Pi[(2, 1)] == 'up', "Test Case 4 failed: The policy should move up towards the goal."

        test_ok()


    @weight(10)
    @timeout_decorator.timeout(5.0)
    def test_4_observations(self):
        answer = get_locals(self.notebook_locals, ["answer"])
        true_answer = {
            "A": 3,
            "B": 2,
            "C": 1,
            "D": 4
        }
        assert answer == true_answer, "Incorrect match."

        test_ok()

    # problem 2, total score 40
    @weight(15)
    @timeout_decorator.timeout(5.0)
    def test_5_policy_evaluation(self):
        f_policy_evaluation = get_locals(self.notebook_locals, ["policy_evaluation"])
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        
        # Build MDP with p=0.8 and gamma=0.8
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        
        # Fixed policy: move right unless blocked
        policy = {
            (0, 0): 'right', (0, 1): 'right', (0, 2): 'right',
            (1, 0): 'right', (1, 1): 'right', (1, 2): 'right',
            (2, 0): 'right', (2, 1): 'right', (2, 2): 'right',
        }

        # Perform policy evaluation
        V = f_policy_evaluation(mdp, policy, epsilon=1e-3)

        # Expected values for each state
        expected_values = {
            (0, 0): -102.98,
            (0, 1): 0.0,    # Obstacle
            (0, 2): -46.58,
            (1, 0): 8.22,
            (1, 1): 26.78,
            (1, 2): 89.29,
            (2, 0): 8.47,
            (2, 1): 29.66,
            (2, 2): 0.0,    # Goal
        }
        
        # Assert that the computed values match the expected values
        for state, expected_value in expected_values.items():
            assert abs(V[state] - expected_value) < 0.1, "Incorrect values."

        test_ok()


    @weight(15)
    @timeout_decorator.timeout(5.0)
    def test_6_policy_improvement(self):
        f_policy_evaluation, f_policy_improvement =  get_locals(self.notebook_locals, ["policy_evaluation", "policy_improvement"])
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)
        
        # Fixed policy (initial)
        policy = {
            (0, 0): 'right', (0, 1): 'right', (0, 2): 'right',
            (1, 0): 'right', (1, 1): 'right', (1, 2): 'right',
            (2, 0): 'right', (2, 1): 'right', (2, 2): 'right',
        }

        # Perform policy evaluation to get value function V
        V = f_policy_evaluation(mdp, policy, epsilon=1e-3)

        # Perform policy improvement
        improved_policy = f_policy_improvement(mdp, policy, V)
        
        # Expected optimal policy
        expected_policy = {
            (0, 0): 'down',
            (0, 1): 'up',  # Obstacle, doesn't really matter
            (0, 2): 'up',
            (1, 0): 'up',
            (1, 1): 'right',
            (1, 2): 'right',
            (2, 0): 'up',
            (2, 1): 'up',
            (2, 2): 'up',  # Goal, doesn't really matter
        }
            
        # Assert that the improved policy matches the expected optimal policy
        for state, expected_action in expected_policy.items():
            assert improved_policy[state] == expected_action, "Incorrect improved policy."

        test_ok()

    @weight(10)
    @timeout_decorator.timeout(5.0)
    def test_7_policy_iteration(self):
        f_policy_iteration = get_locals(self.notebook_locals, ["policy_iteration"])
        n = 3
        goal = (2, 2)
        obstacles = [(0, 1)]
        
        # Build MDP with p=0.8 and gamma=0.8
        mdp = build_mdp(n, 0.8, obstacles, goal, 0.8)

        # Run policy iteration
        optimal_policy, optimal_V = f_policy_iteration(mdp, epsilon=1e-3)
        
        # Expected optimal policy
        expected_policy = {
            (0, 0): 'down',
            (0, 1): 'up',  # Obstacle, arbitrary
            (0, 2): 'up',
            (1, 0): 'right',
            (1, 1): 'right',
            (1, 2): 'right',
            (2, 0): 'up',
            (2, 1): 'up',
            (2, 2): 'up',  # Goal, arbitrary
        }
            
        # Assert that the resulting policy matches the expected optimal policy
        for state, expected_action in expected_policy.items():
            assert optimal_policy[state] == expected_action, "Incorrect final policy."

        test_ok()

    @weight(5)
    @timeout_decorator.timeout(1.0)
    def test_8_form_word(self):
        word = get_locals(self.notebook_locals, ['form_confirmation_word'])
        password_hash = hash("Casablanca".lower()) #to change!!
        if hash(word.strip().lower()) == password_hash:
            return
        else:
            raise RuntimeError(f"Incorrect form word {word}")