from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    quotes = db.relationship('Quote', backref='author', lazy='dynamic', primaryjoin="User.id == Quote.user_id")
    reported_quotes = db.relationship('Quote', backref='reporter', lazy='dynamic',
                                      primaryjoin="User.id == Quote.reporter_id")

    def __repr__(self):
        return '<user {}>'.format(self.username)


class Quote(db.Model):
    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    reporter_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body = db.Column(db.String)

    def __repr__(self):
        return '<quote {}>'.format(self.id)
