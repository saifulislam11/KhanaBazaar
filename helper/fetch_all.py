from helper import sql
from helper.wrap_and_encode import wrap_with_in_single_quote


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


if __name__ == '__main__':
    foods = food_item_all('1000000152')
    print(foods)
    for row in foods:
        print('new food \n\n', type(row))
        print(row)
