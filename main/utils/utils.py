import uuid


def uuid_generator():
    return str(uuid.uuid4())


def str_inter(left, right):
    left_set = set(list(left))
    right_set = set(list(right))
    return len(left_set.intersection(right_set))


def doc_resp(resp):
    return resp[1], resp[0]['message']


def crop_sql_err(sql_err: str):
    idx = sql_err.rfind(':')
    sql_err = sql_err[idx + 1:]
    idx = sql_err.find('.')
    sql_err = sql_err[idx + 1:]
    return sql_err.split("'", 1)[0]


def debug_print(*args, **kwargs):
    print('\n###################################\n')
    print(*args)
    for (k, v) in kwargs:
        print(k, ': ', v)
    print('\n###################################\n')
