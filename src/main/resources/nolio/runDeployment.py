#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import datetime
import json

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

content = {"deployment": "Run Deployment %s %s %s" % (
    application, environment, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')),
           "application": application,
           "environments": [environment],
           "deploymentPlan": deploymentPlan,
           "build": build,
           "project": project
           }

print "* Deployment is {0}".format(content['deployment'])
print "* Sending content {0}".format(json.dumps(content))

context = '/datamanagement/a/api/{0}/run-deployments'.format(nolioServer['version'])
print "* Context is {0}".format(context)

request = HttpRequest(nolioServer, username, password)
response = request.post(context, json.dumps(content), contentType='application/json')

if response.isSuccessful():
    print "* status {0}".format(response.status)
    print "* response {0}".format(response.response)

    data = json.loads(response.response)[0]

    deploymentId = data.get('id')
    deploymentDescription = data.get('description')
    deploymentResult = data.get('result')
    if not deploymentResult:
        print "Failed to create release in Nolio at %s." % nolioUrl
        print "Received description: {0}".format(deploymentDescription)
        response.errorDump()
        sys.exit(1)
    print "Created #%s in Nolio at %s." % (deploymentId, nolioUrl)
    task.setStatusLine("Deployment '{0}' : Started".format(deploymentId))
    task.schedule("nolio/stateDeployment.py", 5)
else:
    print "Failed to create release in Nolio at %s." % nolioUrl
    response.errorDump()
    sys.exit(1)
