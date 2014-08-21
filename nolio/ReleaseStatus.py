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

nolioAPIUrl = nolioUrl + '/datamanagement/a/api/release-status'
releaseStatus = ""

while (releaseStatus == "" or releaseStatus != "Finished"):
    nolioResponse = XLRequest(nolioAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

    if nolioResponse.status == RELEASE_STATUS:
        data = json.loads(nolioResponse.read())
        releaseId = data.get('id')
        releaseStatus = data.get('status')
        releaseDescription = data.get('description')
        releaseResult = data.get('result')
        if releaseResult == False:
            print "Failed to check release status in Nolio at %s." % nolioUrl
            nolioResponse.errorDump()
            sys.exit(1)
        print "Checking %s in Nolio at %s." % (releaseId, nolioUrl)
    else:
        print "Failed to check release status in Nolio at %s." % nolioUrl
        nolioResponse.errorDump()
        sys.exit(1)
    time.sleep(10)    