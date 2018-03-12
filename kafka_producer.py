#!/usr/bin/env python
"""Spam kafka with message"""

from argparse import ArgumentParser
from itertools import count
from os.path import expanduser, isfile
from random import random
from subprocess import run
from time import sleep

from pykafka import KafkaClient

id_file = expanduser('~/.nuclio-kafka-id')


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '--run-docker', action='store_true', default=False,
    help='run docker and exit')
parser.add_argument(
    '--stop-docker', action='store_true', default=False,
    help='stop docker and exit')
parser.add_argument(
    '--create-topic', action='store_true', default=False,
    help='create topic and exit')
parser.add_argument('--topic', help='topic to post', default='trial')
parser.add_argument('--verbose', '-v', help='be verbose', action='store_true')
args = parser.parse_args()

if args.run_docker:
    if isfile(id_file):
        raise SystemExit('error: kafka docker running')

    cmd = [
        'docker', 'run', '-d',
        '-p', '2181:2181',
        '-p', '9092:9092',
        '--env', 'ADVERTISED_HOST=127.0.0.1',
        '--env', 'ADVERTISED_PORT=9092',
        'spotify/kafka',
    ]
    print(' '.join(cmd))
    with open(id_file, 'w') as out:
        rv = run(cmd, stdout=out)
    raise SystemExit(rv.returncode)

try:
    with open(id_file) as fp:
        container_id = fp.read().strip()
except IOError:
    raise SystemExit('error: container not running')

if args.stop_docker:
    cmd = ['docker', 'rm', '-rf', container_id]
    print(' '.join(cmd))
    rv = run(cmd)
    raise SystemExit(rv.returncode)

if args.create_topic:
    cmd = [
        'docker', 'exec', container_id,
        '/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh',
        '--create', '--topic', args.topic,
        '--zookeeper', 'localhost:2181',
        '--partitions', '7',
        '--replication-factor', '1',
    ]
    print(' '.join(cmd))
    rv = run(cmd)
    raise SystemExit(rv.returncode)


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
