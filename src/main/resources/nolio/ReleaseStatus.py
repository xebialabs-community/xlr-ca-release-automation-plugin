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

while releaseStatus in ("Active", "Running", "Open", "") and (trial < numberOfTrials or numberOfTrials == 0):
    httpRequest = HttpRequest(nolioServer, credentials['username'], credentials['password'])
    nolioResponse = httpRequest.post(nolioContext, content, contentType = 'application/json')

    trial += 1

    print "Polling release status(%d)" % (trial)
    
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
        print "Checking %s in Nolio at %s." % (releaseId, nolioUrl)
        print "Description: %s" % (releaseDescription)
        
        print "Received data: releaseId:%s, releaseStatus:%s, releaseResult:%s, releaseDescription:%s" % (releaseId, releaseStatus, releaseResult, releaseDescription)

        if releaseResult == False:
            print "Failed to check release status in Nolio at %s." % nolioUrl
            print "Received description: %s" % releaseDescription
            nolioResponse.errorDump()
            sys.exit(1)
        if releaseStatus in ("Failed", "Canceled"):
            sys.exit(1)
        if releaseStatus in ("Succeeded", "Finished"):
            sys.exit(0)
    else:
        print "Invalid release status received in Nolio at %s." % nolioUrl
        nolioResponse.errorDump()
        sys.exit(1)
    time.sleep(pollingInterval)

# This means we reached max number of trials.
print "Exceeded maximum number of retries in Nolio at %s." % nolioUrl
sys.exit(1)