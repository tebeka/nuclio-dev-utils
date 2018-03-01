#!/usr/bin/env python
"""Spam kafka with message"""

from argparse import ArgumentParser
from itertools import count
from random import random
from subprocess import run
from time import sleep

from pykafka import KafkaClient

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '--run-docker', action='store_true', default=False,
    help='run docker and exit')
parser.add_argument('--topic', help='topic to post', default='topic1')
parser.add_argument('--verbose', '-v', help='be verbose', action='store_true')
args = parser.parse_args()

if args.run_docker:
    cmd = [
        'docker', 'run',
        '-p', '2181:2181',
        '-p', '9092:9092',
        '--env', 'ADVERTISED_HOST=127.0.0.1',
        '--env', 'ADVERTISED_PORT=9092',
        'spotify/kafka',
    ]
    run(cmd)
    raise SystemExit


log = print if args.verbose else lambda x: 1

client = KafkaClient(hosts='127.0.0.1:9092')
topic = client.topics[args.topic.encode()]
log(f'topic = {topic}')
prod = topic.get_producer()

for msg_id in count(1):
    msg = f'Message #{msg_id}'
    log(msg)
    prod.produce(msg.encode())
    sleep(random())
