#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import#, unicode_literals

from apispec import APISpec
from flask import Flask, jsonify
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title=b'Swagger Petstore',
    version=b'1.0.0',
    plugins=[
        b'apispec.ext.flask',
        b'apispec.ext.marshmallow',
    ],
)


# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class PetSchema(Schema):
    category = fields.Nested(CategorySchema, many=True)
    name = fields.Str()


# Optional Flask support
app = Flask(__name__)


@app.route('/random')
def random_pet():
    """A cute furry animal endpoint.
    ---
    get:
        description: Get a random pet
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
    post:
        description: Get a random pet
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
    """
    cat = dict(id=1, name='cat')
    pet = dict(name='god', category=[cat])
    # pet = get_random_pet()
    return jsonify(PetSchema().dump(pet).data)


ctx = app.test_request_context()
ctx.push()

# Register entities and paths
spec.definition('Category', schema=CategorySchema)
spec.definition('Pet', schema=PetSchema)
spec.add_path(view=random_pet)
