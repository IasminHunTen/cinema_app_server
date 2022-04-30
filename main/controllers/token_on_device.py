from extra_modules import db


class TokenOnDevice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    device_id = db.Column(db.String(256))
    token = db.Column(db.String(256))

    def __init__(self, device_id, token):
        self.device_id = device_id
        self.token = token

    def db_store(self):
        td = self.query.filter_by(device_id=self.device_id).first()
        if td:
            td.token = self.token
        else:
            db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_token(cls, device_id):
        td = cls.query.filter_by(device_id=device_id).first()
        return td.token if td else None

    @classmethod
    def delete_token(cls, device_id):
        td = cls.query.filter_by(device_id=device_id).first()
        if td:
            db.session.delete(td)
