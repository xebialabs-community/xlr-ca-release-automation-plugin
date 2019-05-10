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

import sys
import json

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

context = '/datamanagement/a/api/{0}/deployment-state/{1}'.format(nolioServer['version'], deploymentId)
print "* Context is {0}".format(context)

request = HttpRequest(nolioServer, username, password)
response = request.get(context, contentType='application/json')

if not response.isSuccessful():
    print "* Failed to get the deployment state" % deploymentId
    response.errorDump()
    sys.exit(1)

data = json.loads(response.response)
deploymentState = data.get('deploymentState')
deploymentStateText = data.get('deploymentStateText')
deploymentResult = data.get('result')
print "* '{0}' / '{1}'".format(deploymentStateText, data.get('description'))

task.setStatusLine("Deployment '{0}': {1}".format(deploymentId, deploymentState))
if deploymentState == "Active":
    task.schedule("nolio/stateDeployment.py", 5)
elif deploymentState == "Succeeded":
    print "* DONE"
    sys.exit(0)
elif deploymentState == "Failed" or deploymentState == "Canceled":
    print "* Failure"
    sys.exit(1);
else:
    print "* Unmanaged state '{0}'".format(deploymentState)
    sys.exit(2)
