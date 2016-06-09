# _*_ coding: utf-8 _*_

'''
Usage: %(scriptName)s [-n | --nodename] $nodename [-d | --debug]
'''

#
# Constants
# hard-code default value for jenkins master url, roles url, roles search pattern and user authenToken
JENKINS_URL 	= 'http://${jenkins_master}:8080'
ROLES_URL		= 'role-strategy/assign-roles'
ROLES_PATTERN   = '<tr name="\[(?i)(i\d{6})?\]".*?<input name="\[(admin|user|job-creator|guest)\]"\s*checked="true".*?</tr>'
USERAUTHENTOKEN = '${jenkins_account1}:${jenkins_account1_authenToken}'

import subprocess, re
from subprocess import PIPE
from   optparse import OptionParser

class GetJenkinsUsersAndRoles(object):
#TODO
	'''A class to get labels of a jenkins node
	
	input: 
		userAuthenToken: 	user name and authentication token,
							which has permissions to access the Jenkins page:
								${jenkinsurl}/role-strategy/assign-roles
							ex. ${user1}:${authenToken1}
							
		jenkinsurl: 		the url of jenkins server ex. http://***:8080
		
	output:
		User1 has role: role1
		User2 has role: role2
	'''
	def __init__(self, userAuthenToken, jenkinsurl):
		self.userAuthenToken = userAuthenToken
		self.jenkinsurl      = jenkinsurl
	
	def getUsersAndRoles(self):
		# get users and roles, format them, output
		rolesUrl = self.jenkinsurl + '/' + ROLES_URL
		winCmds = ('curl', '-u', self.userAuthenToken, rolesUrl)
		output, error = subprocess.Popen(list(winCmds), stdout=PIPE, stderr=PIPE).communicate()
		pattern = ROLES_PATTERN
		
		for m in re.finditer(pattern, output):	
			print "{} has role: {}".format(m.group(1), m.group(2))

# entry point: main
if __name__ == '__main__':
#	
	# get input options and set defaults if not given.
	parser = OptionParser()
	parser.add_option("-p", "--userAuthenToken", 	dest="userAuthenToken",
						help='''user name and authentication token,
							 which has permissions to access the Jenkins page''')
	parser.add_option("-u", "--jenkinsurl", 		dest="jenkinsurl", 
						help="the url of jenkins server ex. http://***:8080")
	options, arguments = parser.parse_args()
	if options.userAuthenToken:
		userAuthenToken = options.userAuthenToken
	else:
		userAuthenToken = USERAUTHENTOKEN
	if options.jenkinsurl:
		jenkinsurl = options.jenkinsurl
	else:
		jenkinsurl = JENKINS_URL
	GetJenkinsUsersAndRoles(userAuthenToken, jenkinsurl).getUsersAndRoles()
	
##
## check_users_and_roles_in_jenkins.py
## output
##	${jenkins_account2} has role: admin
##	${jenkins_account3} has role: job-creator
