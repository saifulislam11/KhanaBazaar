from cx_Oracle import connect
from django.db import connection

from helper.wrap_and_encode import wrap_with_in_single_quote, not_delivered_str, date_format_oracle


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


if __name__ == '__main__':
    # cursor = open_connection().cursor()
    # cursor.callproc('ORDER_PICKED', ['11111111111', '11111111111'])
    #cursor = open_connection().cursor()
    # cursor = sql.create_cursor()
    to_execute = 'SELECT * FROM "ORDER" WHERE DELIVERY_TIME = TO_DATE({time}, {format})'
    to_execute = to_execute.format(
        time=wrap_with_in_single_quote(not_delivered_str),
        format=wrap_with_in_single_quote(date_format_oracle)
    )
    print(to_execute)
# my_string = None
#
# # Create date object in given time format yyyy-mm-dd
# my_date = datetime.strptime('0001-01-01', "%Y-%m-%d")
#
# print(my_date.strftime("%d-%m-%Y %H:%M:%S"))
# print('Type: ', type(my_date))
# not_picked_date = datetime.strptime('0001-01-01', "%Y-%m-%d")
# not_picked_str = not_picked_date.strftime("%d-%m-%Y %H:%M:%S")
# print(not_picked_str)
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
