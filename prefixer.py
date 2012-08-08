#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converts an infix arithmetic expression into a prefix one.

Usage:
    ./prefixer.py input.txt
    # print out the prefix version of expressions in input.txt

    ./prefixer.py -r input.txt
    # print out the reduced prefix version of expressions in input.txt

@author: kristi
"""

import re


def prefixReduce(string):
    """
    Wrapper function for the Parser
    Returns a result tuple tree for the reduced prefix expression
    """
    parser = Parser()
    parsed = parser.parse(string)
    result = parser.reduce(parsed)
    return result


def prefix(string):
    """
    Wrapper function for the Parser
    Returns a result tuple tree for the prefix expression
    """
    parser = Parser()
    result = parser.parse(string)
    return result


def stringify(result):
    """
    Turns the result tuple tree into a string
    """
    if not result:
        return ""
    return re.sub(r"[',]", "", str(result))


class ParseError(Exception):
    pass


class Parser(object):
    OPERATORS = set("+-*/")
    ADD = set("+-")
    MULT = set("*/")
    PARENTHESIS = set("()")

    def parse(self, string):
        """
        Parses the infix expression into a tuple-based tree
        """
        self.tokens = self.tokenize(string)
        return self.parseExpression()

    def parseExpression(self):
        """
        Recursively parses the infix expression into a tuple-based tree and
        reduces numeric expressions
        """
        a = self.parseOperand()
        last_op = None
        while self.peekToken() in self.OPERATORS:
            op = self.nextToken()
            b = self.parseOperand()
            if last_op in self.ADD and op in self.MULT:
                # Perform mult before add
                a = (a[0], a[1], (op, a[2], b))
            else:
                a = (op, a, b)
                last_op = op
        return a

    def parseOperand(self, paren=False):
        """
        Parses a operand (either an expression contained in parenthesis,
        or a single number or letter)
        """
        if self.peekToken() == ")":
            return None
        tok = self.nextToken()
        if tok == "(":
            a = self.parseExpression()
            tok = self.nextToken()
            if tok != ")":
                raise ParseError("Expected close parenthesis")
            return a
        else:
            return tok

    def nextToken(self):
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        else:
            return None

    def peekToken(self):
        if len(self.tokens) > 0:
            return self.tokens[0]
        else:
            return None

    def toInt(self, string):
        try:
            return int(string)
        except ValueError:
            return string

    def tokenize(self, string):
        """
        Returns a list of tokens
        """
        op = re.escape(''.join(self.OPERATORS | self.PARENTHESIS))
        pattern = r'[{op}]|\d+|[a-z]'.format(op=op)
        return [self.toInt(s) for s in re.findall(pattern, string)]

    def reduce(self, result):
        if not isinstance(result, tuple):
            return result
        op, a, b = result
        a = self.reduce(a)
        b = self.reduce(b)
        if isinstance(a, int) and isinstance(b, int):
            if op == "+":
                return (a + b)
            if op == "-":
                return (a - b)
            if op == "*":
                return (a * b)
            if op == "/":
                return (a / b)
        else:
            return (op, a, b)


if __name__ == "__main__":

    import sys

    script_name = sys.argv[0]
    args = sys.argv[1:]
    if len(args) < 1:
        print script_name + " requires at least 1 argument"
        exit(1)

    do_reduce = False
    for a in args:
        if a == "-h":
            print __doc__
            exit(1)
        elif a == "-r":
            do_reduce = True
        else:
            filename = a

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if do_reduce:
                print stringify(prefixReduce(line))
            else:
                print stringify(prefix(line))