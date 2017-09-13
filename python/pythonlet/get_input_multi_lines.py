#!/usr/bin/env Python
# -*- coding: utf-8 -*-

# title         : get input multi lines
# description   : read multiple lines from input ex STDIN,
#                 replace newline('\n') with semicolon(';').
# author        : liuna
# version       : 0.1
# usage         : python get_input_multi_lines.py
# date          : 2017-09-13
# notes         : n.a
# python version: 2.7.10
# ================================================================================

import sys


def get_input_multi_lines_rawinput():
    res = []
    print('[INFO] input start:')
    try:
        while True:
            # ^D doesn't generate EOF for sys.stdin.readline()
            # ref:  https://stackoverflow.com/questions/1892215/how-to-send-eof-to-python-sys-stdin-from-commandline-ctrl-d-doesnt-work
            # line = sys.stdin.readline().strip('\n')
            line = raw_input().strip()
            if line:
                res.append(line)
    except (EOFError, IOError) as e:
        print('[INFO] input end.')
    finally:
        return ';'.join(res)

def get_input_multi_lines_sysstdin():
    res = []
    print('[INFO] input start:')
    try:
        # ^D doesn't generate EOF for sys.stdin.readline()
        # ref:  http://compgroups.net/comp.lang.python/sys.stdin.readline/1638306
        for line in iter(sys.stdin.readline, ''):
            line = line.strip('\n')
            if line:
                res.append(line)
        # for line in sys.stdin:
            # res.append(line.strip('\n'))
    except (EOFError, IOError) as e:
        print('[INFO] input end.')
    finally:
        return ';'.join(res)


# main entry
if __name__ == '__main__':
    # print(get_input_multi_lines_rawinput())
    print(get_input_multi_lines_sysstdin())
