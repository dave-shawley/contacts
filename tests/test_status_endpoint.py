from tornado import testing

import contacts.app


class StatusEndpointTests(testing.AsyncHTTPTestCase):
    def get_app(self):
        return contacts.app.Application()

    def test_that_status_endpoint_returns_ok(self):
        response = self.fetch('/status')
        self.assertEqual(response.code, 200)
