"""Unit tests for make_landscape.py pure data (no PIL).

Headline invariant: every gateway named on the landscape poster must actually
appear in README.md — so the shareable image can't advertise something the list
doesn't carry.
"""

import unittest

from make_landscape import README, all_matches, build_landscape


class TestLandscapeData(unittest.TestCase):
    def setUp(self):
        self.land = build_landscape()

    def test_nine_categories_each_nonempty(self):
        self.assertEqual(len(self.land), 9)
        for cat in self.land:
            self.assertTrue(cat["title"].strip())
            self.assertGreaterEqual(len(cat["items"]), 4)

    def test_known_kinds(self):
        for cat in self.land:
            self.assertIn(cat["kind"], {"hosted", "self", "cloud", "china", "cross"})

    def test_no_drift_every_gateway_is_in_readme(self):
        readme = README.read_text(encoding="utf-8")
        missing = [m for m in all_matches(self.land) if m not in readme]
        self.assertEqual(missing, [], f"landscape names not found in README: {missing}")

    def test_reasonable_total(self):
        self.assertGreaterEqual(len(all_matches(self.land)), 45)


if __name__ == "__main__":
    unittest.main()
