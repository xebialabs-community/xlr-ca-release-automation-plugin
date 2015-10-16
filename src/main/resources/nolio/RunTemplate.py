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

# No properties (default)
content = """
{"environment":"%s","template":"%s","release":"%s","application":"%s","version":"%s","doStepsValidation":"%s","releaseType":"%s"}
""" % (environmentName, templateName, finalReleaseName, applicationName, version, str(doStepsValidation).lower(), releaseType)

# Properties have been defined.
if props:
    content = """{"environment":"%s","template":"%s","release":"%s","application":"%s","version":"%s","doStepsValidation":"%s","releaseType":"%s","properties":{%s}}
    """ % (environmentName, templateName, finalReleaseName, applicationName, version, str(doStepsValidation).lower(), releaseType, props)

print "Sending content %s" % content

nolioContext = '/datamanagement/a/api/run-template/'
httpRequest = HttpRequest(nolioServer, credentials['username'], credentials['password'])
nolioResponse = httpRequest.post(nolioContext, content, contentType = 'application/json')

if nolioResponse.status == RELEASE_CREATED_STATUS:
    data = json.loads(nolioResponse.getResponse())
    releaseId = data.get('id')
    releaseDescription = data.get('description')
    releaseResult = data.get('result')
    if releaseResult == False:
        print "Failed to run template in Nolio at %s." % nolioUrl
        print "Received description: %s" % releaseDescription
        nolioResponse.errorDump()
        sys.exit(1)
    print "Running template %s in Nolio at %s." % (releaseId, nolioUrl)
else:
    print "Failed to run template in Nolio at %s." % nolioUrl
    nolioResponse.errorDump()
    sys.exit(1)
