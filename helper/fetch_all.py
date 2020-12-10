from helper import sql
from helper.wrap_and_encode import wrap_with_in_single_quote, not_picked_str, date_format_oracle, not_delivered_str


def food_item(food_id, rest_id):
    '''

    :param food_id: the food id of a food
    :return: a dictionary of necessary data of this food_item
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM FOOD_ITEM WHERE ID ={food_id} AND RESTAURANT_ID ={rest_id}"
    to_execute = to_execute.format(
        food_id=wrap_with_in_single_quote(food_id),
        rest_id=wrap_with_in_single_quote(rest_id)
    )
    cursor.execute(to_execute)
    row = cursor.fetchone()
    food = {}
    food['id'] = row[0]
    food['img_path'] = food_item_path(row[0])
    food['name'] = row[2]
    food['price'] = row[3]
    food['offer'] = row[4]
    food['availibility'] = row[5]
    food['description'] = row[6]
    food['type'] = row[7]
    cursor.close()
    return food


def food_item_all(rest_id):
    '''
    returns all food under a restaurant
    sorted according to type
    :param rest_id: the restaurant id
    :return: a list of dictionary of all food items
    '''
    # conn = sql.open_connection()
    # cursor = conn.cursor()
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM FOOD_ITEM WHERE RESTAURANT_ID ={id} ORDER BY TYPE"
    to_execute = to_execute.format(
        id=wrap_with_in_single_quote(rest_id)
    )
    cursor.execute(to_execute)
    f = cursor.fetchall()
    foods = []
    for row in f:
        food = {}
        food['id'] = row[0]
        food['img_path'] = food_item_path(row[0])
        food['name'] = row[2]
        food['price'] = row[3]
        food['offer'] = row[4]
        food['availibility'] = row[5]
        food['description'] = row[6]
        food['type'] = row[7]
        foods.append(food)
    cursor.close()
    return foods


def food_item_path(food_id):
    '''
    returns all food_item_path under a food id
    :param food_id: food_id
    :return: a list of food_item_path
    '''
    # conn = sql.open_connection()
    # cursor = conn.cursor()
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM FOOD_ITEM_PATH WHERE ID = {food_id} ORDER BY IMAGE_PATH DESC"
    to_execute = to_execute.format(food_id=wrap_with_in_single_quote(food_id))
    cursor.execute(to_execute)
    f = cursor.fetchall()
    ret_val = []
    for row in f:
        ret_val.append(row[1])
    cursor.close()
    return ret_val


def restaurant(rest_id):
    '''
    returns all details about a restaurant
    except email or password
    :param rest_id:
    :return:
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM RESTAURANT WHERE ID = {id}"
    to_execute = to_execute.format(id=wrap_with_in_single_quote(rest_id))
    cursor.execute(to_execute)
    row = cursor.fetchone()
    cursor.close()
    rest = {}
    rest['id'] = rest_id  # or may be row[0]
    rest['name'] = row[1]
    rest['location'] = row[2]
    rest['logo_path'] = row[3]
    rest['rating'] = row[4]
    rest['open_time'] = row[5]
    rest['close_time'] = row[6]
    cursor.close()
    return rest


def customer(customer_id):
    '''
    returns all data about customer
    except password
    :param customer_id:
    :return:
    '''

    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM CUSTOMER WHERE ID = {id}"
    to_execute = to_execute.format(id=wrap_with_in_single_quote(customer_id))
    cursor.execute(to_execute)
    row = cursor.fetchone()
    cust = {'id': row[0], 'last_name': row[1], 'first_name': row[2], 'email': row[3], 'address': row[5]}
    cust['phone_no'] = customer_phone(cust['id'])
    cursor.close()
    return cust


def customer_all():
    '''
    returns all customers under an admin
    in sorted order of order by a customer
    :return:
    '''

    cursor = sql.create_cursor()
    to_execute = 'SELECT * FROM CUSTOMER C ORDER BY(SELECT COUNT(*) FROM CHOOSES WHERE CUSTOMER_ID = C.ID ) DESC '
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        cust = {'id': row[0], 'last_name': row[1], 'first_name': row[2], 'email': row[3], 'address': row[5]}
        cust['phone_no'] = customer_phone(cust['id'])
        customers.append(cust)
    return customers


def customer_phone(id):
    '''
    returns the latest two numbers updated by customer
    returns as a string using comma separated format
    suppose 00 and 11 is the number so it will return "00,11"
    :param id: string
    :return: string
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM CUSTOMER_PHONE WHERE CUSTOMER_ID ={id} ORDER BY CUSTOMER_ID ASC"
    to_execute = to_execute.format(
        id=wrap_with_in_single_quote(id)
    )
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    cursor.close()
    numbers = ''
    lim = min(2, len(rows))
    for i in range(lim):
        if (i > 0):
            numbers += ','
        numbers += rows[i][1]
    return numbers


def foodman(id):
    '''

    :param id: string
    :return: list
    '''
    cursor = sql.create_cursor()
    to_execute = 'SELECT * FROM FOODMAN WHERE ID = {id}'
    to_execute = to_execute.format(id=wrap_with_in_single_quote(id))
    cursor.execute(to_execute)
    row = cursor.fetchone()
    cursor.close()
    fm = {'id': row[0], 'name': row[1], 'email': row[2], 'rating': row[4], 'image_path': row[5], 'location': row[6],
          'status': row[7]}
    fm['phone_no'] = foodman_phone(fm['id'])
    return fm


def foodman_all():
    '''

    :return: dictinary
    '''
    cursor = sql.create_cursor()
    to_execute = 'SELECT * FROM FOODMAN'
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    cursor.close()
    fms = []
    for row in rows:
        fm = {'id': row[0], 'name': row[1], 'email': row[2], 'rating': row[4], 'image_path': row[5], 'location': row[6],
              'status': row[7]}
        fm['phone_no'] = foodman_phone(fm['id'])
        fms.append(fm)
    return fms


def foodman_phone(id):
    '''
    returns the latest two numbers updated by foodman
    returns as a string using comma separated format
    suppose 00 and 11 is the number so it will return "00,11"
    :param id: string
    :return: string
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM FOODMAN_PHONE WHERE ID ={id} ORDER BY ID ASC"
    to_execute = to_execute.format(
        id=wrap_with_in_single_quote(id)
    )
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    cursor.close()
    numbers = ''
    lim = min(2, len(rows))
    for i in range(lim):
        if (i > 0):
            numbers += ','
        numbers += rows[i][1]
    return numbers


def foodman_vehicle(f_id):
    cursor = sql.create_cursor()
    to_execute = "SELECT V.ID, V.REG_NO, V.TYPE FROM VEHICLE V, DELIVERS_BY D WHERE D.VEHICLE_ID = V.ID AND D.FOODMAN_ID = {f_id}"
    to_execute = to_execute.format(
        f_id=wrap_with_in_single_quote(f_id)
    )
    cursor.execute(to_execute)
    row = cursor.fetchone()
    cursor.close()
    if row is not None:
        return {'id': row[0], 'reg_no': row[1], 'type': row[2]}


def promo(promo_id):
    '''
    returns a dictionary promo(id,name,percent,fixed_amount,promo_limit,min_order_value,max_discount_amount)
    :param promo_id:
    :return:
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM PROMO WHERE ID ={id}"
    to_execute = to_execute.format(
        id=wrap_with_in_single_quote(promo_id)
    )
    cursor.execute(to_execute)
    row = cursor.fetchone()
    cursor.close()
    pr = {'id': row[0], 'name': row[1], 'percent': row[2], 'fixed_amount': row[3], 'promo_limit': row[4],
          'min_order_value': row[5], 'max_discount_amount': row[6]}
    return pr


def promo_all():
    '''
    returns all the available promos
    :return: list of dict
    '''
    cursor = sql.create_cursor()
    to_execute = "SELECT * FROM PROMO"
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    cursor.close()
    promos = []
    for row in rows:
        pr = {'id': row[0], 'name': row[1], 'percent': row[2], 'fixed_amount': row[3], 'promo_limit': row[4],
              'min_order_value': row[5], 'max_discount_amount': row[6]}
        promos.append(pr)
    return promos


def currently_available_orders(not_picke_str=None):
    '''
    returns all the not picked orders
    :return:
    '''
    cursor = sql.open_connection().cursor()
    # cursor = sql.create_cursor()
    to_execute = 'SELECT * FROM "ORDER" WHERE DELIVERY_TIME = TO_DATE({time}, {format})'
    to_execute = to_execute.format(
        time=wrap_with_in_single_quote(not_picked_str),
        format=wrap_with_in_single_quote(date_format_oracle)
    )
    # print(to_execute)
    cursor.execute(to_execute)
    rows = cursor.fetchall()
    cursor.close()
    orders = []
    for row in rows:
        order = {'id': row[0], 'location': row[3]}
        # print(order)
        orders.append(order)
    return orders


def current_order_by_foodman(foodman_id):
    '''
    returns all the available order for a foodman
    :param foodman_id: string
    :return: dict
    '''
    to_excute = 'SELECT O.ID, O.DELIVERY_LOCATION FROM DELIVERS D, "ORDER" O WHERE D.FOODMAN_ID = {foodman_id} AND O.DELIVERY_TIME = TO_DATE({time}, {format})'
    to_excute = to_excute.format(
        foodman_id=wrap_with_in_single_quote(foodman_id),
        time=wrap_with_in_single_quote(not_delivered_str),
        format=wrap_with_in_single_quote(date_format_oracle)
    )
    cursor = sql.create_cursor()
    cursor.execute(to_excute)
    row = cursor.fetchone()
    cursor.close()
    order = {'id': row[0], 'location': row[1]}
    return order


def restaurant_ID_by_order_ID(order_id):
    '''
    grabs the restaurant_id of a particular order
    :param order_id: string
    :return: string
    '''
    to_execute = "SELECT F.RESTAURANT_ID FROM SELECTED S, FOOD_ITEM F WHERE F.ID = S.FOOD_ID AND ORDER_ID = {order_id}"
    to_execute = to_execute.format(
        order_id=wrap_with_in_single_quote(order_id)
    )
    cursor = sql.create_cursor()
    cursor.execute(to_execute)
    row = cursor.fetchone()
    return row[0]


def food_ID_by_order_ID(order_id):
    '''
    grabs only one food_id of a particular order
    :param order_id: string
    :return: string
    '''
    to_execute = "SELECT FOOD_ID FROM SELECTED WHERE ORDER_ID = {order_id}"
    to_execute = to_execute.format(
        order_id=wrap_with_in_single_quote(order_id)
    )
    cursor = sql.create_cursor()
    cursor.execute(to_execute)
    row = cursor.fetchone()
    return row[0]


def restaurant_ID_by_food_ID(food_id):
    '''
    grabs the restaurant_id of a particular food_id
    :param order_id: string
    :return: string
    '''
    to_execute = "SELECT RESTAURANT_ID FROM FOOD_ITEM WHERE ID = {food_id}"
    to_execute = to_execute.format(
        food_id=wrap_with_in_single_quote(food_id)
    )
    cursor = sql.create_cursor()
    cursor.execute(to_execute)
    row = cursor.fetchone()
    return row[0]


if __name__ == '__main__':
    current_available_orders()
