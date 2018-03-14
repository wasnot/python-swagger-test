#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from apispec import APISpec
from bottle import route, default_app


# Create an APISpec
spec = APISpec(
    title=b'Swagger Petstore',
    version=b'1.0.0',
    plugins=[
        b'apispec.ext.bottle',
    ],
)

app = default_app()


@route('/gists/<gist_id>')
def gist_detail(gist_id):
    """Gist detail view.
    ---
    get:
        responses:
            200:
                schema:
                    $ref: '#/definitions/Gist'
    """
    return 'detail for gist {}'.format(gist_id)

# app.test_request_context().push()
spec.add_path(view=gist_detail)
