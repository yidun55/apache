#!/usr/bin/env python
#coding: utf-8

import sys



for line in sys.stdin:
    print line


def find_json(line_str):
    """
    pick out json from line
    """
    assert type(line_str) == str, "line_str must be string"
    stack = []
    start = 0
    end = 0 
    for value, key in enumerate(line_str):
        if key == u"{":
            stack.append(value)
        elif key == u"}":
            if len(stack) == 0:
                break
            else:
                start = stack.pop()
                end = value
    if start != end and start != 0:
        json_str = line_str[start:end + 1]
        try:
            false = False
            true = True
            return eval(json_str)
        except:
            pass