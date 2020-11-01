from cx_Oracle import connect


def openConnection():
    """
    creates a connection
    :return: a connection object
    """
    con = connect("KB", "123", "localhost/orcl")
    return con


def get_next_id():
    """

    :return: the next possible ID for our ID columns
    """
    con = openConnection()
    c = con.cursor()
    sql = 'Select ID_GENERATOR.NEXTVAL FROM DUAL'
    c.execute(sql)
    id = c.fetchone()
    id = str(id[0])
    con.close()
    #print(id)
    return str(id)
