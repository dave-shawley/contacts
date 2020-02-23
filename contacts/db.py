import dataclasses
import typing
import uuid


@dataclasses.dataclass
class Contact:
    contact_id: uuid.UUID
    display: str
    name: typing.List[str]
    primary_email: str = None
    company: str = None


contacts: typing.MutableMapping[uuid.UUID, Contact] = {}


class Database:
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
        contacts[new_contact.contact_id] = new_contact
        return new_contact

    async def get_contact_by_id(
            self, contact_id: uuid.UUID) -> typing.Union[Contact, None]:
        return contacts[contact_id]
