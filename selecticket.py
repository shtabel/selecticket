from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    header = "<h1>Hell(n)o There!</h1>"
    body = "<div>While setting up environment for an test task for Selectel I've killed my server accidently, so this site is temporary dead (and ssl is dead too, so you can't view it via https).</div>"
    msg = f'{header}{body}'
    return msg

if __name__ == "__main__":
    app.run(host='0.0.0.0')
