#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import json

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

content = {"deployment": "Run Deployment %s %s" % (application, environment),
           "application": application,
           "environments": [environment],
           "deploymentPlan": deploymentPlan,
           "build": build,
           "project": project
           }

print "* Sending content {0}".format(json.dumps(content))

context = '/datamanagement/a/api/{0}/run-deployments'.format(nolioServer['version'])
print "* Context is {0}".format(context)

request = HttpRequest(nolioServer, username, password)
response = request.post(context, json.dumps(content), contentType='application/json')

if response.status == 200:
    print "* status %s" % response.status
    print "* response %s" % response.response

    data = json.loads(response.response)[0]
    deploymentId = data.get('id')
    deploymentDescription = data.get('description')
    deploymentResult = data.get('result')
    if not deploymentResult:
        print "Failed to create release in Nolio at %s." % nolioUrl
        print "Received description: {0}".format(deploymentDescription)
        response.errorDump()
        sys.exit(1)
    print "Created %s in Nolio at %s." % (deploymentId, nolioUrl)
else:
    print "Failed to create release in Nolio at %s." % nolioUrl
    response.errorDump()
    sys.exit(1)
