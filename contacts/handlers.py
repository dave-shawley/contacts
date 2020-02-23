import dataclasses
import json
import uuid

from tornado import web
from sprockets.mixins.mediatype import content

import contacts.app


class StatusHandler(web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(
            json.dumps({
                'service': __package__,
                'version': contacts.version,
            }).encode('utf-8'))


class ContactHandler(content.ContentMixin, web.RequestHandler):
    application: 'contacts.app.Application'

    async def get(self, contact_id):
        contact = await self.application.database.get_contact_by_id(
            uuid.UUID(contact_id))
        self.set_status(200)
        self.send_response(dataclasses.asdict(contact))

    async def post(self):
        body = self.get_request_body()
        contact = await self.application.database.create_contact(
            body['name'], body.get('display', None), body.get('email', None),
            body.get('company', None))
        self.set_header(
            'Location',
            self.reverse_url('contact-handler', str(contact.contact_id)))
        self.set_status(303)
