def reverser(context, event):
    body = event.body.decode('utf-8')
    return body[::-1]


def handler(context, event):
    return 'OK'
