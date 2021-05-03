from sqlalchemy import desc
from datamodels import Comment, Ticket
from app_init import db
import utils


def create(params: dict):
    '''
        params:
            id: uuid
            theme: text
            text: text
            email: text
    '''
    params['ticket'] = Ticket.query.get(params['ticket'])
    comment = Comment(**params)
    db.session.add(comment)
    db.session.commit()
    # TODO: drop redis cache for that parent ticket
    return utils.return_text('Comment created')


def list(ticket):
    comments = Comment.query.filter_by(ticket=ticket).order_by(desc(Comment.datetime)).limit(100).all()
    result = []
    for comment in comments:
        result.append({
            'datetime': comment.datetime,
            'text': comment.text,
            'email': comment.email,
        })
    return result
