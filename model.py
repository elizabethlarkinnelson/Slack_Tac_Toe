"""Models and database functions for Slack-Tac-Toe"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################


class Game(db.Model):
    """Games in play, one per channel"""

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.channel_id'))

    channel = db.relationship('Channel', backref='channels')

    @classmethod
    def create_game(cls, channel_id, user1, user2):
        """Creates new game, users in db"""

        new_game = cls(channel_id=channel_id)

        db.session.add(new_game)
        db.session.commit()

        #Query db for newly created channel to game id, create users
        #attached to this params

        game = cls.query.filter(cls.channel_id == channel_id).first()

        User.create_user(game.game_id, user1)
        User.create_user(game.game_id, user2)

    @classmethod
    def get_game_id(cls, channel_id):

        game_info = cls.query.filter(cls.channel_id == channel_id).first()
        return game_info.game_id

    def __repr__(self):

        return "<game_id=%s channel_id=%s>" % (self.game_id, self.channel_id)


class Channel(db.Model):
    """Channels in play"""

    __tablename__ = "channels"

    channel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_name = db.Column(db.String(50), unique=True, nullable=False)
    user_one = db.Column(db.String(25), nullable=False)
    user_two = db.Column(db.String(25), nullable=False)

    @classmethod
    def link_game_channel(cls, channel, user1, user2):
        #First function to be called when creating a new game
        new_channel_game = cls(channel_name=channel, user_one=user1, user_two=user2)
        db.session.add(new_channel_game)
        db.session.commit()

        #Call create game function which:
        #1)Creates game to channel relationship
        #2)Creates a user profile in db for each user in game
        channel_db = cls.query.filter(cls.channel_name == channel).first()
        Game.create_game(channel_db.channel_id, user1, user2)

    @classmethod
    def query_channel_game(cls, channel):
        """Returns true if game in play, false if not"""

        if cls.query.filter(cls.channel_name == channel).first() is not None:
            return True
        else:
            return False

    @classmethod
    def get_channel_id(cls, channel):
        """Returns channel id"""
        channel_info = cls.query.filter(cls.channel_name == channel).first()
        return channel_info.channel_id

    def __repr__(self):

        return "<channel_id=%s, channel_name=%s, user_one=%s, user_two=%s" % (
            self.channel_id, self.channel_name, self.user_one, self.user_two)


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    user_name = db.Column(db.String(25), nullable=False)

    game = db.relationship('Game', backref='users')

    @classmethod
    def create_user(cls, game_id, user_name):
        new_user = cls(game_id=game_id, user_name=user_name)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def get_game_users(cls, game_id):
        game_users = cls.query.filter(cls.game_id == game_id).all()
        return game_users

    @classmethod
    def get_user_id(cls, user_name):
        user_info = cls.query.filter(cls.user_name == user_name).first()
        return user_info.user_id

    def __repr__(self):

        return "<user_id=%s, game_id=%s, user_name=%s>" % (
            self.user_id, self.game_id, self.user_name)


class Move(db.Model):

    __tablename__ = "moves"

    move_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    board_space = db.Column(db.Integer, nullable=False)
    character = db.Column(db.String(1), nullable=False)

    user = db.relationship('User', backref='moves')

    def __repr__(self):

        return "<move_id=%s, user_id=%s, board_space=%s, char=%s>" % (
            self.move_id, self.user_id, self.board_space, self.character)

    @classmethod
    def query_board_moves(cls, channel):
        channel_id = Channel.get_channel_id(channel)
        game_id = Game.get_game_id(channel_id)
        users = User.get_game_users(game_id)

        current_plays = []

        for user in users:
            if cls.query.filter(cls.user_id == user.user_id).first() is None:
                continue
            else:
                moves = cls.query.filter(cls.user_id == user.user_id).all()
                for move in moves:
                    current_plays.append((move.board_space, move.character))

        return current_plays

    @classmethod
    def move_made(cls, guess, channel):
        current_plays = cls.query_board_moves(channel)

        for play in current_plays:
            if play[0] == guess:
                return True
        else:
            return False

    @classmethod
    def board_full(cls, channel):
        channel_id = Channel.get_channel_id(channel)
        game_id = Game.get_game_id(channel_id)
        users = User.get_game_users(game_id)

        all_moves = []

        for user in users:
            moves = Move.query.filter(Move.user_id == user.user_id).all()
            for move in moves:
                all_moves.append(move.board_space)

        if sorted(all_moves) == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True

        return False

    @classmethod
    def create_user_character(cls, channel):
        channel_id = Channel.get_channel_id(channel)
        game_id = Game.get_game_id(channel_id)
        users = User.get_game_users(game_id)

        user_char = []

        for user in users:
            if cls.query.filter(cls.user_id == user.user_id).first() is not None:
                user_move = Move.query.filter(cls.user_id == user.user_id).first()
                user_char.append((user.user_id, user_move.character))

        if not user_char:
            user_char.append((users[0].user_id, 'X'))

        elif len(user_char) == 1:
            user_char.append((users[1].user_id, 'O'))

        return user_char

    @classmethod
    def create_move(cls, channel, user, board_space):

        user_characters = Move.create_user_character(channel)

        user_id = User.get_user_id(user)

        my_char = []

        for character in user_characters:
            if character[0] == user_id:
                my_char.append(character[1])

        new_move = cls(user_id=user_id, board_space=board_space, character=my_char[0])
        db.session.add(new_move)
        db.session.commit()

        return

    @classmethod
    def whose_turn(cls, channel):
        channel_id = Channel.get_channel_id(channel)
        game_id = Game.get_game_id(channel_id)
        users = User.get_game_users(game_id)

        user1_count = cls.query.filter(cls.user_id == users[0].user_id).count()
        user2_count = cls.query.filter(cls.user_id == users[1].user_id).count()

        if user1_count > user2_count:
            return users[1].user_name

        else:
            return users[0].user_name

    @classmethod
    def game_over(cls, channel, user):
        user_id = User.get_user_id(user)
        user_moves = cls.query.filter(cls.user_id == user_id).all()

        all_moves = []

        for move in user_moves:
            all_moves.append(move.board_space)

        moves = sorted(all_moves)

        if moves == ([1, 2, 3] or [1, 4, 7] or
                     [1, 5, 9] or [7, 8, 9] or
                     [4, 5, 6] or [3, 6, 9] or
                     [2, 5, 8] or [3, 5, 7]):
            return [True, Move.whose_turn(channel)]

        return [False]

    @classmethod
    def clear_game(cls, channel):
        channel_id = Channel.get_channel_id(channel)
        game_id = Game.get_game_id(channel_id)
        users = User.get_game_users(game_id)

        channel = Channel.query.get(channel_id)
        db.session.delete(channel)

        game = Game.query.get(game_id)
        db.session.delete(game)

        for user in users:
            user_id = user.user_id
            user_moves = Move.query.filter(Move.user_id == user_id).all()
            for move in user_moves:
                db.session.delete(move)
            old_user = User.query.get(user_id)
            db.session.delete(old_user)

        db.session.commit()

        return







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