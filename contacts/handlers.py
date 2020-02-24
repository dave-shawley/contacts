import dataclasses
import json
import uuid

import problemdetails
from sprockets.mixins.mediatype import content
from tornado import web

import contacts.app


class StatusHandler(web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(
            json.dumps({
                'service': __package__,
                'version': contacts.version,
            }).encode('utf-8'))


class ContactHandler(problemdetails.ErrorWriter, content.ContentMixin,
                     web.RequestHandler):
    application: 'contacts.app.Application'

    async def get(self, contact_id):
        try:
            contact_id = uuid.UUID(contact_id)
        except ValueError:
            contact_id = uuid.UUID(int=0)

        contact = await self.application.database.get_contact_by_id(contact_id)
        if contact is None:
            raise problemdetails.Problem(status_code=404,
                                         title='Contact does not exist',
                                         instance=self.request.path)
        self.set_status(200)
        self.send_response(dataclasses.asdict(contact))

    async def post(self):
        body = self.get_request_body()
        try:
            name = body['name']
            display = body.get('display', None)
            email = body.get('email', None)
            company = body.get('company', None)
        except KeyError as error:
            self.set_status(422)
            raise problemdetails.Problem(
                status_code=422,
                title='Body is missing required parameters',
                detail=f'{error.args[0]} is required')

        contact = await self.application.database.create_contact(
            name, display, email, company)
        self.set_header(
            'Location',
            self.reverse_url('contact-handler', str(contact.contact_id)))
        self.set_status(303)
