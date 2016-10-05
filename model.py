"""Models and database functions for Slack-Tac-Toe"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################

class UserMove(db.Model):
    """User and user's move for current game"""

    __tablename__ = "user_move"

    user__move_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    move = db.Column(db.Integer, unique=True, nullable=False)

    @classmethod
    def move_made(cls, move):
        """Querying db to see if move already made"""

        if cls.query.filter(cls.move == move).first() is not None:
            return True
        return False

    @classmethod
    def game_on(cls):
        """Querying db to see if game in progress"""

        if cls.query.first() is not None:
            return True
        else:
            return False

    @classmethod
    def query_board(cls):
        board_array = []

        if cls.query.first() is not None:
            user_one_username = cls.query.first().username
        else:
            return False

        if cls.query.filter(cls.username != user_one_username).first() is not None:
            user_two_username = cls.query.filter(cls.username != user_one_username).first().username
        else:
            return False

        user_one_moves = cls.query.filter(cls.username == user_one_username).all()
        for each_move in user_one_moves:
            one_move = (each_move.move, 'X')
            board_array.append(one_move)

        user_two_moves = cls.query.filter(cls.username == user_two_username).all()
        for user_move in user_two_moves:
            single_move = (user_move.move, 'O')
            board_array.append(single_move)

        return board_array

    def __repr__(self):

        return "<user_move_id=%s username=%s move=%s>" % (self.user_move_id,
                                                        self.username,
                                                        self.move)

##############################################################################
def init_app():
    from flask import Flask
    from server import app

    connect_to_db(app)
    print "Connected to DB."

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///slack_tac_toe'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    #To utilize database interactively
    from flask import Flask
    from server import app

    connect_to_db(app)
    print "Connected to DB."