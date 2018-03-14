#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from apispec import APISpec
from tornado.web import RequestHandler

# Create an APISpec
spec = APISpec(
    title=b'Swagger Petstore',
    version=b'1.0.0',
    plugins=[
        b'apispec.ext.tornado',
    ],
)


class HelloHandler(RequestHandler):
    def get(self):
        '''Get a greeting endpoint.
        ---
        description: Get a greeting
        responses:
            200:
                description: A greeting to the client
                schema:
                    $ref: '#/definitions/Greeting'
        '''
        self.write("hello")

    def post(self):
        '''Post a greeting endpoint.
        ---
        description: Post a greeting
        responses:
            200:
                description: A greeting to the client
                schema:
                    $ref: '#/definitions/Greeting'
        '''
        self.write("hello")


urlspec = (r'/hello', HelloHandler)
spec.add_path(urlspec=urlspec)
