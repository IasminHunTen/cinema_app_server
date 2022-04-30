import uuid
from datetime import date
from marshmallow import ValidationError
from random import choice
from string import digits


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


def dict_upside_down(d):
    rev_d = {}
    for k, v in d.items():
        if isinstance(v, (list, tuple, set)):
            for it in v:
                rev_d[it] = k
        else:
            rev_d[v] = k
    return rev_d


def dict_validator(data, constrains, min_keys=0):

    if len(data) < min_keys:
        raise ValidationError(f"Dictionary has to have at least {min_keys} keys-value pairs")
    for k, v in data.items():
        if k not in constrains:
            raise ValidationError(f"Unknown key '{k}'")
        valid = type(v) is constrains.get(k) if constrains.get(k) is not None else True
        if not valid:
            raise ValidationError(f"Value for '{k}' must to be of type '{constrains.get(k)}'")


def tuple_overlap(t1, t2):
    if t1[0] == t2[0]:
        return False
    return t1[0] < t2[0] if t1[1] < t2[0] else t2[1] < t1[0]


def minutes_2_time(a, b):
    def fun(minutes):
        return '{}:{}'.format(*divmod(minutes, 60))
    return f'{fun(a)}-{fun(b)}'


def date_from_string(date_str):
    return date(
        *tuple(
            map(int, date_str.split('-'))
        )
    )


def debug_print(*args, **kwargs):
    print('\n###################################\n')
    print(*args)
    for (k, v) in kwargs:
        print(k, ': ', v)
    print('\n###################################\n')


def generate_number_sequence(seq_len):
    return ''.join([choice(digits) for _ in range(seq_len)])


def config_range(config):
    def _f():
        s = config.split('-')
        return int(s[0]), int(s[1])+1

    return range(*_f())
