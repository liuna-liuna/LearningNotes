#
#	get the configure urls of all jobs on jenkins
#
import contextlib
import urllib
import json
topurl  = 'http://shg-cvom-infra.pgdev.sap.corp:8080/api/json?tree=jobs[url]'
topurl  = 'http://10.193.245.135:8080/api/json?tree=jobs[url]'
url1 = 'http://10.193.245.135:8080/job/voter-master/config.xml'
disabledPattern = r'<disabled>false</disabled>'
gitrepoPattern  = r'.*https://.*SV/.*'

with contextlib.closing( urllib.urlopen( topurl ) ) as j:
    jjobs = json.loads( j.read() )
    urls  = jjobs['jobs']
    for url in urls:
		configFilePath = url.values()[0] + 'config.xml'	
		configFilePath = configFilePath.replace( r'***', r'10.193.245.135' )
		with contextlib.closing( urllib.urlopen( configFilePath ) ) as config:
			configContent = config.read();
			if ( re.search(disabledPattern, configContent) == None ):
				continue
			searchResult = re.search( gitrepoPattern, configContent )
			if searchResult:
				print 'for file: ' + configFilePath
				print searchResult.group(0)
				
