#!/usr/bin/env python

import requests
from pprint import pprint

stop, start = 3, 1


def post(processor, task, state):
    msg = {
        "name": "fn1-0003",
        "namespace": "default",
        "function": "fn1",
        "version": "latest",
        "alias": "latest",
        "ip": "",
        "port": 0,
        "state": 1,
        "lastEvent": "0001-01-01T00:00:00Z",
        "jobs": {
            "franz": {
                "totalTasks": 5,
                "tasks": [
                    {
                        "id": task,
                        "state": state,
                    }
                ]
            }
        }
    }

    return requests.post(urlof(processor), json=msg).json()


def urlof(pid):
    return f'http://localhost:88{pid:02d}/triggers'


def log(msg):
    size = 10
    lpad, rpad = '<' * size, '>' * size
    print(f'{lpad} {msg:^40} {rpad}')


def status():
    for pid in (1, 2):
        print(pid)
        resp = requests.get(urlof(pid)).json()
        pprint(resp['jobs']['franz']['tasks'])


log('INITIAL GET')
status()

input('Hit Enter')

log('STOPPING 1/1')
resp = post(1, 1, stop)
pprint(resp['jobs']['franz']['tasks'])

log('STATUS')
status()

input('Hit Enter')

log('STARTING 2/1')
resp = post(2, 1, start)
pprint(resp['jobs']['franz']['tasks'])

log('STATUS')
status()
