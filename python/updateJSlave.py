# _*_ coding: utf-8 _*_

import urllib
import libxml2
import re
import lxml.etree
import lxml.builder

url		= "http://${jenkins_server1}:8080/computer/${jenkins_slave1}/slave-agent.jnlp"
content = urllib.urlopen(url).read()
print content
#	print html.getcode()
#	print html.geturl()
#	print html.info()

#
# example jnlp 
#	http://${jenkins_server1}:8080/computer/${jenkins_slave1}/slave-agent.jnlp
#
##	<jnlp codebase="http://${jenkins_server1}:8080/computer/${jenkins_slave1}/" spec="1.0+">
##		<information>
##			<title>Slave Agent for ${jenkins_slave1}</title>
##			<vendor>Jenkins project</vendor>
##			<homepage href="https://jenkins-ci.org/"/>
##		</information>
##		
##		<security>
##			<all-permissions/>
##		</security>
##		
##		<resources>
##			<j2se version="1.5+"/>
##			<jar href="http://${jenkins_server1}:8080/jnlpJars/remoting.jar"/>
##			<property name="hudson.showWindowsServiceInstallLink" value="true"/>
##		</resources>
##		<application-desc main-class="hudson.remoting.jnlp.Main">
##			<argument>${jenkins_slave1_secret}</argument>
##			<argument>${jenkins_slave1}</argument>
##			<argument>-url</argument>
##			<argument>http://${jenkins_server1}:8080/</argument>
##		</application-desc>
##		
##	</jnlp>

# parse jenkins-agent.jnlp to get parameters: xpath: //jnlp/application-desc/argument
jnlp		= libxml2.parseMemory(content, len(content))

#only for test #	
#only for test #	fileName 	= "jnlp.xml"
#only for test #	jnlp 		= libxml2.parseFile(fileName)
#only for test #	

# to get parameter <jnlp codebase=...>  in jenkins-agent.jnlp to be used as value for  -jnlpUrl in jenkins-slave.xml
xpath4codebase	= "//jnlp[@codebase]"
jnlpUrl			= "";
for jnlpElement in jnlp.xpathEval(xpath4codebase):
	for jnlpElement in jnlp.xpathEval(xpath4codebase):
	    for prop in jnlpElement.properties:
	        if prop.name == 'codebase':
				jnlpUrl	 = prop.content + "slave-agent.jnlp"
				print jnlpUrl
				break

# to get parameter <argument>	       in jenkins-agent.jnlp to be used as value for  -secret in jenkins-slave.xml
xpath4arg	= "//jnlp/application-desc/argument"
secret		= "";
for arg in jnlp.xpathEval(xpath4arg):
	argValue = arg.content
	print argValue
	
	# check if a 64 bit hexdigest <- a SHA1 value
	sha1Pattern 	= '^[a-f0-9]{64}$'
	sha1PatCompiled = re.compile(sha1Pattern)
	if bool( sha1PatCompiled.match(argValue) ):
		secret = argValue
		print "SHA1 is found: could be the -secret needed in jenkins-slave.xml."
		
# to be tested 
jnlp.freeDoc()


# create a jenkins-slave.xml file 
E = lxml.builder.ElementMaker()
SERVICE = E.service
ID = E.id
NAME = E.name
DESCRIPTION = E.description
EXECUTABLE = E.executable
ARGUMENTS = E.arguments
LOGMODE = E.logmode
ONFAILURE = E.onfailure

theDoc = SERVICE(
	ID('jenkinsslave-c__jenkins'),
	NAME('Jenkins Slave'),
	DESCRIPTION('This service runs a slave for Jenkins continuous integration system.'),
	EXECUTABLE('java'),
	ARGUMENTS('-Xrs  -jar "%BASE%\slave.jar" -jnlpUrl ' + jnlpUrl + ' -secret ' + secret),
	LOGMODE('rotate'),
	ONFAILURE('', action = 'restart'),
)

with open("jenkins-slave.xml", "w") as f:
	f.write( lxml.etree.tostring(theDoc, pretty_print=True) )

	
	
	


