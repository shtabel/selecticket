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


class Comment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    ticket = db.relationship('Ticket', backref=db.backref('messages', lazy=True))
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(const.EMAIL_SIZE))
    text = db.Column(db.String, nullable=False)

db.create_all()