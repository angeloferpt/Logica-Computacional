"""Testes independentes das células de demonstração do notebook."""

import random
import unittest

from sudoku import (
    SudokuCSP,
    box,
    cube,
    make_sudoku,
    path,
    random_clues,
    run_example,
    validate_solution,
)


class GroupTests(unittest.TestCase):
    def test_box_add_matrix_and_initial_cells(self):
        group = box(2, {(0, 1): None, (3, 3): 4})
        group.add(0, 1, 2)
        group.add(3, 3, 4)
        matrix = group.matrix()
        self.assertEqual(len(matrix), 4)
        self.assertEqual(matrix[0], [0, 2, 0, 0])
        self.assertEqual(matrix[3][3], 4)

    def test_invalid_cells_and_values(self):
        for i, j, value in [(-1, 0, None), (4, 0, None),
                            (0, 4, None), (0, 0, 0), (0, 0, 5)]:
            with self.subTest(i=i, j=j, value=value):
                with self.assertRaises(ValueError):
                    box(2).add(i, j, value)
        with self.assertRaises(ValueError):
            box(2).add(0, 0, 1).add(0, 0, 2)

    def test_cube_and_paths_in_both_directions(self):
        self.assertEqual(
            set(cube(2, 1, 1).cells),
            {(2, 2), (2, 3), (3, 2), (3, 3)},
        )
        self.assertEqual(set(path(2, (0, 3), (0, 0)).cells),
                         {(0, j) for j in range(4)})
        self.assertEqual(set(path(2, (3, 1), (0, 1)).cells),
                         {(i, 1) for i in range(4)})
        with self.assertRaises(ValueError):
            path(2, (0, 0), (1, 1))
        with self.assertRaises(ValueError):
            cube(2, 2, 0)

    def test_random_clues(self):
        clues = random_clues(3, 12, random.Random(42))
        self.assertEqual(len(clues.cells), 12)
        self.assertTrue(all(1 <= value <= 9 for value in clues.cells.values()))
        with self.assertRaises(ValueError):
            random_clues(2, 17)


class SolverTests(unittest.TestCase):
    def test_full_flow_for_three_sizes(self):
        for n, seed in [(2, 2026), (3, 2027), (4, 2028)]:
            with self.subTest(n=n):
                clues, solution, problem, attempts = run_example(n, seed)
                self.assertTrue(validate_solution(n, solution, clues))
                self.assertEqual(problem.group_count, 3 * n * n + 1)
                self.assertGreaterEqual(attempts, 1)

    def test_arbitrary_extra_groups(self):
        diagonal = box(2, {(i, i): None for i in range(4)})
        problem = make_sudoku(2, box(2), (diagonal,))
        solution = problem.solve()
        self.assertTrue(validate_solution(2, solution, box(2)))
        self.assertEqual({solution[i][i] for i in range(4)}, {1, 2, 3, 4})

    def test_impossible_puzzle_returns_none(self):
        clues = box(2, {(0, 0): 1, (0, 1): 1})
        problem = make_sudoku(2, clues)
        self.assertIsNone(problem.solve())
        self.assertEqual(problem.status, "INFEASIBLE")

    def test_mismatched_group_is_rejected(self):
        problem = SudokuCSP(2)
        with self.assertRaises(ValueError):
            problem.add_groups(box(3))

    def test_validator_detects_broken_solution(self):
        clues, solution, _, _ = run_example(2, 2026)
        self.assertTrue(validate_solution(2, solution, clues))
        broken = [row[:] for row in solution]
        broken[0][0] = broken[0][1]
        with self.assertRaises(AssertionError):
            validate_solution(2, broken, clues)


if __name__ == "__main__":
    unittest.main()
