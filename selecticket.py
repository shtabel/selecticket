import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
import config
import const


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.get_db_uri()
db = SQLAlchemy(app)


@app.route("/")
@app.route("/index")
def index():
    heading = "<h1>Hell(n)o There!</h1>"
    content = "<div>While setting up environment for an test task for Selectel I've killed my server accidently, so this site is temporary dead (and ssl is dead too, so you can't view it via https).</div>"
    body = f'{heading}{content}'
    title = 'MadTentacle.com is down. Here is Selectel test task instead'
    html_text = f'''
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>{body}</body>
    </html>
    '''
    return html_text

@app.route("/ticket", methods = ['PUT'])
def ticket_create():
    # gather params
    raw_params = {
        'id': request.args.get('id', uuid.uuid4()),
        'theme': request.args.get('theme'),
        'email': request.args.get('email')
    }
    # validate params
    if not raw_params['theme']:
        raise ValueError()

    #TODO: validate email



if __name__ == "__main__":
    app.run(host='0.0.0.0')
