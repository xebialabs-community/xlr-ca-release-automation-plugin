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

deploymentPlan = "{project}_{uniqueid}".format(project=project,
                                               uniqueid=datetime.datetime.fromtimestamp(time.time()).strftime(
                                                   '%Y-%m-%d_%H:%M:%S'))

content = {
    "application": application,
    "build": build,
    "deploymentPlan": deploymentPlan,
    "deploymentTemplate": deploymentTemplate,
    "project": project,
    "templateCategory": templateCategory,
    "manifest": manifest
}

print "* Sending content {0}".format(json.dumps(content))

context = '/datamanagement/a/api/{0}/create-deployment-plan'.format(nolioServer['version'])
print "* Context is {0}".format(context)

request = HttpRequest(nolioServer, username, password)
response = request.post(context, json.dumps(content), contentType='application/json')

if response.isSuccessful():
    print "* status {0}".format(response.status)
    print "* response {0}".format(response.response)

    json_response = json.loads(response.response)
    data = json_response
    result = data.get('result')
    if result == "false":
        description = data.get('description')
        print description
        print "Failed to create release in Nolio at %s." % nolioUrl
        response.errorDump()
        sys.exit(1)
    else:
        deploymentPlan = data.get('deploymentPlan')
        print "successfully create the deployment plan " + deploymentPlan
        deploymentPlanId = data.get('deploymentPlanId')
else:
    print "Failed to create release in Nolio at %s." % nolioUrl
    response.errorDump()
    sys.exit(1)
