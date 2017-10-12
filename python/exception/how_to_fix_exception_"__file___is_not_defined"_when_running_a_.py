#
# how to fix exception "__file__ is not defined" when running a .py
#
    Complete output from command C:\Python27\python.exe -c "import setuptools, tokenize;__file__='c:\\cygwin64\\tmp\\pip-build-cigve2\\wordcloud\\setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record c:\cygwin64\tmp\pip-_zxrhm-record\install-record.txt --single-version-externally-managed --compile:
    running install
    running build
	
Ex.
in CLI：
	python.exe -c "import Localize, subprocess; subprocess.call(['python','Localize.py'])"
	python.exe -c "import Localize, subprocess; subprocess.call(['python','C:\workspace\*\Scripts\${python_script1}.py'])"

in PowerShell ISE：
	&C:\Python27\python.exe -c "import Localize, subprocess; subprocess.call(['python', 'C:\workspace\*\Scripts\${python_script1}.py'])"
	&C:\Python27\python.exe -c "import Localize, subprocess; subprocess.call(['python', '${python_script1}.py'])"
