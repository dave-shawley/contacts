from sprockets.http import testing

import contacts.app


class StatusEndpointTests(testing.SprocketsHttpTestCase):
    def get_app(self):
        self.app = contacts.app.Application()
        return self.app

    def test_that_status_endpoint_returns_ok(self):
        response = self.fetch('/status')
        self.assertEqual(response.code, 200)

    def test_that_endpoint_503s_when_not_ready_to_serve(self):
        self.app.ready_to_serve.clear()
        response = self.fetch('/status')
        self.assertEqual(response.code, 503)
