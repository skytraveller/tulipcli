#!/usr/bin/env python3

import tulipcli
import unittest


class TestUpdate(unittest.TestCase):

    def test_update(self):
        self.assertEqual(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                update=True,
                name="test",
                uid=2,
                description="update",
            ),
            "{'test': {'description': 'update', 'parent': 0, 'uid': 2}}"
        )


if __name__ == '__main__':
    unittest.main()
