#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Runs unittests for prefixer

Usage:
    ./test_prefixer.py

@author: kristi
"""

import unittest
from prefixer import prefix, prefixReduce, ParseError


class TestPrefix(unittest.TestCase):
    def setUp(self):
        pass

    def testPrefixExample(self):
        x = prefix("3")
        self.assertEqual(x, 3)

        x = prefix("1 + 1")
        self.assertEqual(x, ("+", 1, 1))

        x = prefix("2 * 5 + 1")
        self.assertEqual(x, ("+", ("*", 2, 5), 1))

        x = prefix("2 * ( 5 + 1 )")
        self.assertEqual(x, ("*", 2, ("+", 5, 1)))

        x = prefix("3 * x + ( 9 + y ) / 4")
        self.assertEqual(x, ("+", ("*", 3, "x"), ("/", ("+", 9, "y"), 4)))

    def testNumber(self):
        x = prefix("1")
        self.assertEqual(x, 1)

        x = prefix("10")
        self.assertEqual(x, 10)

        x = prefix("999")
        self.assertEqual(x, 999)

    def testLetter(self):
        x = prefix("a")
        self.assertEqual(x, "a")

        x = prefix("z")
        self.assertEqual(x, "z")

        x = prefix("a + b + c + d")
        self.assertEqual(x, ("+", ("+", ("+", "a", "b"), "c"), "d"))

    def testEmpty(self):
        x = prefix("")
        self.assertEqual(x, None)

        x = prefix(" ")
        self.assertEqual(x, None)

        x = prefix("(  )")
        self.assertEqual(x, None)

        x = prefix("( ( ) )")
        self.assertEqual(x, None)

    def testParenNumber(self):
        x = prefix("( 1 )")
        self.assertEqual(x, 1)

        x = prefix("( 10 )")
        self.assertEqual(x, 10)

        x = prefix("( 999 )")
        self.assertEqual(x, 999)

    def testParenLetter(self):
        x = prefix("( a )")
        self.assertEqual(x, "a")

        x = prefix("( z )")
        self.assertEqual(x, "z")

    def testEmbedParenNumber(self):
        x = prefix("( ( 1 ) )")
        self.assertEqual(x, 1)

        x = prefix("( ( ( 1 ) ) )")
        self.assertEqual(x, 1)

    def testParenError(self):
        with self.assertRaises(ParseError):
            prefix("( 1 ")

    def testAdd(self):
        x = prefix("1 + 2")
        self.assertEqual(x, ("+", 1, 2))

        x = prefix("1 + 2 + 3")
        self.assertEqual(x, ("+", ("+", 1, 2), 3))

        x = prefix("1 + 2 + 3 + 4")
        self.assertEqual(x, ("+", ("+", ("+", 1, 2), 3), 4))

    def testMult(self):
        x = prefix("3 * 2")
        self.assertEqual(x, ("*", 3, 2))

        x = prefix("3 * 2 * 4")
        self.assertEqual(x, ("*", ("*", 3, 2), 4))

    def testParenMult(self):
        x = prefix("( 3 * 2 )")
        self.assertEqual(x, ("*", 3, 2))

        x = prefix("5 * ( 3 * 2 )")
        self.assertEqual(x, ("*", 5, ("*", 3, 2)))

        x = prefix("( 3 * 2 ) * 5")
        self.assertEqual(x, ("*", ("*", 3, 2), 5))

    def testParenAdd(self):
        x = prefix("( 3 + 2 )")
        self.assertEqual(x, ("+", 3, 2))

        x = prefix("5 + ( 3 + 2 )")
        self.assertEqual(x, ("+", 5, ("+", 3, 2)))

        x = prefix("( 3 + 2 ) + 5")
        self.assertEqual(x, ("+", ("+", 3, 2), 5))

    def testParenMixed(self):
        x = prefix("5 * ( 3 + 2 )")
        self.assertEqual(x, ("*", 5, ("+", 3, 2)))

        x = prefix("( 3 + 2 ) * 5")
        self.assertEqual(x, ("*", ("+", 3, 2), 5))

    def testPrecedence(self):
        x = prefix("2 * 3 + 5")
        self.assertEqual(x, ("+", ("*", 2, 3), 5))

        x = prefix("5 + 2 * 3")
        self.assertEqual(x, ("+", 5, ("*", 2, 3)))

        x = prefix("1 + 2 * 3 + 5")
        self.assertEqual(x, ("+", ("+", 1, ("*", 2, 3)), 5))

        x = prefix("1 * 2 + 3 * 5")
        self.assertEqual(x, ("+", ("*", 1, 2), ("*", 3, 5)))


class TestPrefixReduce(unittest.TestCase):
    def setUp(self):
        pass

    def testReduceNumber(self):
        x = prefixReduce("1")
        self.assertEqual(x, 1)

        x = prefixReduce("10")
        self.assertEqual(x, 10)

        x = prefixReduce("999")
        self.assertEqual(x, 999)

    def testReduceAdd(self):
        x = prefixReduce("1 + 2")
        self.assertEqual(x, 3)

        x = prefixReduce("1 + 2 + 3")
        self.assertEqual(x, 6)

    def testReduceMult(self):
        x = prefixReduce("3 * 2")
        self.assertEqual(x, 6)

        x = prefixReduce("3 * 2 * 4")
        self.assertEqual(x, 24)

    def testReduceParen(self):
        x = prefixReduce("(3 * 2)")
        self.assertEqual(x, 6)

        x = prefixReduce("(3 + 2)")
        self.assertEqual(x, 5)

        x = prefixReduce("5 * (3 + 2)")
        self.assertEqual(x, 25)

        x = prefixReduce("(3 + 2) * 5")
        self.assertEqual(x, 25)

    def testReduceLetter(self):
        x = prefixReduce("a")
        self.assertEqual(x, "a")

        x = prefixReduce("z")
        self.assertEqual(x, "z")

    def testReduceLetterAdd(self):
        x = prefixReduce("a + b")
        self.assertEqual(x, ("+", "a", "b"))

        x = prefixReduce("a + 1")
        self.assertEqual(x, ("+", "a", 1))

        x = prefixReduce("1 + a")
        self.assertEqual(x, ("+", 1, "a"))

    def testReduceLetterSubtract(self):
        x = prefixReduce("a - b")
        self.assertEqual(x, ("-", "a", "b"))

        x = prefixReduce("a - 1")
        self.assertEqual(x, ("-", "a", 1))

        x = prefixReduce("1 - a")
        self.assertEqual(x, ("-", 1, "a"))

    def testReduceLetterMult(self):
        x = prefixReduce("a * b")
        self.assertEqual(x, ("*", "a", "b"))

        x = prefixReduce("a * 1")
        self.assertEqual(x, ("*", "a", 1))

        x = prefixReduce("1 * a")
        self.assertEqual(x, ("*", 1, "a"))

    def testReduceLetterDivide(self):
        x = prefixReduce("a / b")
        self.assertEqual(x, ("/", "a", "b"))

        x = prefixReduce("a / 1")
        self.assertEqual(x, ("/", "a", 1))

        x = prefixReduce("1 / a")
        self.assertEqual(x, ("/", 1, "a"))

    def testReduceMixed(self):
        x = prefixReduce("a + ( 1 + 2 )")
        self.assertEqual(x, ("+", "a", 3))

        x = prefixReduce("( 1 + 2 ) + a")
        self.assertEqual(x, ("+", 3, "a"))

        x = prefixReduce("a + ( 2 * 3 )")
        self.assertEqual(x, ("+", "a", 6))

        x = prefixReduce("( 2 * 3 ) + a")
        self.assertEqual(x, ("+", 6, "a"))


if __name__ == "__main__":
    unittest.main()