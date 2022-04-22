#!/usr/bin/env python3

import tulipcli
import unittest


class TestDelete(unittest.TestCase):

    def test_delete(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                delete=True,
                noversion=True,
                uid=3,
            ),
            [
                "Deleted 3",
                "Item 3 not found",
            ]
        )


if __name__ == '__main__':
    unittest.main()
