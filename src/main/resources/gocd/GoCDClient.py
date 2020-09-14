#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import json
import time

from gocd.HttpRequest import HttpRequest


def check_response(response, message):
    if not response.isSuccessful():
        raise Exception(message)


class GoCD_Client(object):
    def __init__(self, http_connection, username=None, password=None, verify=True):
        self.http_request = HttpRequest(http_connection, username, password, verify)

    @staticmethod
    def create_client(http_connection, username=None, password=None, verify=True):
        return GoCD_Client(http_connection, username, password, verify)
    
    def gocd_currentuser(self, variables):
        current_user_endpoint = "/current_user"
        current_user_repsonse = self.http_request.get(current_user_endpoint, contentType='application/vnd.go.cd.v1+json')
        check_response(current_user_repsonse,
                            "Failed to get system configuration properties. Server return [%s], with content [%s]" % (
                                current_user_repsonse.status, current_user_repsonse.response))
        result = json.loads(current_user_repsonse.getResponse())
        variables['currentUser'] = result
        return result

    def gocd_pipelinehistoy(self, variables):
        pipeline_histoy_endpoint = "/pipelines/{}/history".format(variables["pipelineName"])
        pipeline_histoy_repsonse = self.http_request.get(pipeline_histoy_endpoint, contentType='application/vnd.go.cd.v1+json')
        check_response(pipeline_histoy_repsonse,
                            "Failed to execute application process request. Server return [%s], with content [%s]" % (
                                pipeline_histoy_repsonse.status, pipeline_histoy_repsonse.response))
        result = json.loads(pipeline_histoy_repsonse.getResponse())
        variables['history'] = result
        return result
