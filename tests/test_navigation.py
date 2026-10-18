import unittest
import tomllib
from pathlib import Path

from trusslab.domain.catalog import get_modules
from trusslab.ui.navigation import NAV_GROUPS, NAV_LABELS, SIDEBAR_PAGES, navigation_groups, navigation_label


class SidebarNavigationTests(unittest.TestCase):
    def test_every_course_module_has_one_short_sidebar_label(self):
        module_ids = tuple(module.id for module in get_modules())
        self.assertEqual(set(NAV_LABELS), set(module_ids))
        self.assertEqual(len(NAV_LABELS), len(module_ids))
        for label in NAV_LABELS.values():
            with self.subTest(label=label):
                self.assertLessEqual(len(label), 24)

    def test_navigation_groups_cover_course_in_order_without_duplicates(self):
        module_ids = tuple(module.id for module in get_modules())
        groups = navigation_groups(module_ids)
        flattened = tuple(module_id for _, group_ids in groups for module_id in group_ids)
        self.assertEqual(flattened, module_ids)
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertEqual(tuple(title for title, _ in groups), tuple(title for title, _ in NAV_GROUPS))

    def test_future_unmapped_module_gets_a_more_group(self):
        known_plus_future = tuple(module.id for module in get_modules()) + ("future-topic",)
        groups = navigation_groups(known_plus_future)
        self.assertEqual(groups[-1], ("MORE", ("future-topic",)))


    def test_navigation_buttons_have_no_number_prefix(self):
        for module_id, label in NAV_LABELS.items():
            with self.subTest(module=module_id):
                self.assertFalse(label[:1].isdigit())
                self.assertEqual(navigation_label(module_id), label)
                self.assertEqual(navigation_label(module_id, mastered=True), f"✓  {label}")

    def test_app_does_not_use_deprecated_container_width_argument(self):
        root = Path(__file__).parents[1]
        for relative_path in (
            "app.py",
            "trusslab/ui/components.py",
            "trusslab/ui/experiments.py",
        ):
            with self.subTest(path=relative_path):
                source = (root / relative_path).read_text(encoding="utf-8")
                self.assertNotIn("use_container_width", source)


    def test_sidebar_uses_native_dark_theme_and_accessible_button_selectors(self):
        root = Path(__file__).parents[1]
        config = tomllib.loads((root / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
        sidebar = config["theme"]["sidebar"]
        self.assertEqual(sidebar["backgroundColor"], "#152535")
        self.assertEqual(sidebar["secondaryBackgroundColor"], "#1B3040")
        self.assertEqual(sidebar["textColor"], "#EDF5F7")
        self.assertEqual(sidebar["primaryColor"], "#48C7B6")

        theme_css = (root / "trusslab" / "ui" / "theme.py").read_text(encoding="utf-8")
        self.assertIn('button[data-testid="stBaseButton-secondary"]', theme_css)
        self.assertIn('button[data-testid="stBaseButton-primary"]', theme_css)
        self.assertNotIn('button[kind="secondary"]', theme_css)


    def test_sidebar_groups_have_explicit_spacing_and_readable_button_height(self):
        root = Path(__file__).parents[1]
        theme_css = (root / "trusslab" / "ui" / "theme.py").read_text(encoding="utf-8")
        self.assertIn(':has(.sidebar-nav-group)', theme_css)
        self.assertIn('margin-top:.38rem !important; margin-bottom:.14rem !important;', theme_css)
        self.assertIn('margin-top:.02rem !important; margin-bottom:.20rem !important;', theme_css)
        self.assertIn('min-height:2.0rem !important;', theme_css)
        self.assertIn('background:#1b3040 !important;', theme_css)
        self.assertIn('color:#e5eef2 !important;', theme_css)


    def test_main_page_does_not_render_top_hero_or_summary_cards(self):
        root = Path(__file__).parents[1]
        app_source = (root / "app.py").read_text(encoding="utf-8")
        main_source = app_source[app_source.index("def main()"):]
        self.assertNotIn("def _render_header", app_source)
        self.assertNotIn("_render_header()", main_source)
        self.assertNotIn("hero-panel", main_source)
        self.assertNotIn('metric("Modules mastered"', main_source)
        self.assertIn("_render_module(MODULES[index], index)", main_source)


    def test_quiz_hints_are_not_rendered(self):
        root = Path(__file__).parents[1]
        components = (root / "trusslab" / "ui" / "components.py").read_text(encoding="utf-8")
        self.assertNotIn("Hint for question", components)
        self.assertNotIn("st.write(question.hint)", components)
        self.assertIn("Check answers", components)
        self.assertIn("learning.evaluate(module, answers)", components)


    def test_abbreviations_is_a_separate_sidebar_page_not_a_lesson(self):
        page_ids = tuple(page_id for page_id, _ in SIDEBAR_PAGES)
        module_ids = tuple(module.id for module in get_modules())
        self.assertIn(("glossary", "Abbreviations & symbols"), SIDEBAR_PAGES)
        self.assertNotIn("glossary", module_ids)

        root = Path(__file__).parents[1]
        app_source = (root / "app.py").read_text(encoding="utf-8")
        component_source = (root / "trusslab" / "ui" / "components.py").read_text(encoding="utf-8")
        self.assertIn('"glossary": render_abbreviations_page', app_source)
        self.assertIn('active_page, selected_id = _render_sidebar()', app_source)
        self.assertIn('for page_id, page_label in SIDEBAR_PAGES:', app_source)
        self.assertIn('st.title("Abbreviations & symbols")', component_source)
        self.assertNotIn('with st.expander("Symbols & abbreviations used in this app"', component_source)
        self.assertIn('This page is separate from the lessons', component_source)


if __name__ == "__main__":
    unittest.main()
