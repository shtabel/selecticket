import uuid
from flask import request
from app_init import app
import comment
import ticket
import utils

HTML_TEXT = '''
    <html>
    <head>
        <title>MadTentacle.com is down. Here is Selectel test task instead</title>
    </head>
    <body>{body}</body>
    </html>
'''

@app.route("/")
@app.route("/index")
def index():
    heading = "<h1>Hell(n)o There!</h1>"
    content = "<div>While setting up environment for an test task for Selectel I've killed my server accidently, so this site is temporary dead (and ssl is dead too, so you can't view it via https).</div>"
    body = f'{heading}{content}'
    html_text = HTML_TEXT.format(body = body)
    return html_text


# TICKET LOGIC
@app.route("/ticket/_create", methods = ['GET'])
def ticket_create():
    # gather params
    raw_params = {
        'id': request.args.get('id', uuid.uuid4()),
        'theme': request.args.get('theme'),
        'email': request.args.get('email')
    }
    # validate params
    try:
        utils.has_fields(raw_params, ('theme', 'email'))
        utils.validate_email(raw_params['email'])
        utils.check_uuid(raw_params['id'])
        return ticket.create(raw_params)
    except ValueError as exc:
        return utils.return_text(exc)


@app.route("/ticket/_update", methods = ['GET'])
def ticket_update():
    raw_params = {
        'id': request.args.get('id'),
        'status': request.args.get('status')
    }
    try:
        utils.has_fields(raw_params, ('id', 'status'))
        utils.check_uuid(raw_params['id'])
        return ticket.status_update(raw_params)
    except ValueError as exc:
        return utils.return_text(exc)


@app.route("/ticket/<ticket_id>}", methods = ['GET'])
def ticket_read(ticket_id):
    try:
        utils.check_uuid(ticket_id)
        ticket_dict = ticket.read(ticket_id)
        body = ''
        for key, val in ticket_dict.items():
            body += f'''<p><b>{key}</b>: {val}</p>'''
        body = f'<div>{body}</div>'
        html_text = HTML_TEXT.format(body = body)
        return html_text
    except ValueError as exc:
        return utils.return_text(exc)


# COMMENT LOGIC
@app.route("/comment/_create", methods = ['GET'])
def comment_create():
    raw_params = {
        'id': request.args.get('id'),
        'parent': request.args.get('parent'),
        'email': request.args.get('email'),
        'text': request.args.get('text')
    }
    try:
        utils.has_fields(raw_params, ('id', 'parent', 'text'))
        utils.validate_email(raw_params['email'])
        utils.check_uuid(raw_params['id'])
        utils.check_uuid(raw_params['parent'])
        return comment.create(raw_params)
    except ValueError as exc:
        return utils.return_text(exc)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
