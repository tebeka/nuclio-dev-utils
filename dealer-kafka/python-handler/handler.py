from time import sleep, strftime


def reverser(context, event):
    body = event.body.decode('utf-8')
    return body[::-1]


def handler(context, event):
    return 'OK'


def slow(context, event):
    sleep(0.1)
    return 'SLOW'


def log(context, event):
    body = event.body.decode('utf-8')
    with open('/tmp/py-handler.log', 'at') as out:
        timestamp = strftime('%Y-%m-%dT%H:%M:%S')
        out.write('[{}] {}\n'.format(timestamp, body))
        out.flush()
    return 'Event logged\n'
