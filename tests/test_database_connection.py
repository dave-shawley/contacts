import os
import unittest.mock
import uuid

import psycopg2.extras

from contacts import db


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.database = db.Database(os.environ['DATABASE_URL'])
        self.conn = psycopg2.connect(
            os.environ['DATABASE_URL'],
            connection_factory=psycopg2.extras.RealDictConnection)
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM public.contacts')
            cursor.execute('DELETE FROM public.identifiers')
            cursor.execute('DELETE FROM public.street_addresses')

    async def asyncTearDown(self):
        self.conn.close()
        await self.database.close()
        await super().asyncTearDown()

    async def test_database_connect(self):
        self.assertFalse(self.database.connected)
        await self.database.connect()
        self.assertTrue(self.database.connected)

    async def test_minimal_contact_creation(self):
        contact = await self.database.create_contact(['jane', 'doe'])
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM public.contacts WHERE id = %s',
                           [contact.contact_id])
            row = cursor.fetchone()
            self.assertEqual(row['id'], contact.contact_id)
            self.assertIsNone(row['company'])
            self.assertEqual('jane doe', row['display'])
            self.assertEqual(['jane', 'doe'], row['name'])
            self.assertIsNone(row['primary_email'])

    async def test_lookup_contact_by_id(self):
        created_contact = await self.database.create_contact(
            ['jane', 'doe'],
            display='Jane Doe',
            primary_email='jdoe@example.com',
            company='Spaceley Space Sprockets')
        fetched_contact = await self.database.get_contact_by_id(
            created_contact.contact_id)
        self.assertEqual(created_contact, fetched_contact)

    async def test_lookup_of_nonexistent_contact(self):
        fetched = await self.database.get_contact_by_id(uuid.uuid4())
        self.assertIsNone(fetched)

    async def test_database_connection_failure_recovery(self):
        await self.database.connect()
        with unittest.mock.patch.object(
                self.database._pool,
                '_acquire',
                new_callable=unittest.mock.AsyncMock) as m:
            m.side_effect = psycopg2.Error('injected failure')
            with self.assertRaises(psycopg2.Error):
                await self.database.create_contact(['jane', 'doe'])
            self.assertFalse(self.database.connected)
        await self.database.create_contact(['jane', 'doe'])
