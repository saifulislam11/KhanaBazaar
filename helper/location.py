buet_location = '23.7265768,90.3926623'


def valid_location(location):
    '''
    checks if a loction is valid or not
    :param loc:
    :return:
    '''
    try:
        arr = location.split(',')
        if arr.size() != 2:
            raise Exception
        a = float(arr[0])
        b = float(arr[1])
    except Exception as e:
        print(e)
        return False
    return True
