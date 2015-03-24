#!/usr/bin/python
import BaseHTTPServer
import threading
import json

def to_json(request_info):
    assert request_info.get('content_type') == 'application/json'
    return json.loads(request_info['body'])


class MyHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.request_info = dict()
        self.server.request_info['path'] = self.path
        self.server.request_info['headers'] = self.headers.dict
        self.server.request_info['command'] = self.command

        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)

    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        content_type = self.headers.get('content-type', None)
        body = self.rfile.read(length)

        self.server.request_info = dict()
        self.server.request_info['content_type'] = content_type
        self.server.request_info['body'] = body
        self.server.request_info['path'] = self.path
        self.server.request_info['headers'] = self.headers.dict
        self.server.request_info['command'] = self.command


        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)


def detach(func):
    t = threading.Thread(target=func)
    t.start()

    return t

class MockServer(object):
    def __init__(self, port=8000):
        server_addr = ('', port)
        httpd = BaseHTTPServer.HTTPServer(server_addr, MyHTTPHandler)
        httpd.request_info = dict()
        self.httpd = httpd
        self.server_thread = None

    def handle_request(self, detached=True):
        if detached:
            self.server_thread = threading.Thread(target=self.httpd.handle_request)
            self.server_thread.start()
        else:
            self.httpd.handle_request()

    def server_forever(self, detached=True):
        if detached:
            self.server_thread = threading.Thread(target=self.httpd.serve_forever)
            self.server_thread.start()
        else:
            self.httpd.serve_forever()

    @property
    def request_info(self):
        return self.httpd.request_info
