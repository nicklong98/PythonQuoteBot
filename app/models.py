from datetime import datetime
from app import db


class Quote(db.Model):
    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    user_id = db.Column(db.BigInteger, index=True, nullable=False)
    reporter_id = db.Column(db.BigInteger, index=True, nullable=False)
    server_id = db.Column(db.BigInteger, index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body = db.Column(db.String)

    def __repr__(self):
        return '<quote {}>'.format(self.id)
