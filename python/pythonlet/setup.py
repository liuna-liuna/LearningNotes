# for distutils* to generate a package
from distutils.core import setup, Extension

module1 = Extension('hello', sources=['hello.c'])
setup(name='hello',
		version='1.0',
		description='hello ${input}',
		ext_modules = [module1]
		)


