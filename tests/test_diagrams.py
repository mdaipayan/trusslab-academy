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
        # Important labels must be visible by default, not only on hover.
        visible_text = [str(item.text) for item in (figure.layout.annotations or [])]
        for label in ("AB · 4 m", "AC · 3 m", "BC · 5 m", "P = 10 kN ↓", "R = Cₓ"):
            self.assertTrue(any(label in text for text in visible_text), f"Missing visible annotation: {label}")
        label_annotations = [
            item for item in (figure.layout.annotations or [])
            if any(label in str(item.text) for label in ("AB · 4 m", "AC · 3 m", "BC · 5 m"))
        ]
        self.assertEqual(len(label_annotations), 3)
        self.assertTrue(all(item.bgcolor for item in label_annotations), "Member labels should have opaque backgrounds for contrast.")
        joint_trace = next(trace for trace in figure.data if trace.name == "Joints")
        self.assertEqual(list(joint_trace.textposition), ["top left", "top center", "top left"])


    def test_fbd_catalog_entries_have_color_coded_visible_diagrams(self):
        modules = {module.id: module for module in get_modules()}
        expected = {
            "joints": ("joint_c_fbd",),
            "sections": ("section_cut_fbd",),
            "determinate-example": ("whole_truss_fbd", "joint_c_fbd"),
            "truss-compatibility": ("released_truss_fbd", "unit_load_fbd"),
            "indeterminate-triangle": ("loaded_truss_fbd", "joint_c_loaded_fbd"),
            "force-method": ("released_rectangular_fbd",),
        }
        for module_id, diagram_ids in expected.items():
            with self.subTest(module=module_id):
                self.assertEqual(modules[module_id].free_body_ids, diagram_ids)
                for diagram_id in diagram_ids:
                    figure = DiagramFactory.build_free_body(diagram_id)
                    self.assertTrue(figure.data or figure.layout.shapes or figure.layout.annotations)
                    self.assertGreater(figure.layout.height, 0)
                    self.assertIsNotNone(figure.layout.title.text)

    def test_joint_fbd_uses_semantic_color_groups_and_force_labels(self):
        figure = DiagramFactory.build_free_body("joint_c_fbd")
        colors = [annotation.arrowcolor for annotation in (figure.layout.annotations or []) if getattr(annotation, "arrowcolor", None)]
        self.assertIn("#d18b14", colors)  # applied load
        self.assertIn("#16845a", colors)  # assumed tension
        labels = [str(annotation.text) for annotation in (figure.layout.annotations or [])]
        self.assertTrue(any("ΣFₓ = 0" in text for text in labels))
        self.assertTrue(any("ΣFᵧ = 0" in text for text in labels))



if __name__ == "__main__":
    unittest.main()
