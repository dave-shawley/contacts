import asyncio
import contextlib
import dataclasses
import logging
import typing
import uuid

import aiopg
import psycopg2.extras


@dataclasses.dataclass
class Contact:
    contact_id: uuid.UUID
    display: str
    name: typing.List[str]
    primary_email: str = None
    company: str = None


class Database:
    def __init__(self, dsn):
        self.logger = logging.getLogger(__package__).getChild('Database')
        self._dsn = dsn
        self._connected = asyncio.Event()
        self._pool = None

    @property
    def connected(self):
        return self._connected.is_set()

    async def connect(self):
        if self._pool is None:
            self.logger.info('creating pool for %s', self._dsn)
            self._pool = aiopg.Pool(
                self._dsn,
                minsize=2,
                maxsize=10,
                timeout=0.5,
                enable_hstore=True,
                enable_json=True,
                enable_uuid=True,
                pool_recycle=-1,
                echo=False,
                on_connect=None,
                connection_factory=psycopg2.extras.RealDictConnection)
        async with self._pool.acquire():
            self.logger.info('database connected')
            self._connected.set()

    async def close(self):
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
        self._connected.clear()

    async def create_contact(self,
                             name: typing.List[str],
                             display: str = None,
                             primary_email: str = None,
                             company: str = None) -> Contact:
        display = display or ' '.join(p.strip() for p in name)
        new_contact = Contact(contact_id=uuid.uuid4(),
                              display=display,
                              name=name,
                              primary_email=primary_email,
                              company=company)

        async with self._get_cursor() as cursor:
            await self._execute(
                cursor,
                'INSERT INTO public.contacts(id, display, name, primary_email,'
                '                            company)'
                '     VALUES (%(id)s, %(display)s, %(name)s, %(email)s,'
                '             %(company)s)',
                company=new_contact.company,
                display=new_contact.display,
                email=new_contact.primary_email,
                id=new_contact.contact_id,
                name=new_contact.name,
            )

        return new_contact

    async def get_contact_by_id(
            self, contact_id: uuid.UUID) -> typing.Union[Contact, None]:
        async with self._get_cursor() as cursor:
            row = await self._fetch_one(
                cursor,
                'SELECT id AS contact_id, company, display, name,'
                '       primary_email'
                '  FROM public.contacts'
                ' WHERE id = %(contact_id)s',
                contact_id=contact_id,
            )
        return Contact(**row) if row else None

    @contextlib.asynccontextmanager
    async def _get_cursor(self) -> aiopg.Cursor:
        try:
            await self.connect()
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    yield cursor
        except psycopg2.Error as error:
            self.logger.error('database failure: %s', error)
            self.logger.warning('disconnecting from database')
            await self.close()
            raise error

    async def _execute(self, cursor: aiopg.Cursor, sql: str, **params):
        await cursor.execute(sql, parameters=params)

    async def _fetch_one(self, cursor: aiopg.Cursor, sql: str,
                         **params) -> dict:
        await self._execute(cursor, sql, **params)
        return await cursor.fetchone()
