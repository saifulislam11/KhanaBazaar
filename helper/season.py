def not_this_season(request, app_name):
    '''
    if request season is empty or the season app_name doesn't matches
    flushes the season and returns true
    :param request:
    :param app_name:
    :return: boolean
    '''
    if request.season.is_empty():
        return True
    elif request.season.get('app_name') == app_name:
        return False
    else:
        request.season.flush()
        return True
