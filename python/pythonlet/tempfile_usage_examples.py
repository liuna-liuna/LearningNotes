#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title         : tempfile usage examples
# description   : n.a
# author        : liuna
# version       : 0.1
# usage         : python tempfile_usage_examples.py
# date          : 2017-10-23
# notes         : n.a
# python version: 2
# ================================================================================
# imports
import os, tempfile

# consts
TMPDIR_1 = '/tmp'
DEFAULT_TMPDIR = TMPDIR_1 
DUMMY_FILENAME_1 = 'dummy_file_%s.txt' % os.getpid()
DEFAULT_FILENAME = DUMMY_FILENAME_1
DEFAULT_FILE_FULLPATH = '{}/{}'.format(DEFAULT_TMPDIR, DEFAULT_FILENAME)
SUFFIX_1 = '_suffix'
DEFAULT_SUFFIX = SUFFIX_1
PREFIX_1 = 'prefix_'
DEFAULT_PREFIX = PREFIX_1

# class
class TempfileUsageExample(object):
    def _create_a_temp_file_by_open(self, fn=DEFAULT_FILE_FULLPATH):
        temp = open(fn, 'w+b')
        try:
            print('[INFO] in function {}:\n\ttemp: {}'.format('_create_a_temp_file_by_open', temp))
            print('\ttemp.name: {}'.format(temp.name))
        finally:
            temp.close()
            os.remove(fn)

    def _create_a_temp_file_by_tempfile_TemporaryFile(self):
        temp = tempfile.TemporaryFile()
        try:
            print('[INFO] in function {}:\n\ttemp: {}'.format('_create_a_temp_file_by_tempfile_TemporaryFile', temp))
            print('\ttemp.name: {}'.format(temp.name))
        finally:
            temp.close()
    
    def _write_to_a_tempfile_TemporaryFile_in_binary(self):
        temp = tempfile.TemporaryFile()
        try:
            temp.write('Some data')
            temp.seek(0)
            print('[INFO] in function {}:\n\tcontent in file:\n{}\n'.format('_write_to_a_tempfile_TemporaryFile_in_binary', temp.read()))
        finally:
            temp.close()
    
    def _write_to_a_tempfile_TemporaryFile_in_text(self):
        temp = tempfile.TemporaryFile(mode='w+x')
        try:
            temp.writelines(['first\n', 'second\n'])
            temp.seek(0)
            print('[INFO] in function {}:\n\tcontent in file:\n'.format('_write_to_a_tempfile_TemporaryFile_in_text'))
            for line in temp:
                print(line.rstrip())
            print('\n')
        finally:
            temp.close()
    
    def _create_a_temp_file_by_tempfile_NamedTemporaryFile(self):
        temp = tempfile.NamedTemporaryFile()
        try:
            print('[INFO] in function {}:\n\ttemp: {}'.format('_create_a_temp_file_by_tempfile_NamedTemporaryFile', temp))
            print('\ttemp.name: {}'.format(temp.name))
        finally:
            temp.close()
        print('\tExists after close: {}'.format(os.path.exists(temp.name)))
    
    def _create_a_temp_file_by_tempfile_NamedTemporaryFile_with_options(self, \
            suffix=DEFAULT_SUFFIX, prefix=DEFAULT_PREFIX, dir=DEFAULT_TMPDIR):
        temp = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, dir=dir)
        try:
            print('[INFO] in function {}:\n\ttemp: {}'.format('_create_a_temp_file_by_tempfile_NamedTemporaryFile_with_options', temp))
            print('\ttemp.name: {}'.format(temp.name))
        finally:
            temp.close()


def main():
    tfusage = TempfileUsageExample()
    tfusage._create_a_temp_file_by_open()
    tfusage._create_a_temp_file_by_tempfile_TemporaryFile()
    tfusage._write_to_a_tempfile_TemporaryFile_in_binary()
    tfusage._write_to_a_tempfile_TemporaryFile_in_text()
    tfusage._create_a_temp_file_by_tempfile_NamedTemporaryFile()
    tfusage._create_a_temp_file_by_tempfile_NamedTemporaryFile_with_options()



# main entry
if __name__ == '__main__':
    main()


