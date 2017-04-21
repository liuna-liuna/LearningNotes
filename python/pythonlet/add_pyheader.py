#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""create the meta information of a python script as its header

    create the meta information,
    ex. #!...python line, encoding, title, author, date, description, version, 
        usage, notes, python version,
    put it as header of a python script at the very beginning,
    and open the script in vim editor to continue programming in python.

    # ref:  http://www.jb51.net/article/91761.htm?source=1
"""
import os, sys, time

# const
AUTHOR = os.environ['USER'] or 'Na Liu'
VERSION = '0.1'
PY_VERSION = sys.version.split(' ')[0] or '2.7.10'
MAX_DIV_LENGTH = 80
MAX_FIELD_LENGTH = len('python version')
DEFAULT_N_A = 'n.a'

# get the script meta info
title = ''
while title == '':
    title = raw_input('Please input the script title [mandatory]:').strip()
    script_name = (title + '.py').lower().replace(' ', '_')
    if os.path.exists(script_name):
        print('\nA script with this name {0} already exists.\n'.format(script_name))
        title = ''
        
name = raw_input('Please input the author name [optional]:')
name = name and name.strip() or AUTHOR
description = raw_input('Please input the description [optional]:').strip() or DEFAULT_N_A
version = raw_input('Please input the script version [optional]:').strip() or VERSION
div = '=' * MAX_DIV_LENGTH
date = time.strftime('%Y-%m-%d')

# format header of a python script
data = []
data.append('#!/usr/bin/env Python')
data.append('# -*- coding: utf-8 -*-')
data.append('')
data.append('# {0:<{1}}: {2}'.format('title', MAX_FIELD_LENGTH, title))
data.append('# {0:<{1}}: {2}'.format('description', MAX_FIELD_LENGTH, description))
data.append('# {0:<{1}}: {2}'.format('author', MAX_FIELD_LENGTH, name))
data.append('# {0:<{1}}: {2}'.format('version', MAX_FIELD_LENGTH, version))
data.append('# {0:<{1}}: {2}'.format('usage', MAX_FIELD_LENGTH, 'python ' + script_name))
data.append('# {0:<{1}}: {2}'.format('date', MAX_FIELD_LENGTH, date))
data.append('# {0:<{1}}: {2}'.format('notes', MAX_FIELD_LENGTH, DEFAULT_N_A))
data.append('# {0:<{1}}: {2}'.format('python version', MAX_FIELD_LENGTH, PY_VERSION))
data.append('# {0}'.format(div))
data.append('')
data.append('')

# create the python script with header
with open(script_name, 'w') as f:
   f.writelines('\n'.join(data))

# continue to program in python in vim editor
os.system('vim +14 {0}'.format(script_name))
exit(0)

