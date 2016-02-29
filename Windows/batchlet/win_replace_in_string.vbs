'win_replace_in_string.vbs //nologo /node:$nodename
'
' Replace a substring in a string
'	ref doc: http://www.regular-expressions.info/vbscript.html
Dim DEBUG
DEBUG = False 'False is default: output no information
Dim re, string
Set re 			= new RegExp
re.Global		= True 'False is default. True: to return or replace all matches.
re.IgnoreCase 	= True

' get HOSTNAME / node name from input
If DEBUG = True Then 
	WScript.Echo "To get the host name from the given node name..."
End If
Dim strHostname
Set objArgs 	= WScript.Arguments.Named
If ( objArgs.Exists("node") AND objArgs.Item("node") <> "" ) Then
	strHostname	= objArgs.Item("node")
	strHostname	= Trim(strHostname)
Else
	WScript.Echo "No node name is give." & vbCRLF & "Please call the script: win_replace_in_string.vbs //nologo /node:$nodename" & vbCRLF
	WScript.Quit 0
End If


' remove suffixes
' suffixes are hard-coded in an array
Dim arrTBDPatterns
arrTBDPatterns = Array("~scm", "-Z820", "UT_coverage", "\(", "\)", "-b8")
Dim i
For i=0 To ubound(arrTBDPatterns)
	re.pattern = arrTBDPatterns(i)
	If DEBUG = True Then
		WScript.Echo "pattern is " & re.pattern & vbCRLF & "strHostname is " & strHostname & vbCRLF
	End If
	strHostname = re.Replace(strHostname, "")
Next

' to translate a node name from master to shg-cvom-infra
If strHostname = "master" Then
	strHostname = "shg-cvom-infra"
End If

If DEBUG = True Then
	WScript.Echo "Host name is " & strHostname
	WScript.Echo "To get the host name is done." & vbCRLF
End If

' to add specific domain suffix to host name
re.pattern = "PVGD5083"
If re.Test(strHostname) Then
	strHostname = strHostname & ".apj.global.corp.sap"
ElseIf strHostname = "shg-cvom-infra" Then
	strHostname = "shg-cvom-infra.pgdev.sap.corp"
Else
	strHostname = strHostname & ".dhcp.pgdev.sap.corp"
End If

' return the translated HOSTNAME
'	ref doc: http://stackoverflow.com/questions/15129085/how-to-return-a-string-from-a-vbscript-which-is-executed-from-a-python-file
WScript.StdOut.Write strHostname


