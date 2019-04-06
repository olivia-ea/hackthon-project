"""Models and databases"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id}>'x


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
    print('Connected to DB.')