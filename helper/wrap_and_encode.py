from hashlib import md5


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
    password = salt+password
    return md5(password.encode('utf-8')).hexdigest()