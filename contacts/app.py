import asyncio
import os

from tornado import web
import sprockets.http.app
from sprockets.mixins.mediatype import content, transcoders

import contacts.handlers
import contacts.db


class Application(sprockets.http.app.Application):
    database: contacts.db.Database

    def __init__(self, *args, **kwargs):
        handlers = [
            web.url('/contacts',
                    contacts.handlers.ContactHandler,
                    name='contacts-root'),
            web.url('/contacts/(?P<contact_id>.*)',
                    contacts.handlers.ContactHandler,
                    name='contact-handler'),
            web.url('/status', contacts.handlers.StatusHandler),
        ]
        super(Application, self).__init__(handlers, *args, **kwargs)

        content.install(self,
                        default_content_type='application/json',
                        encoding='utf-8')
        content.add_transcoder(self, transcoders.JSONTranscoder())

        self.database = None
        self.ready_to_serve = None

        self.before_run_callbacks.append(self.on_start)
        self.on_shutdown_callbacks.append(self.on_shutdown)

    def on_start(self, _ignored_app, _ignored_loop):
        self.ready_to_serve = asyncio.Event()
        self.database = contacts.db.Database(os.environ['DATABASE_URL'])
        self.ready_to_serve.set()

    async def on_shutdown(self, _ignored):
        await self.database.close()


def entry_point():
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
