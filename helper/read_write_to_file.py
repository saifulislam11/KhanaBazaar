

def handle_uploaded_file(f, prefix,location, id = None, ):
    """
    :param f: file itself
    :param prefix: prefix of the file . like rest1.jpg here rest1 would be prefix
    :param location: where to save. need suggestion
    :param id: id for the element
    :return: Boolean
    """
    name = location + prefix + str(id)+ '.png'
    print(name)
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)