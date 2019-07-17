def users(data):
    result = "<select name= 'usr'> "
    for i in data:
        result += '<option value="%s"selected>%s</option>' % (i, i)
    result += '</select>'

    return (result)
