# -*- coding: utf-8 -*-
"""Webapp2 plugin. Includes a path helper that allows you to pass an Route (path-handler pair)
object to `add_path`.
::

    from pprint import pprint

    from webapp2 import RequestHandler

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
            self.response.write("hello")

    route = (r'/hello', HelloHandler)
    spec.add_path(route=route)
    pprint(spec.to_dict()['paths'])
    # {'/hello': {'get': {'description': 'Get a greeting',
    #                     'responses': {200: {'description': 'A greeting to the '
    #                                                     'client',
    #                                         'schema': {'$ref': '#/definitions/Greeting'}}}}}}

"""
from __future__ import absolute_import
import inspect
import sys
from webapp2 import BaseRoute, Route, SimpleRoute
from types import FunctionType

from apispec import Path
from apispec import utils
from apispec.exceptions import APISpecError


def __extract_wrapped(decorated):
    """unwrap, decorated method"""
    if decorated is None or decorated.__closure__ is None:
        return decorated
    closure = (c.cell_contents for c in decorated.__closure__)
    return __extract_wrapped(next((c for c in closure if isinstance(c, FunctionType)), None))

def setup(spec):
    """Setup for the plugin."""
    spec.register_path_helper(path_from_route)

def path_from_route(spec, route, operations, **kwargs):
    """Path helper that allows passing a webapp2 Route or tuple."""
    if not isinstance(route, BaseRoute):
        route = Route(*route)
    if operations is None:
        operations = {}
        for operation in _operations_from_methods(route.handler):
            operations.update(operation)
    if not operations:
        raise APISpecError(
            'Could not find endpoint for route {0}'.format(route))
    params_method = getattr(route.handler, list(operations.keys())[0])
    path = webapp2_path_to_swagger(route, params_method)
    extensions = _extensions_from_handler(route.handler)
    operations.update(extensions)
    return Path(path=path, operations=operations)

def _operations_from_methods(handler_class):
    """Generator of operations described in handler's http methods

    :param handler_class:
    :type handler_class: RequestHandler descendant
    """
    for httpmethod in utils.PATH_KEYS:
        if not hasattr(handler_class, httpmethod):
            continue
        method = getattr(handler_class, httpmethod)
        operation_data = utils.load_yaml_from_docstring(method.__doc__)
        if operation_data:
            operation = {httpmethod: operation_data}
            yield operation

def webapp2_path_to_swagger(route, method):
    """Convert webapp2 Route to OpenAPI-compliant path.

    :param route:
    :type route: Route
    :param method: Handler http method
    :type method: function
    """
    method = __extract_wrapped(method)
    if sys.version_info >= (3, 3):
        args = [k for k, v in inspect.signature(method).parameters.items() if
                v.kind not in [v.VAR_KEYWORD, v.VAR_POSITIONAL]][1:]
    else:
        args = inspect.getargspec(method).args[1:]
    params = tuple('{{{}}}'.format(arg) for arg in args)
    if isinstance(route, SimpleRoute):
        path_tpl = route.template
    elif isinstance(route, Route):
        path_tpl = route.reverse_template
    path = (path_tpl % params)
    if path.count('/') > 1:
        path = path.rstrip('/?*')
    return path

def _extensions_from_handler(handler_class):
    """Returns extensions dict from handler docstring

    :param handler_class:
    :type handler_class: RequestHandler descendant
    """
    extensions = utils.load_yaml_from_docstring(handler_class.__doc__) or {}
    return extensions
