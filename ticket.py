import uuid
from app_init import db
from datamodels import Ticket
import const
import utils


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
    ticket = Ticket.query.filter_by(id = params[id])

    wanted_status = params['status']
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
            available = (const.STATUS_NAMES.get(x, 'unknown') for x in const.ALLOWED_TRANSITIONS[ticket.status])
            txt = utils.return_text(f'Available transitions for current status is: {available}')
        raise ValueError(txt)
    ticket.status = wanted_status
    db.session.commit()
    return utils.return_text('Status updated')


def read(ticket_id: uuid):
    ticket = Ticket.query.filter_by(id = ticket_id)
    result = {
        'id': ticket.id,
        'datetime': ticket.datetime,
        'lastchange': ticket.lastchange,
        'theme': ticket.theme,
        'text': ticket.text,
        'email': ticket.email,
        'status': const.STATUS_NAMES.get(ticket.status, 'unknown')
    }
    return result
