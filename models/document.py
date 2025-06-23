from models.db import db
from datetime import datetime, timezone

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    date_modified = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Document %r>' % self.id
