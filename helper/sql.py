from cx_Oracle import connect
from django.db import connection


def open_connection():
    """
    creates a connection
    :return: a connection object
    """
    con = connect("KB", "123", "localhost/orcl")
    return con


def create_cursor():
    """
    creates a new cursor using django's database engine
    :return: a cursor object
    """
    return connection.cursor()


def get_next_id():
    """

    :return: the next possible ID for our ID columns
    """
    con = open_connection()
    c = con.cursor()
    sql = 'Select ID_GENERATOR.NEXTVAL FROM DUAL'
    c.execute(sql)
    id = c.fetchone()
    id = str(id[0])
    con.close()
    # print(id)
    return str(id)


if __name__ == '__main__':
    email = 'vodro@khanabazaar.com'
    password = '77d9ec7c7b405cd2be7f2276dc500f5e'
    c = open_connection().cursor()
    sql = "Select * From ADMIN Where EMAIL = {email} " \
          "and PASSWORD_HASH = {password}"
    from helper.wrap_and_encode import wrap_with_in_single_quote
    sql = sql.format(
        email=wrap_with_in_single_quote(email),
        password=wrap_with_in_single_quote(password)
    )
    c.execute(sql)
    admin = c.fetchone()
    c.close()
    for r in admin:
        print(r)
    pass
