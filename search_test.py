#!/usr/bin/env python3

import tulipcli
import unittest


class TestSearch(unittest.TestCase):

    def test_search(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                search=True,
                name="ome",
                description="ome"
            ),
            [
                ["{'Welcome!': {'description': '', 'parent': 3, 'uid': 4}}"],
                []
            ]
        )


if __name__ == '__main__':
    unittest.main()
