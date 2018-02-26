from time import sleep

def reverser(context, event):
    body = event.body.decode('utf-8')
    return body[::-1]


def handler(context, event):
    return 'OK'


def slow(context, event):
    sleep(0.1)
    return 'SLOW'
