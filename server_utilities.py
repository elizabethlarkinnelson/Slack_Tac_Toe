import os
from slackclient import SlackClient

SLACK_TOKEN_KEY = os.environ.get('SLACK_TOKEN_KEY')
slack_client = SlackClient(SLACK_TOKEN_KEY)

board = [1, 2, 3]


def display_board(board):
    """Board is an array of tuples e.g. (2, "O") """

    one = " "
    two = " "
    three = " "

    return ''' \n
    |''' + one + '''|''' + two + '''|''' + three + '''|
    |---+---+---|
    |---+---+---|
    '''
slack_board = display_board(board)



def send_message(channel_id, message):
            slack_client.api_call(
                "chat.postMessage",
                channel=channel_id,
                text=message,
                username='me'
                )
            return


# board = ''' \n
# | X | O | O |
# |---+---+---|
# | O | X | X |
# |---+---+---|
# | X | O | X |
# '''
