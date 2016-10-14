import os
from server_utilities import send_message, play_game

from flask import Flask, request, Response

from model import connect_to_db

# from app import print_users

app = Flask(__name__)

app.secret_key = "ABC"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABC")

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        text = request.form.get('text')
        split_text = text.split(" ")
        channel = request.form.get('channel_name')
        user = request.form.get('user_name')

        play_game(split_text, channel, user)

        # numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        # if text == "play":
        #     if UserMove.game_on() is True:
        #         send_message(channel, "There's a game in progress!")
        #         return Response(), 200
        #     else:
        #         confirm = "Tell me who you want to play!"
        #         send_message(channel, confirm)
        # elif text in print_users():
        #     UserMove.create_game(user, text)
        #     send_message(channel, "Game started, your move!")

        # elif text == "board":
        #     if UserMove.query_board() is False:
        #         send_message(channel, "No game, or no challenger")
        #     else:
        #         board_array = UserMove.query_board()
        #         send_message(channel, slack_board)

        # elif text in numbers:
        #     if UserMove.move_made(text) is True:
        #         send_message(channel, "Sorry that spot is taken")
        #     else:
        #         UserMove.create_move(user, text)
        #         send_message(channel, "cool")

        # else:
        #     send_message(channel, "Sorry not a valid response. Try again!")

    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":

    app.debug = True
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
