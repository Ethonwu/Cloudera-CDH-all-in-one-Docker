#! /usr/bin/env python

#   Copyright 2014-2015 Cloudera, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# This require python-argparse on CentOS 6

import argparse
import base64
import getpass
import httplib
import json
import logging
import re
import sys
import time
import urllib

logger = logging.getLogger('cm_api')
hdlr = logging.FileHandler('/var/tmp/cm_api.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class cm_api():
    methods = ['POST', 'GET', 'PUT', 'DELETE']
    poll_limit = 300
    poll_delay = 7
    result = {}
    headers = {'Content-type': 'application/json'}
    endpoint = None
    method = 'GET'
    body = ''
    commands_resources = [
        re.compile('^/clusters/[^/]+/services/[^/]+/roles/[^/]+/commands'),
        re.compile('^/clusters/[^/]+/services/[^/]+/commands'),
        re.compile('^/clusters/[^/]+/commands'),
        re.compile('^/cm/service/roles/[^/]+/commands'),
        re.compile('^/cm/service/commands'),
        re.compile('^/cm/commands')
    ]
    def __init__(self, endpoint=None, method='GET', body='', host='localhost', port=7180, username='admin', password='admin', api_version=10, https=False, asynchronous=False):
        self.host = host
        self.port = port
        self.body = body
        self.https = https
        self.asynchronous = asynchronous
        self.headers['Authorization'] = 'Basic ' + base64.b64encode(username + ':' + password)
        self.method = method.upper()
        if not method in cm_api.methods:
            raise Exception('Illegal method: ' + method)
        self.base_resource = '/api/v' + str(api_version)
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        self.endpoint = urllib.quote(endpoint)
    def execute(self):
        commands_resource = self.get_commands_resource()
        logger.info(self.method + '-ing ' + self.endpoint + ', with body:')
        logger.info(self.body)
        response = self.request(self.method, self.endpoint, self.body)
        logger.info('Response: ' + str(response))
        if commands_resource in [None, self.endpoint]:
            return response
        else:
            job_ids = []
            if 'id' in response:
                job_ids.append(response['id'])
            elif 'items' in response: # TODO See what variations are possible
                for item in response['items']:
                    job_ids.append(item['id'])
            logger.info('Tracking IDs: ' + str(job_ids))
            if self.asynchronous:
                return job_ids
            else:
                sys.stderr.write('Submitted jobs: ' + ', '.join([str(job_id) for job_id in job_ids]) + '\n')
                return self.poll(job_ids, commands_resource)
    def get_commands_resource(self):
        for resource in self.commands_resources:
            matched = resource.match(self.endpoint)
            if matched:
                return matched.group()
        return None
    def request(self, method, resource, body = ''):
        http_connection_class = httplib.HTTPSConnection if self.https else httplib.HTTPConnection
        connection = http_connection_class(self.host, self.port)
        connection.request(method, self.base_resource + resource, body, self.headers)
        response = connection.getresponse()
        if not (response.status in [200, 204, 400]):
            raise Exception('HTTP ' + str(response.status) + ' ' + response.reason)
        response_body = response.read()
        content_type = response.getheader('Content-Type')
        connection.close()
        if content_type == 'application/json':
            response_json = json.loads(response_body)
            return response_json
        return response_body
    def poll (self, job_ids, commands_resource):
        poll_count = 0
        final_results = dict((job_id, 'unknown') for job_id in job_ids)
        while poll_count < self.poll_limit and len(job_ids) > 0:
            logger.info('Polling...')
            response = self.request('GET', commands_resource)
            inter_results = {}
            for item in response['items']:
                inter_results[item['id']] = item
            for job_id in job_ids:
                if not job_id in inter_results:
                    logger.info(str(job_id) + ' ended')
                    final_results[job_id] = 'finished'
                    del job_ids[job_ids.index(job_id)]
                elif 'success' in inter_results[job_id]:
                    logger.info(str(job_id) + ' succeeded')
                    final_results[job_id] = 'success'
                    del job_ids[job_ids.index(job_id)]
                elif inter_results[job_id]['active']:
                    final_results[job_id] = 'active'
                else:
                    logger.info(str(job_id) + ': ' + item['resultMessage'])
                    final_results[job_id] = item['resultMessage'] # TODO can there be sub-commands?
            time.sleep(self.poll_delay)
            poll_count = poll_count + 1
        if poll_count >= self.poll_limit:
            for item in final_results:
                if not item in ['finished', 'success']:
                    item = 'timed out'
        return final_results

class cm_live():
    retry_delay = 5
    retry_limit = 120
    args = None
    def __init__(self, args):
        self.args = args
    def get(self, endpoint):
        self.args['endpoint'] = endpoint
        return cm_api(**(self.args)).execute()
    def post(self, endpoint, body=''):
        self.args['endpoint'] = endpoint
        self.args['body'] = body
        self.args['method'] = 'POST'
        return cm_api(**(self.args)).execute()
    def put(self, endpoint, body=''):
        self.args['endpoint'] = endpoint
        self.args['body'] = body
        self.args['method'] = 'PUT'
        return cm_api(**(self.args)).execute()
    def trial(self):
        license = None
        try:
            license = self.get('cm/license')
        except Exception, e:
            # If we 404, that means no license is installed yet
            license = None
        if license == None or not 'uuid' in license:
            self.post('cm/trial/begin')
    def deployment(self):
        old_deployment = self.get('cm/deployment')
        if len(old_deployment['clusters']) > 0:
            return
        new_deployment_json = sys.stdin.read()
        self.put('cm/deployment', new_deployment_json)
    def echo(self):
        i = 0;
        while i < self.retry_limit:
            try:
                back = self.get('tools/echo')
                if back['message'] == 'Hello, World!':
                    return
            except Exception, e:
                if str(e) == 'HTTP 401 Bad credentials':
                    raise
                pass
            i = i + 1
            time.sleep(self.retry_delay)

def main():
    parser = argparse.ArgumentParser(description='Cloudera Manager API CLI client')
    parser.add_argument('--host',         action='store',      dest='host',        default='localhost', help='Cloudera Manager server host (default: localhost)')
    parser.add_argument('--port',         action='store',      dest='port',        default=7180,        help='Cloudera Manager server port (default: 7180)', type=int)
    parser.add_argument('--username',     action='store',      dest='username',    default='admin',     help='Username (default: admin)')
    parser.add_argument('--password',     action='store',      dest='password',    default='admin',     help='Password (default: admin)')
    parser.add_argument('--method',       action='store',      dest='method',      default='GET',       help='HTTP method to use (default: GET)', choices=cm_api.methods)
    parser.add_argument('--body',         action='store',      dest='body',        default='',          help='Request body, or stdin (default: None)')
    parser.add_argument('--api-version',  action='store',      dest='api_version', default='10',        help='API version to use (default: 10)')
    parser.add_argument('--https',        action='store_true', dest='https',                            help='Use HTTPS for connection to Cloudera Manager')
    parser.add_argument('--asynchronous', action='store_true', dest='asynchronous',                     help='Return immediately for asynchronous actions')
    parser.add_argument('endpoint', help='API endpoint (see documentation for possibilities) or "live-[trial|deployment|echo]')
    args = vars(parser.parse_args())

    if args['endpoint'] in ['live-trial', 'live-deployment', 'live-echo']:
        try:
            live = cm_live(args)
            if args['endpoint'] == 'live-trial':
                live.trial()
            elif args['endpoint'] == 'live-deployment':
                live.deployment()
            elif args['endpoint'] == 'live-echo':
                live.echo()
        except Exception, e:
            print(e)
            sys.exit(1)
        sys.exit(0)

    if args['body'] == 'stdin':
        args['body'] = sys.stdin.read()
    try:
        result = cm_api(**args).execute()
        if type(result).__name__ in ['dict', 'list']:
            print(json.dumps(result, indent=4))
        else:
            sys.stdout.write(result)
    except Exception, e:
        print(e)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()

