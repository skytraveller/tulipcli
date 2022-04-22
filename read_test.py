#!/usr/bin/env python3

import tulipcli
import unittest


class TestRead(unittest.TestCase):
    testdata = {
        'test': {
            'description': 'Hello',
            'world!': {
                'Welcome!': {}
            },
            'uid': 2,
        }
    }

    def test_read(self):
        self.assertEqual(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                read=self.testdata,
            ),
            "Item(s) imported"
        )

    def test_string_read(self):
        self.assertEqual(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                read=str(self.testdata),
            ),
            "Item(s) imported"
        )

    def test_bad_read(self):
        self.assertIn(
            tulipcli.Tulipcli(
                database="results.db",
                noversion=True,
                read="{'test': {'desc",
            ),
            [
                "Unable to read data. EOL while scanning string literal (<string>, line 1)",
                "Unable to read data. invalid syntax (<string>, line 1)",
            ]
        )


if __name__ == '__main__':
    unittest.main()
