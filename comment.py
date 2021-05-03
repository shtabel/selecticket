from  datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app_init import db
import const


class Ticket(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent = db.Column(UUID(as_uuid=True))
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(const.EMAIL_SIZE))
    text = db.Column(db.String)

def create(object):
    #TODO: create a logic!
    pass
