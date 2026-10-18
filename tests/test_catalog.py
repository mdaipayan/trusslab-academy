import unittest
from pathlib import Path

from trusslab.domain.catalog import get_modules
from trusslab.domain.glossary import GLOSSARY
from trusslab.domain.models import ContentBlock, QuizOption, QuizQuestion
from trusslab.services.engineering import solve_vertical_load_truss_compatibility


class CatalogTests(unittest.TestCase):
    def test_every_module_has_objectives_and_three_quiz_questions(self):
        modules = get_modules()
        self.assertEqual(len(modules), 10)
        ids = [module.id for module in modules]
        self.assertEqual(len(ids), len(set(ids)))
        for module in modules:
            with self.subTest(module=module.id):
                self.assertTrue(module.objectives)
                self.assertTrue(module.purpose)
                self.assertEqual(len(module.quiz), 3)
                for question in module.quiz:
                    self.assertIn(question.correct_option_id, {option.id for option in question.options})

    def test_equilibrium_and_compatibility_lessons_explain_equations_with_examples(self):
        modules = {module.id: module for module in get_modules()}
        joints_text = " ".join((block.heading + " " + block.text + " " + block.formula) for block in modules["joints"].sections)
        truss_text = " ".join((block.heading + " " + block.text + " " + block.formula) for block in modules["truss-compatibility"].sections)
        triangle_text = " ".join((block.heading + " " + block.text + " " + block.formula) for block in modules["indeterminate-triangle"].sections)
        method_text = " ".join((block.heading + " " + block.text + " " + block.formula) for block in modules["force-method"].sections)
        self.assertIn("no unbalanced force", joints_text)
        self.assertIn("F_{BC}=-25", joints_text)
        self.assertIn("pin-jointed triangular truss", truss_text)
        self.assertIn("acts directly at joint C", truss_text)
        self.assertIn("u_C", truss_text)
        self.assertIn("13.5", truss_text)
        self.assertIn("1.667", truss_text)
        compatibility_quiz = {q.id: q for q in modules["truss-compatibility"].quiz}
        self.assertEqual(compatibility_quiz["tc1"].correct_option_id, "B")
        self.assertEqual(compatibility_quiz["tc3"].correct_option_id, "B")
        self.assertIn("u_C", triangle_text)
        self.assertIn("own signed axial deformation", method_text)

    def test_truss_compatibility_force_method_example(self):
        response = solve_vertical_load_truss_compatibility((1000, 1000, 1000))
        self.assertAlmostEqual(float(response["R"]), 1.6666666667, places=6)
        self.assertAlmostEqual(float(response["F_AB"]), 1.6666666667, places=6)
        self.assertAlmostEqual(float(response["F_AC"]), -8.75, places=6)
        self.assertAlmostEqual(float(response["F_BC"]), -2.0833333333, places=6)


    def test_member_force_notation_uses_f_and_glossary_is_complete(self):
        modules = get_modules()
        all_lesson_text = " ".join(
            " ".join((block.heading, block.text, block.formula, " ".join(block.items)))
            for module in modules for block in module.sections
        )
        self.assertIn(r"F_{AB}", all_lesson_text)
        self.assertIn(r"\frac{F}{A}", all_lesson_text)
        self.assertNotIn("N_AB", all_lesson_text)
        self.assertNotIn("N_{AB}", all_lesson_text)
        self.assertNotIn("Nᵢ", all_lesson_text)
        glossary_rows = [row for _, rows in GLOSSARY for row in rows]
        glossary_symbols = {row[0] for row in glossary_rows}
        self.assertIn("Fᵢ or F_AB", glossary_symbols)
        self.assertIn("N", glossary_symbols)  # N is explicitly documented as the unit newton.
        self.assertIn("DSM", glossary_symbols)
        self.assertIn("PDF", glossary_symbols)
        self.assertIn("kN·m", glossary_symbols)
        self.assertEqual(len(glossary_rows), 47)
        unit_load_row = next(row for row in glossary_rows if row[0] == "nᵢ")
        self.assertIn("actual member force is Fᵢ", unit_load_row[2])
        # Keep the displayed notation consistent in experiments and diagram labels too.
        root = Path(__file__).parents[1]
        ui_text = " ".join(path.read_text(encoding="utf-8") for path in (
            root / "trusslab" / "ui" / "experiments.py",
            root / "trusslab" / "ui" / "diagrams.py",
        ))
        self.assertNotIn("N_AB", ui_text)
        self.assertNotIn("N_{AB}", ui_text)
        self.assertNotIn("member force N", ui_text.lower())

    def test_uploaded_source_audit_is_present_in_force_method_lesson(self):
        module = next(item for item in get_modules() if item.id == "force-method")
        text = " ".join(block.text for block in module.sections)
        self.assertIn("12,280 mm", text)
        self.assertIn("13,400 mm", text)
        self.assertIn("Verify both formulation and arithmetic", text)

    def test_invalid_lesson_blocks_are_rejected(self):
        with self.assertRaises(ValueError):
            ContentBlock(kind="formula")
        with self.assertRaises(ValueError):
            ContentBlock(kind="bullets")

    def test_question_requires_a_valid_correct_answer(self):
        with self.assertRaises(ValueError):
            QuizQuestion("broken", "Pick one", (QuizOption("A", "Alpha"), QuizOption("B", "Beta")), "C", "Why", "Hint")


if __name__ == "__main__":
    unittest.main()
