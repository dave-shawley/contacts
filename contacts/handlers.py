import json

from tornado import web

import contacts


class StatusHandler(web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(
            json.dumps({
                'service': __package__,
                'version': contacts.version,
            }).encode('utf-8'))
