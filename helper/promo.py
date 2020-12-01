from helper.sql import open_connection
from helper.wrap_and_encode import wrap_with_in_single_quote


def promo_exists(promo_name):
    conn = open_connection()
    cursor = conn.cursor()
    to_execute = "SELECT COUNT(*) FROM PROMO WHERE NAME = {name}"
    to_execute = to_execute.format(
        name=wrap_with_in_single_quote(promo_name)
    )
    cursor.execute(to_execute)
    count = cursor.fetchone()

    # print(count)
    return count[0] != 0
