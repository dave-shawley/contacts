import json
import uuid

from sprockets.http import testing
from tornado import httpclient

from contacts import app


class ContactCreationTests(testing.SprocketsHttpTestCase):
    def get_app(self):
        self.app = app.Application()
        return self.app

    def fetch(self,
              path,
              raise_error=False,
              **kwargs) -> httpclient.HTTPResponse:
        if 'json' in kwargs:
            kwargs['body'] = json.dumps(kwargs.pop('json'))
            headers = kwargs.pop('headers', {})
            headers['Content-Type'] = 'application/json'
            kwargs['headers'] = headers
        return super().fetch(path, raise_error=raise_error, **kwargs)

    def test_simple_contact_creation(self):
        response = self.fetch('/contacts',
                              method='POST',
                              json={'name': ['john', 'doe']},
                              headers={'Accept': 'application/json'},
                              follow_redirects=False)
        self.assertEqual(303, response.code)

        response = self.fetch(response.headers['Location'])
        self.assertEqual(200, response.code)
        self.assertEqual('application/json; charset="utf-8"',
                         response.headers['Content-Type'])

        body = json.loads(response.body.decode('utf-8'))
        self.assertIsNone(body['company'])
        self.assertEqual('john doe', body['display'])
        self.assertListEqual(['john', 'doe'], body['name'])
        self.assertIsNone(body['primary_email'])

    def test_that_unhandled_content_type_results_in_415(self):
        response = self.fetch('/contacts',
                              method='POST',
                              body='<?xml version="1.0"?><contact/>',
                              headers={'Content-Type': 'application/xml'})
        self.assertEqual(415, response.code)

    def test_that_unparseable_json_results_in_400(self):
        response = self.fetch('/contacts',
                              method='POST',
                              body='{]',
                              headers={'Content-Type': 'application/json'})
        self.assertEqual(400, response.code)

    def test_that_missing_name_results_in_422(self):
        response = self.fetch('/contacts',
                              method='POST',
                              json={
                                  'display': 'whatever',
                                  'email': 'me@example.com'
                              })
        self.assertEqual(422, response.code)
        self.assertEqual('application/problem+json',
                         response.headers['Content-Type'])
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual('Body is missing required parameters', body['title'])
        self.assertEqual('name is required', body['detail'])

    def test_that_endpoint_503s_when_not_ready_to_serve(self):
        self.app.ready_to_serve.clear()
        response = self.fetch('/contacts',
                              method='POST',
                              json={
                                  'name': [],
                                  'email': 'me@example.com',
                              })
        self.assertEqual(response.code, 503)


class ContactRetrievalTests(testing.SprocketsHttpTestCase):
    def get_app(self):
        self.app = app.Application()
        return self.app

    def test_that_random_id_returns_not_found(self):
        contact_id = str(uuid.uuid4())
        response = self.fetch(f'/contacts/{contact_id}')
        self.assertEqual(404, response.code)
        self.assertEqual('application/problem+json',
                         response.headers['Content-Type'])
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual('Contact does not exist', body['title'])
        self.assertEqual(f'/contacts/{contact_id}', body['instance'])

    def test_that_non_uuid_id_returns_not_found(self):
        response = self.fetch('/contacts/12345')
        self.assertEqual(404, response.code)

    def test_that_endpoint_503s_when_not_ready_to_serve(self):
        self.app.ready_to_serve.clear()
        response = self.fetch('/contacts/12345')
        self.assertEqual(response.code, 503)
