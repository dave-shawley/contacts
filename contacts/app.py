from tornado import web
import sprockets.http.app

import contacts.handlers


class Application(sprockets.http.app.Application):
    def __init__(self, *args, **kwargs):
        handlers = [
            web.url('/status', contacts.handlers.StatusHandler),
        ]
        super(Application, self).__init__(handlers, *args, **kwargs)


def main():
    sprockets.http.run(Application)
