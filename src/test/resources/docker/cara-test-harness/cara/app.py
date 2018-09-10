#!flask/bin/python
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from flask import Flask
from flask import request
from flask import make_response
import json

app = Flask(__name__)


def getFile(fileName):
    filePath = "/cara/responses/%s" % fileName
    F = open(filePath, "r")
    resp = make_response(F.read())
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/')
def index():
    app.logger.info('Slash...')
    return "Hello, CARA!"


@app.route('/datamanagement/a/api/<versionId>/run-deployments', methods=['POST'])
def runDeployment(versionId):
    app.logger.info('run deployment for %s' % versionId)
    data = request.data
    dataDict = json.loads(data)
    app.logger.info("dataDict %s" % dataDict)
    return getFile("runDeployment-1.json")


@app.route('/datamanagement/a/api/<versionId>//deployment-state/<deploymentId>', methods=['GET'])
def deploymentState(deploymentId):
    app.logger.info('state of deployment  %s' % deploymentId)
    return getFile("deploymentState-%s.json" % deploymentId)


if __name__ == '__main__':
    app.run(debug=True)
