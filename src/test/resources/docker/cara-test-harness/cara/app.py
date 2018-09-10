#!flask/bin/python
#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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