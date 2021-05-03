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
        <style>
            table, th, td {{ border: 1px solid #cacaca;}}
            table {{ border-collapse: collapse; }}
            td {{ padding: 8px }}
        </style>
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
        'text': request.args.get('text'),
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


@app.route("/ticket/<ticket_id>", methods = ['GET'])
def ticket_read(ticket_id):
    try:
        utils.check_uuid(ticket_id)
        ticket_dict = ticket.read(ticket_id)

        if not ticket_dict.get('comments'):
            comment_block = '''<h3>No comments</h3>'''
        else:
            comments_rows = ''
            for comment_dict in ticket_dict['comments']:
                comments_rows += f'''                <tr>
                        <td>{comment_dict['datetime']}</td>
                        <td>{comment_dict['text']}</td>
                        <td>{comment_dict['email']}</td>
                    </tr>'''
            comment_block = f'''<h3>Comments</h3>
            <table>
                <tr>
                    <td><b>Created</b></td>
                    <td><b>Text</b></td>
                    <td><b>Email</b></td>
                </tr>
                {comments_rows}
            </table>
            '''

        body = f'''<div>
        <h2>Ticket</h2>
            <table>
                <tr>
                    <td><b>ID</b></td>
                    <td><b>Created</b></td>
                    <td><b>Changed</b></td>
                    <td><b>Theme</b></td>
                    <td><b>Text</b></td>
                    <td><b>Email</b></td>
                    <td><b>Status</b></td>
                </tr>
                <tr>
                    <td>{ticket_dict.get('id')}</td>
                    <td>{ticket_dict.get('datetime')}</td>
                    <td>{ticket_dict.get('lastchange')}</td>
                    <td>{ticket_dict.get('theme')}</td>
                    <td>{ticket_dict.get('text')}</td>
                    <td>{ticket_dict.get('email')}</td>
                    <td>{ticket_dict.get('status')}</td>
                </tr>
            </table>
            {comment_block}
        </div>'''
        html_text = HTML_TEXT.format(body = body)
        return html_text
    except ValueError as exc:
        return utils.return_text(exc)


@app.route("/tickets", methods = ['GET'])
def ticket_list():
    try:
        tickets = ticket.list()
        body = '''<div>
        <h2>Last 100 tickets</h2>
            <table>
                <tr>
                    <td><b>ID</b></td>
                    <td><b>Theme</b></td>
                    <td><b>Created</b></td>
                    <td><b>Changed</b></td>
                    <td><b>Email</b></td>
                    <td><b>Status</b></td>
                </tr>
                {ROWS}
            </table>
        </div>'''
        rows = ''
        for ticket_dict in tickets:
            rows += f'''                <tr>
                    <td><a href="/ticket/{ticket_dict['id']}">{ticket_dict['id']}</a></td>
                    <td>{ticket_dict['theme']}</td>
                    <td>{ticket_dict['datetime']}</td>
                    <td>{ticket_dict['lastchange']}</td>
                    <td>{ticket_dict['email']}</td>
                    <td>{ticket_dict['status']}</td>
                </tr>'''
        body = body.format(ROWS = rows)
        html_text = HTML_TEXT.format(body = body)
        return html_text
    except ValueError as exc:
        return utils.return_text(exc)


# COMMENT LOGIC
@app.route("/comment/_create", methods = ['GET'])
def comment_create():
    raw_params = {
        'id': request.args.get('id', uuid.uuid4()),
        'ticket': request.args.get('ticket'),
        'email': request.args.get('email'),
        'text': request.args.get('text')
    }
    try:
        utils.has_fields(raw_params, ('ticket', 'text'))
        utils.validate_email(raw_params['email'])
        utils.check_uuid(raw_params['id'])
        utils.check_uuid(raw_params['ticket'])
        return comment.create(raw_params)
    except ValueError as exc:
        return utils.return_text(exc)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
