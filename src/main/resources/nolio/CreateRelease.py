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

content = """
{"environment":"%s","template":"%s","release":"%s","application":"%s","version":"%s","doStepsValidation":"%s","releaseType":"%s"}
""" % (environmentName, templateName, releaseName, applicationName, version, str(doStepsValidation).lower(), releaseType)


print "Sending content %s" % content

nolioAPIUrl = nolioUrl + '/datamanagement/a/api/create-release'

nolioResponse = XLRequest(nolioAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

if nolioResponse.status == RELEASE_CREATED_STATUS:
    data = json.loads(nolioResponse.read())
    releaseId = data.get('id')
    releaseDescrition = data.get('description')
    releaseResult = data.get('result')
    if releaseResult == False:
        print "Failed to create release in Nolio at %s." % nolioUrl
        nolioResponse.errorDump()
        sys.exit(1)
    print "Created %s in Nolio at %s." % (releaseId, nolioUrl)
else:
    print "Failed to create release in Nolio at %s." % nolioUrl
    nolioResponse.errorDump()
    sys.exit(1)

