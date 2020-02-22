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
    sprockets.http.run(
        Application,
        log_config={
            'version': 1,
            'formatters': {
                'console': {
                    'datefmt': '%Y-%m-%dT%H:%M:%S',
                    'format': (
                        '%(asctime)s.%(msecs)03d %(levelname)10s - %(name)s: '
                        '%(message)s [pid=%(process)d]'),
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'console',
                    'stream': 'ext://sys.stdout',
                }
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        })
