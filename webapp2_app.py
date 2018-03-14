#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from apispec import APISpec
import webapp2
from webapp2 import Route, RequestHandler
from webapp2_extras.routes import PathPrefixRoute

# Create an APISpec
spec = APISpec(
    title=b'Swagger Petstore',
    version=b'1.0.0',
    plugins=[
        b'webapp2_plugin',
    ],
)


class DeleteHandler(RequestHandler):
    def get(self):
        """Get delete page.
        ---
        description: Get delete page
        responses:
            200:
                description: A greeting to the client
                schema:
                    $ref: '#/definitions/Greeting'
        """
        logging.debug("============= /delete ==============")
        if 'localhost' not in self.request.host:
            self.redirect('/test')
            return
        self.redirect('/test')


class MainHandler(RequestHandler):
    def get(self):
        """Get a greeting endpoint.
        ---
        description: Get a greeting
        responses:
            200:
                description: A greeting to the client
                schema:
                    $ref: '#/definitions/Greeting'
        """
        logging.debug("============= / ==============")
        self.response.write('test')


class HelloHandler(RequestHandler):
    def get(self):
        """Get a greeting endpoint.
        ---
        description: Get a greeting
        responses:
            200:
                description: A greeting to the client
                schema:
                    $ref: '#/definitions/Greeting'
        """
        self.response.write("hello")


webapp2_config = {
    'webapp2_extras.sessions': {
        'secret_key': 'test',
        'session_max_age': 60 * 60 * 24 * 30,
    }
}

app = webapp2.WSGIApplication([
    ('/delete', DeleteHandler),
    # api v1
    PathPrefixRoute('/v1', [
        Route('/main', MainHandler),
    ]),
], debug=True, config=webapp2_config)


spec.add_path(route=('/hello', HelloHandler))
