from flask_restx import fields

from extra_modules import api

get_user_devices_model = api.model('UserDeviceGetSchema', {
    'devices': fields.List(fields.String)
})



