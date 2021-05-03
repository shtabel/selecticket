from  datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app_init import db

import const

class Ticket(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastchange = db.Column(db.DateTime)
    theme = db.Column(db.String(const.THEME_SIZE), nullable=False)
    text = db.Column(db.String)
    email = db.Column(db.String(const.EMAIL_SIZE))
    status = db.Column(db.Integer, nullable=False, default=const.TICKET_STATUS_OPENED)


def create(params: dict):
    '''
    params:
        id: uuid
        theme: text
        email: text
    '''
    #TODO: create a logic!
    pass


def status_update(params: dict):
    # TODO: create a logic!
    pass


def read(ticket_id: uuid):
    # TODO: create a logic!
    pass