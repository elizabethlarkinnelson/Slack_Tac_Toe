import os
from server_utilities import send_message, slack_board

from flask import Flask, request, Response, session

from model import connect_to_db, db, UserMove

app = Flask(__name__)

app.secret_key = "ABC"

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        text = request.form.get('text')
        channel = request.form.get('channel_name')

        if text == 'play':
            if UserMove.game_on() is True:
                send_message(channel, "There's a game in progress!")
                return Response(), 200
            else:
                confirm = "Tell me who you want to play!"
                send_message(channel, confirm)
        elif text == "board":
            if UserMove.query_board() is False:
                send_message(channel, "No game, or no challenger")
            else:
                board_array = UserMove.query_board()
                send_message(channel, slack_board)

    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")
