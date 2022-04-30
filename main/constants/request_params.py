auth_in_header = {
    'token': {
        'type': 'auth',
        'in': 'query',
        'name': 'Auth Token'
    }
}


def string_from_query(key):
    return {
        key: {
            'type': 'string',
            'in': 'query'
        }
    }

