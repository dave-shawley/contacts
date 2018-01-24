from tornado import web

import contacts.handlers


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        handlers = [
            web.url('/status', contacts.handlers.StatusHandler),
        ]
        super(Application, self).__init__(handlers, *args, **kwargs)
