def users(data):
    result = "<select name= 'title'> "
    for i in data:
        result += '<option value="%s"selected>%s</option>' % (i, i)
    result += '</select>'

    return (result)
