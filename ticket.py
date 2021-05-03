from datetime import datetime
import uuid
from sqlalchemy import desc
from app_init import db
from datamodels import Ticket
import const
import utils
import comment


def create(params: dict):
    '''
        params:
            id: uuid
            theme: text
            email: text
    '''
    ticket = Ticket(**params)
    db.session.add(ticket)
    db.session.commit()
    return utils.return_text('Ticket created')


def status_update(params: dict):
    '''
        params:
            id: uuid
            status: int
    '''
    ticket = Ticket.query.filter_by(id = params['id']).first()

    wanted_status = int(params['status'])
    status_ok = False
    if ticket.status in const.ALLOWED_TRANSITIONS and wanted_status in const.ALLOWED_TRANSITIONS[ticket.status]:
        status_ok = True

    if not status_ok:
        if ticket.status == const.TICKET_STATUS_CLOSED:
            txt = utils.return_text('Ticket is closed!')
        elif ticket.status not in const.AVAILABLE_STATUSES:
            txt = utils.return_text('Current status is not available, ticket is closed for changes!')
        elif ticket.status not in const.ALLOWED_TRANSITIONS:
            txt = utils.return_text('There is not known transitions for current status!')
        else:
            available = tuple(const.STATUS_NAMES.get(x, 'unknown') for x in const.ALLOWED_TRANSITIONS[ticket.status])
            txt = utils.return_text(f'Available transitions for current status is: {available}')
        raise ValueError(txt)
    ticket.status = wanted_status
    ticket.lastchange = datetime.utcnow()
    db.session.commit()
    # TODO: drop redis cache for that ticket and list
    return utils.return_text('Status updated')


def read(ticket_id: uuid):
    # TODO: return redis cache if existed
    ticket = Ticket.query.get(ticket_id)
    comments = comment.list(ticket)
    result = {
        'id': ticket.id,
        'datetime': ticket.datetime,
        'lastchange': ticket.lastchange,
        'theme': ticket.theme,
        'text': ticket.text,
        'email': ticket.email,
        'status': const.STATUS_NAMES.get(ticket.status, 'unknown'),
        'comments': comments
    }
    # TODO: write redis cache
    return result


def list():
    #TODO: return redis cache if existed
    tickets = Ticket.query.order_by(desc(Ticket.datetime)).limit(100).all()
    result = []
    for ticket in tickets:
        result.append({
            'id': ticket.id,
            'datetime': ticket.datetime,
            'lastchange': ticket.lastchange,
            'theme': ticket.theme,
            'text': ticket.text,
            'email': ticket.email,
            'status': const.STATUS_NAMES.get(ticket.status, 'unknown')
        })
    #TODO: write redis cache
    return result