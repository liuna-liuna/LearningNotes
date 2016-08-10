@echo off
REM
REM copy a set of files from one path to another
REM

setlocal EnableDelayedExpansion

:: Method1 hard code files into a multiline variable
::
REM how to set a multiline variable
REM 	ref doc: http://stackoverflow.com/questions/6379619/explain-how-dos-batch-newline-variable-hack-works
REM		ref doc: http://stackoverflow.com/questions/16291479/store-multiline-string-in-batch-variable
REM
SET flist= %USERPROFILE%\My Documents^
 %USERPROFILE%\Favorites^
 %USERPROFILE%\Desktop^
 %USERPROFILE%\AppData\Local\Microsoft\Outlook^
 %USERPROFILE%\AppData\Roaming\Microsoft\Outlook^
 %USERPROFILE%\AppData\Roaming\Microsoft\Signatures^
 C:\Work\documents

SET from_dd=C:
SET to_dd=E:

REM echo name: !flist!
SET new_flist_nodd=!flist:%from_dd%=!
REM echo %new_flist_nodd%
REM echo !new_flist_nodd!
REM echo.

for %%F in ( !new_flist_nodd! ) do (
	echo copy file from %from_dd%%%F to %to_dd%%%F ...
	xcopy /S/E/Y/I "%from_dd%%%F" "%to_dd%%%F"
	echo   done.
)

:: Method2 using a temp file as input
::	1) input files list into inputFile.txt
::	2) change for loop to as below:
::		REM for /f "delims= " %%F in ( 'type inputFile.txt' ) do (
::		for /f %%F in ( 'type inputFile.txt' ) do (
::			echo copy file from %from_path%\%%F to %to_path%\%%F
::			echo.
::		REM	xcopy /Y "%from_path%\%%F" "%to_path%\%%F"
::		)

