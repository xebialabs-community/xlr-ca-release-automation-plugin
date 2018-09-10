#
# Copyright 2018 XEBIALABS
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
import com.xhaus.jyson.JysonCodec as json

RELEASE_CREATED_STATUS = 200

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

credentials = CredentialsFallback(nolioServer, username, password).getCredentials()

if appendTimestampToRelease:
    if releaseName is None: 
        finalReleaseName = time.strftime("%Y%m%d-%H%M%S")
    else:
        finalReleaseName = releaseName + " " + time.strftime("%Y%m%d-%H%M%S")
else:
    finalReleaseName = releaseName

content = """
{"environment":"%s","template":"%s","release":"%s","application":"%s","version":"%s","doStepsValidation":"%s","releaseType":"%s"}
""" % (environmentName, templateName, releaseName, applicationName, version, str(doStepsValidation).lower(), releaseType)

print "Sending content %s" % content

nolioContext = '/datamanagement/a/api/create-release/'
httpRequest = HttpRequest(nolioServer, credentials['username'], credentials['password'])
nolioResponse = httpRequest.post(nolioContext, content, contentType = 'application/json')

if nolioResponse.status == RELEASE_CREATED_STATUS:
    data = json.loads(nolioResponse.getResponse())
    releaseId = data.get('id')
    releaseDescrition = data.get('description')
    releaseResult = data.get('result')
    if releaseResult == False:
        print "Failed to create release in Nolio at %s." % nolioUrl
        print "Received description: %s" % releaseDescription
        nolioResponse.errorDump()
        sys.exit(1)
    print "Created %s in Nolio at %s." % (releaseId, nolioUrl)
else:
    print "Failed to create release in Nolio at %s." % nolioUrl
    nolioResponse.errorDump()
    sys.exit(1)

