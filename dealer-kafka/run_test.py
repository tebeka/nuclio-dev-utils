#!/usr/bin/env python

"""Run minimal test after "make run-processor" setup"""

import requests
from argparse import ArgumentParser

stop, start = 3, 1
verbose = False


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
        "triggers": {
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
        print(f'processor {pid} tasks:')
        resp = requests.get(urlof(pid)).json()
        print_tasks(resp)


def print_tasks(resp):
    if verbose:
        print(f'RESP:\n{resp}\n---------------\n')

    for task in resp['triggers']['franz']['tasks']:
        print(f'\t{task}')


parser = ArgumentParser(description=__doc__)
parser.add_argument('--verbose', '-v', help='be verbose', action='store_true')
args = parser.parse_args()

verbose = args.verbose


log('INITIAL GET')
status()

input('Hit Enter')

log('STOPPING 1/1')
resp = post(1, 1, stop)
print_tasks(resp)

log('STATUS')
status()

input('Hit Enter')

log('STARTING 2/1')
resp = post(2, 1, start)
print_tasks(resp)

log('STATUS')
status()
