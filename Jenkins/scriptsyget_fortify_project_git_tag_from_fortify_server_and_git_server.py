@echo off
REM
REM get latest version from fortify 360 ssc server
REM

REM
REM Usage: %0 [-p]
REM				-p: patch, to get latest patch version in git
REM 

REM constants
REM
SET FORTIFY_SERVER=https://${Fortify_server1}/ssc
SET FORTIFY_AUTHTOKEN=${Fortify_authtoken}
SET FORTIFY_CMD=fortifyclient
SET PROJECT_KEY=${Project_name1_in_Fortify_server}
SET GIT_EXE=c:\jenkins\tools\hudson.plugins.git.GitTool\git-win-1.9.4\bin\git.exe
SET GIT_REPO_FETCH_URL=ssh://service.tip.${Project_name1_in_Fortify_server}@${Git_project1}:29418/SV/${Project_name1_in_Fortify_server}.html.git


REM check latest minor by default for version: major:minor:patch
SET VERSION_TO_CHECK=1
if "X%1"=="X-p" set /a VERSION_TO_CHECK+=1
SET FORTIFY_VERSION=
SET GIT_TAG=

:: in cmd:
::		fortifyclient listprojects -url https://${Fortify_server1}/ssc -authtoken ${Fortify_authtoken}  | grep ${Project_name1_in_Fortify_server} | sort /R
::		C:\fortify>fortifyclient listprojects -url https://${Fortify_server1}/ssc -authtoken ${Fortify_authtoken}  | grep ${Project_name1_in_Fortify_server} | sort /R | head -1 | cut -f1
::			16051
REM SET fortify_client="%FORTIFY_CMD% listprojects -url %FORTIFY_SERVER% -authtoken %FORTIFY_AUTHTOKEN% ^| grep %PROJECT_KEY% ^| sort /R ^| head -1 ^| cut -f1"
SET fortify_client="%FORTIFY_CMD% listprojects -url %FORTIFY_SERVER% -authtoken %FORTIFY_AUTHTOKEN% | grep %PROJECT_KEY% | sort /R | head -1 | cut -f1"
REM echo CMD to run: 
REM echo     %fortify_client%
REM echo.

REM
REM step1. get latest Project ID in fortify  360 ssc server
REM
for /f %%F in ( '%fortify_client%' ) do (
REM for /f "tokens=1-2 delims= " %%F in ( 'date /T' ) do (
	setlocal EnableDelayedExpansion
	SET FORTIFY_VERSION=%%F
REM 	echo     latest Project ID of %PROJECT_KEY% is:
REM	echo !FORTIFY_VERSION!
REM 	echo.
	setlocal DisableDelayedExpansion
)

REM
REM step2. get latest release tag in git server
REM
::	in cmd
::		git ls-remote --tags ssh://${Git_account1}@${Git_project1}:29418/SV/${Project_name1_in_Fortify_server}.html.git
::		[not the latest] c:\git\${workspace1}>git ls-remote --tags ssh://${Git_account1}@leanditst.wdf.sap.corp:29418/SV/${Project_name1_in_Fortify_server}.html.git | cut -f2 | grep -v '\{' | sed 's#refs/tags/##' | "C:\Program Files (x86)\Git\bin\sort.exe" -n
::		[not the latest] c:\git\${workspace1}>git ls-remote --tags ssh://${Git_account1}@leanditst.wdf.sap.corp:29418/SV/${Project_name1_in_Fortify_server}.html.git | cut -f2 | grep -v '\{' | sed 's#refs/tags/##' | sort
::
::		[might work]	"C:\Program Files (x86)\Git\bin\sort.exe" -n -t. -k2,2 -k3,3 -k1,1 c:\Work\4Fortify\tt
::						c:\PROGRA~2\Git\bin\sort.exe
::
REM SET git_lsremote="git ls-remote --tags %GIT_REPO_FETCH_URL% ^| cut -f2 ^| grep -v '\{' ^| sed 's#refs/tags/##' ^| c:\PROGRA~2\Git\bin\sort.exe -r -n -t. -k2,2 -k3,3 -k1,1 ^| head -%VERSION_TO_CHECK% ^|tail -1"
SET git_lsremote="%GIT_EXE% -c core.askpass=true ls-remote --tags %GIT_REPO_FETCH_URL% | cut -f2 | grep -v '\{' | sed 's#refs/tags/##' | c:\PROGRA~2\Git\bin\sort.exe -r -n -t. -k2,2 -k3,3 -k1,1 | head -%VERSION_TO_CHECK% |tail -1"

REM echo CMD to run:
REM echo     %git_lsremote%
REM echo.
for /f %%F in ( '%git_lsremote%' ) do (
	setlocal EnableDelayedExpansion
	set GIT_TAG=%%F
REM 	echo     latest git tag of %GIT_REPO_FETCH_URL% is:
REM	echo !GIT_TAG!
REM 	echo.
	setlocal DisableDelayedExpansion
)

echo %FORTIFY_VERSION% %GIT_TAG%
REM echo %ERRORLEVEL%
REM exit /b 0


REM fortifyclient listprojects -url https://${Fortify_server1}/ssc -authtoken ${Fortify_authtoken} 
REM		| C:\jenkins\tools\hudson.plugins.git.GitTool\git-win-1.9.4\bin\gawk.exe '{print $4}'

:: get output from a command in batch
::
::	REM NB:in a batch file, need to use %%i not %i
::	setlocal EnableDelayedExpansion
::	SET lf=-
::	FOR /F "delims=" %%i IN ('dir \ /b') DO if ("!out!"=="") (set out=%%i) else (set out=!out!%lf%%%i)
::	ECHO %out%
::
::	ref doc: http://stackoverflow.com/questions/108439/how-do-i-get-the-result-of-a-command-in-a-variable-in-windows
::
::	in cmd line:
::			CMD /V:ON to enable the delayed execution in a batch script
::		ref doc: http://www.computerhope.com/forum/index.php?topic=51665.0
::
:: 	in cmd line: Note that if your command includes a pipe then you need to escape it with a caret, 
::		for example: for /f "delims=" %%a in ('echo foobar^|sed -e s/foo/fu/') do @set foobar=%%a – yoyo Apr 21 '15 at 22:42 


REM output from fortify listprojects
REM
REM ID      Name                    Version
REM
REM	12639   ${Project_name1_in_Fortify_server}                        ${FORTIFY_PROJECT1}_1.1
REM	11280   ${Project_name1_in_Fortify_server}                        ${FORTIFY_PROJECT2}_1.0




