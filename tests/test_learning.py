import unittest

from trusslab.domain.catalog import get_modules
from trusslab.services.learning import LearningService, ProgressService
from trusslab.services.engineering import single_member_sizing, solve_indeterminate_triangle_areas, solve_vertical_load_truss_compatibility


class LearningServiceTests(unittest.TestCase):
    def setUp(self):
        self.module = get_modules()[0]
        self.learning = LearningService()

    def test_perfect_score_passes_and_partial_score_does_not(self):
        perfect = {q.id: q.correct_option_id for q in self.module.quiz}
        result = self.learning.evaluate(self.module, perfect)
        self.assertEqual(result.score, 3)
        self.assertTrue(result.passed)
        imperfect = dict(perfect)
        imperfect[self.module.quiz[0].id] = next(o.id for o in self.module.quiz[0].options if o.id != self.module.quiz[0].correct_option_id)
        result = self.learning.evaluate(self.module, imperfect)
        self.assertEqual(result.score, 2)
        self.assertFalse(result.passed)

    def test_missing_answer_is_marked_not_correct(self):
        answers = {q.id: None for q in self.module.quiz}
        result = self.learning.evaluate(self.module, answers)
        self.assertEqual(result.score, 0)
        self.assertFalse(result.passed)
        self.assertTrue(all(not item.is_correct for item in result.feedback))

    def test_progress_records_attempt_and_mastery(self):
        state = {}
        progress = ProgressService(state)
        answers = {q.id: q.correct_option_id for q in self.module.quiz}
        result = self.learning.evaluate(self.module, answers)
        progress.record(self.module.id, result)
        self.assertTrue(progress.is_mastered(self.module.id))
        self.assertEqual(progress.best_score(self.module.id), 3)
        self.assertEqual(progress.attempt_count(self.module.id), 1)
        self.assertEqual(progress.completion_percent(10), 10)

    def test_failed_attempt_is_not_mastery_and_best_score_is_kept(self):
        state = {}
        progress = ProgressService(state)
        correct = {q.id: q.correct_option_id for q in self.module.quiz}
        wrong = dict(correct)
        q = self.module.quiz[0]
        wrong[q.id] = next(o.id for o in q.options if o.id != q.correct_option_id)
        progress.record(self.module.id, self.learning.evaluate(self.module, wrong))
        self.assertFalse(progress.is_mastered(self.module.id))
        progress.record(self.module.id, self.learning.evaluate(self.module, correct))
        self.assertTrue(progress.is_mastered(self.module.id))
        self.assertEqual(progress.best_score(self.module.id), 3)
        self.assertEqual(progress.attempt_count(self.module.id), 2)


class EngineeringCalculationTests(unittest.TestCase):
    def test_triangle_compatibility_examples_match_the_supplied_equation(self):
        equal = solve_indeterminate_triangle_areas((1000, 1000, 1000))
        self.assertAlmostEqual(equal["R"], -16.6666667, places=5)
        self.assertAlmostEqual(equal["F_AB"], 3.3333333, places=5)
        self.assertAlmostEqual(equal["F_AC"], -17.5, places=5)
        self.assertAlmostEqual(equal["F_BC"], -4.1666667, places=5)
        changed = solve_indeterminate_triangle_areas((1000, 1000, 2000))
        self.assertAlmostEqual(changed["R"], -15.3094463, places=5)
        self.assertAlmostEqual(changed["F_AC"], -16.4820847, places=5)

    def test_single_member_sizing_reports_stress_and_mass(self):
        result = single_member_sizing(1000, 100, 2.5, 150)
        self.assertAlmostEqual(result["stress_mpa"], 100)
        self.assertAlmostEqual(result["volume_m3"], .0025)
        self.assertAlmostEqual(result["mass_kg"], 19.625)
        self.assertTrue(result["feasible_by_stress"])
        self.assertFalse(single_member_sizing(400, 100, 2.5, 150)["feasible_by_stress"])

    def test_invalid_engineering_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            solve_vertical_load_truss_compatibility((1000, 0, 1000))
        with self.assertRaises(ValueError):
            solve_indeterminate_triangle_areas((1000, -1000, 1000))
        with self.assertRaises(ValueError):
            single_member_sizing(0, 100, 2.5, 150)
        with self.assertRaises(ValueError):
            single_member_sizing(1e-300, 1e308, 1.0, 1.0)


if __name__ == "__main__":
    unittest.main()
