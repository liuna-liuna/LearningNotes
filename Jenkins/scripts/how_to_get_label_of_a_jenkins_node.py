# _*_ coding: utf-8 _*_
#
# ref doc: http://stackoverflow.com/questions/14531919/node-labels-from-jenkins-api
#
JENKINS_URL = "http://$Jenkins_server:8080"

from jenkinsapi import jenkins
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

node_labels = dict()
jenkins_obj = jenkins.Jenkins(JENKINS_URL)
node_names  = jenkins_obj.get_nodes().keys()

#TODO
# hard-code the to-be-find node name patterns
pattern='PVGD'
for node_name in node_names:
    if node_name != "master" and re.match(pattern, node_name):
            req = urlopen('{}/computer/{}'.format(JENKINS_URL, node_name))
            soup = BeautifulSoup(req.read())
            node_labels[node_name] = [tag.text for tag in soup.findAll("a", {"class":"tag0 model-link inside"})]

# data structure:
#	for li in node_labels.items():
#	    print li
#	#output:	('$Node1', [u'builder', u'windows'])

# for debug
for k,v in node_labels.iteritems():
    print 'Node {} has labels: {}'.format(k, ' '.join(str(t) for t in v))



