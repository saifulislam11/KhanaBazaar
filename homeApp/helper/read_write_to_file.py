def handle_uploaded_file(f, file_name, location):
    """
    we will save lod
    :param f: file itself
    :param file_name: fileName to be saved as
    :param location: where to save or base directory. need suggestion
    :return: Boolean
    """
    name = location + file_name
    print(name)
    try:
        with open(name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        print("hello world")
        return False
