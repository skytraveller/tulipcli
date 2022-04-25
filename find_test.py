#!/usr/bin/env python3

import tulipcli
import unittest


class TestFind(unittest.TestCase):

    def test_find(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                find="test,world!,Welcome!",
            ),
            [
                "{'test': {'description': 'update', 'parent': 0, 'uid': 2}}",
                "{'Welcome!': {'description': '', 'parent': 3, 'uid': 4}}",
                None
            ]
        )

    def test_bad_find(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                find=(9,4)
            ),
            [
                None
            ]
        )


if __name__ == '__main__':
    unittest.main()
