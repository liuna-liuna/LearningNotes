# _*_ coding: utf-8 _*_

import urllib
import re
import lxml.etree
import lxml.builder
import contextlib

#
# subroutines
#
# level_Prefix: could be INFO, DEBUG.
def log_print(msg, level_Prefix):
	print "%s: %s" % (level_Prefix, msg)
	return
	
	
	
# get input options
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n", "--nodename", dest="nodename", help="node name to be checked")
parser.add_option("-d", "--debug",    dest="debug",    help="output more information for debugging purpose", action="store_true", default=False)
options, arguments = parser.parse_args()
if options.nodename:
	log_print( "The nodename input is: %s" %(options.nodename), "INFO " )
else:
	log_print( '''Please input the name of a node to be checked.
Usage: $0 [-n | --nodename] $nodename [-d | --debug]
	''', "INFO " )
	exit(1)

# Constants
FLAG_DEBUG			= options.debug
JENKINS_SERVER_URL  = "http://***:8080"
COMPUTER			= "computer"
SLAVEAGENT_JNLP		= "slave-agent.jnlp"
JENKINS_SLAVE_XML	= "jenkins-slave.xml"

url		= JENKINS_SERVER_URL + "/" + COMPUTER + "/" + options.nodename + "/" + SLAVEAGENT_JNLP
content = "";
with contextlib.closing( urllib.urlopen(url) ) as x:
	content = x.read()
	if FLAG_DEBUG:
		log_print( "The whole content from the url is:\n\n" + content + "\n", "DEBUG" )

# parse jenkins-agent.jnlp to get parameters: xpath: //jnlp/application-desc/argument
jnlp	= lxml.etree.fromstring(content)
jnlpUrl	= "";
for element in jnlp.iter():
	codebase = element.attrib.get('codebase')
	if (codebase):
		jnlpUrl = codebase + SLAVEAGENT_JNLP
		if FLAG_DEBUG:
			log_print( jnlpUrl, "DEBUG" )
		break

		
# to get parameter <argument>	       in jenkins-agent.jnlp to be used as value for  -secret in JENKINS_SLAVE_XML
# to get parameter <jnlp codebase=...>  in jenkins-agent.jnlp to be used as value for  -jnlpUrl in JENKINS_SLAVE_XML
secret = "";
for arg in jnlp.iter():
	argValue = arg.text
	if argValue:
		# check if a 64 bit hexdigest <- a SHA1 value
		sha1Pattern 	= '^[a-f0-9]{64}$'
		sha1PatCompiled = re.compile(sha1Pattern)
		if bool( sha1PatCompiled.match(argValue) ):
			secret = argValue
			if FLAG_DEBUG:
				log_print( "SHA1 is found: " + secret + "\n       It could be the -secret needed in " + JENKINS_SLAVE_XML, "DEBUG" )
			break
	else:
		continue


# create a JENKINS_SLAVE_XML file 
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

xmlFileName = JENKINS_SLAVE_XML + "_for_" + options.nodename
with open(xmlFileName, "w") as f:
	f.write( lxml.etree.tostring(theDoc, pretty_print=True) )
	log_print( "File " + xmlFileName + " is created.\n       It could be used to connect between a Jenkins server and a node.", "INFO " )

exit(0)





