#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title         : fabfile
# description   : n.a
# author        : liuna
# version       : 0.1
# usage         : python fabfile.py
# date          : 2017-11-04
# notes         : n.a
# python version: 2
# ================================================================================
# imports
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *

# globals
# examples for running commands through env.host_string or env.hosts
# [works for one host] env.host_string = '127.0.0.1'
env.hosts = ['127.0.0.1']
env.port = '5000'
env.user = 'test'
env.password = 'passwd'

# examples for running commands through env.roledefs
env.roledefs = {
    'db': ['db1', 'db2'],
    'web': ['web1', 'web2', 'web3'],
}

# tasks
def print_mem():
    cmd = 'free -m'
    cmd_output = run(cmd)
    print('[INFO] memory usage through {}:\n{}'.format(cmd, cmd_output))

def ls_home():
    with cd('/home'):
        run('ls -l')    # run on env.hosts
        # local('ls -l')  # run local on computer where this script is run.

def ls_tmp():
    print('[INFO]', red("I'm 201"))
    local('ls -l /tmp')

def get_file():
    print('[INFO]', green("I'm get file 45 to 186"))
    get('/tmp/tt', '/tmp/')
    local('ls -l /tmp')

@roles('db')
def migrate():
    # db stuff here
    pass
    
@roles('web')
def update():
    # code updates here
    pass


# main tentry
if __name__ == '__main__':
    ls_home()
    prinmt_mem()
    get_file()


