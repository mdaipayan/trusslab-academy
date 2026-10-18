import unittest

from trusslab.domain.catalog import get_modules
from trusslab.ui.navigation import NAV_GROUPS, NAV_LABELS, navigation_groups


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


if __name__ == "__main__":
    unittest.main()
