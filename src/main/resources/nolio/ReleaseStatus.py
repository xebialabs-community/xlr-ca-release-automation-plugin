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
import com.xhaus.jyson.JysonCodec as json

RELEASE_STATUS = 200

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

credentials = CredentialsFallback(nolioServer, username, password).getCredentials()

content = """
{"releaseId":"%s"}
""" % (releaseId)

print "Sending content %s" % content

nolioContext = '/datamanagement/a/api/release-status/'
if version2:
    nolioContext = '/datamanagement/a/api/v2/release-status/'
releaseStatus = ""
trial = 0
if not numberOfTrials:
    numberOfTrials = 0
if not pollingInterval:
    pollingInterval = 60

while releaseStatus in ("Active", "Running", "Open", "Creating release: Running", "Creating release: Open", "") and (trial < numberOfTrials or numberOfTrials == 0):
    httpRequest = HttpRequest(nolioServer, credentials['username'], credentials['password'])
    nolioResponse = httpRequest.post(nolioContext, content, contentType = 'application/json')

    trial += 1

    print "- Polling release status(%d)" % (trial)

    if nolioResponse.status == RELEASE_STATUS:
    #   data = json.loads(nolioResponse.read())
        data = json.loads(nolioResponse.getResponse())
        releaseId = data.get('id')
        if version2:
            releaseStatus = data.get('releaseStatus')
        else:
            releaseStatus = data.get('status')
        releaseDescription = data.get('description')
        releaseResult = data.get('result')
        print "  - Checking %s in Nolio at %s." % (releaseId, nolioUrl)
        print "    - Description: %s" % (releaseDescription)
        print "    - Received data: releaseId:%s, releaseStatus:%s, releaseResult:%s, releaseDescription:%s" % (releaseId, releaseStatus, releaseResult, releaseDescription)

        if releaseResult == False:
            print "\nFailed to check release status in Nolio at %s." % nolioUrl
            print "\nReceived description: %s" % releaseDescription
            nolioResponse.errorDump()
            sys.exit(1)
        if releaseStatus in ("Failed", "Canceled"):
            sys.exit(1)
        if releaseStatus in ("Succeeded", "Finished"):
            sys.exit(0)
    else:
        print "\nInvalid release status received in Nolio at %s." % nolioUrl
        nolioResponse.errorDump()
        sys.exit(1)
    time.sleep(pollingInterval)

# This means we reached max number of trials.
print "\nExceeded maximum number of retries in Nolio at %s." % nolioUrl
sys.exit(1)