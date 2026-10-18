import unittest

from trusslab.domain.catalog import get_modules
from trusslab.ui.diagrams import DiagramFactory


class DiagramTests(unittest.TestCase):
    def test_every_module_has_a_nonempty_plotly_diagram(self):
        for module in get_modules():
            with self.subTest(module=module.id):
                figure = DiagramFactory.build(module.diagram_id)
                self.assertTrue(figure.data or figure.layout.shapes or figure.layout.annotations)
                self.assertGreater(figure.layout.height, 0)

    def test_force_method_diagram_highlights_selected_redundant(self):
        figure = DiagramFactory.build("rectangular_redundant")
        names = [trace.name for trace in figure.data]
        self.assertTrue(any("BD selected redundant" in name for name in names))

    def test_truss_compatibility_diagram_is_a_pin_jointed_truss(self):
        figure = DiagramFactory.build("truss_compatibility")
        names = [trace.name for trace in figure.data]
        self.assertTrue(any("AB" in name for name in names))
        self.assertTrue(any("AC" in name for name in names))
        self.assertTrue(any("BC" in name for name in names))
        annotations = [str(item.text) for item in (figure.layout.annotations or [])]
        self.assertTrue(any("joint c" in text.lower() for text in annotations))
        self.assertTrue(any("redundant reaction" in text.lower() for text in annotations))
        self.assertTrue(any(shape.type == "line" for shape in (figure.layout.shapes or [])), "The horizontal guide at C should be drawn.")


if __name__ == "__main__":
    unittest.main()
