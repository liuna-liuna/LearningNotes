#!/usr/bin/env Python
# -*- coding: utf-8 -*-

# title         : hello use
# description   : n.a
# author        : liuna
# version       : 0.1
# usage         : python hello_use.py
# date          : 2017-05-15
# notes         : n.a
# python version: 2.7.10
# ================================================================================
# consts 
N = 3
# SELF_PY_TOPPATH = '/Volumes/Data/Learning/Python'
# import sys
# sys.path.insert(0, SELF_PY_TOPPATH)
import hello


print(hello.message('C'))
print(hello.message('module ' + hello.__file__))

for i in xrange(N):
    print(hello.message(str(i)))


