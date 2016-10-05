import os

from flask import Flask, request, Response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "ABC"

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        #USED FOR TESTING
        # channel = request.form.get('channel_name')
        # username = request.form.get('user_name')
        # text = request.form.get('text')
        # inbound_message = username + " in " + channel + " says: " + text
        # print inbound_message

        #CHALLENGE CODE:
        
    return Response(), 200

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
