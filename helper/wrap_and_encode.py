from datetime import datetime
from hashlib import md5

not_picked_date = datetime.strptime('0001-01-01', "%Y-%m-%d")
not_delivered_date = datetime.strptime('1000-01-01', "%Y-%m-%d")


def wrap_with_in_single_quote(s):
    """
    wraps a string within single qoute.
    Mostly needed for insert into database
    :param s: the string
    :return: the desired single quoted version
    """
    return "'{}'".format(s)


def get_hashed_value(password):
    """
    returns md5 hashed password
    :param password: the password
    :return: hashed value of password
    """
    salt = 'saifulBoss'
    password = salt + password
    return md5(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print(get_hashed_value('123'))
    pass
