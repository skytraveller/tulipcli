#!/usr/bin/env python3

import tulipcli
import unittest


class TestWrite(unittest.TestCase):

    def test_write(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                write=True,
                uid=2,
            ),
            [
                "{'test': {'description': 'update', 'parent': 0, 'uid': 2, 'world!': {'description': '', 'parent': 2, 'uid': 3}}}",
                "{'test': {'description': 'update', 'parent': 0, 'uid': 2}}",
                "Item 2 not found"
            ]
        )


if __name__ == '__main__':
    unittest.main()
