from sprockets.http import testing

import contacts.app


class StatusEndpointTests(testing.SprocketsHttpTestCase):
    def get_app(self):
        self.app = contacts.app.Application()
        return self.app

    def test_that_status_endpoint_returns_ok(self):
        response = self.fetch('/status')
        self.assertEqual(response.code, 200)
