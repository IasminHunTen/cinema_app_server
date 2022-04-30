from extra_modules import db


class UserDevices(db.Model):
    pk = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(64))
    device_serial_number = db.Column(db.String(64))

    def __init__(self, user_id, device_serial_number):
        self.user_id = user_id
        self.device_serial_number = device_serial_number

    def db_store(self):
        if self.query.\
                filter_by(user_id=self.user_id).\
                filter_by(device_serial_number=self.device_serial_number).\
                first() is not None:
            return
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, user_id, device_serial_number=None):
        device = cls.query.filter_by(user_id=user_id).filter_by(device_serial_number=device_serial_number).first()
        db.session.delete(device)
        db.session.commit()

    @classmethod
    def fetch_user_device(cls, user_id):
        return {
            'devices': [device.device_serial_number for device in cls.query.filter_by(user_id=user_id).all()]
        }

    @classmethod
    def on_user_delete(cls, user_id):
        for device in cls.query.filter_by(user_id=user_id).all():
            db.session.delete(device)
        db.session.commit()




