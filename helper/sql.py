from datetime import datetime

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


def execute(sql):
    """
    create a cursor
    executes the sql
    closes the cursor
    :param sql: sql to execute
    :return:
    """
    c = create_cursor()
    c.execute(sql)
    c.close()
    return


def commit():
    connection.commit()


def rollback():
    connection.rollback()


# if __name__ == '__main__':
#     my_string = None
#
#     # Create date object in given time format yyyy-mm-dd
#     my_date = datetime.strptime('0001-01-01', "%Y-%m-%d")
#
#     print(my_date)
#     print('Type: ', type(my_date))
#     cursor = open_connection().cursor()
#     to_execute = 'SELECT DELIVERY_TIME FROM "ORDER"'
#     cursor.execute(to_execute)
#     rows = cursor.fetchall()
#     for i in rows:
#         print(type(i))
#         for j in i:
#             print(j)
#             print(type(j))
#             now = datetime.now()
#             print(type(now))
#             order_time = now.strftime("%d-%m-%Y %H:%M:%S")
#             print(type(order_time))
#             print(order_time)
