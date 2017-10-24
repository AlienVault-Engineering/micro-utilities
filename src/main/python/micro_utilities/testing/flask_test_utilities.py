import random
import string

import os
from flask import Flask, Response as BaseResponse, json
from flask.testing import FlaskClient
from werkzeug.utils import cached_property

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class Response(BaseResponse):
    @cached_property
    def json(self):
        return json.loads(self.data)


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)


def configure_test_app(app):
    app.response_class = Response
    app.test_client_class = TestClient
    app.testing = True

