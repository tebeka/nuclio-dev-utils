#!/usr/bin/env python
"""Spam kafka with message"""

from argparse import ArgumentParser
from itertools import count
from os import remove
from os.path import expanduser, isfile
from random import random
from subprocess import PIPE, run
from time import sleep


id_file = expanduser('~/.nuclio-kafka-id')


def get_container_id():
    with open(id_file) as fp:
        return fp.read().strip()


def create_topic(name):
    container_id = get_container_id()
    cmd = [
        'docker', 'exec', container_id,
        '/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh',
        '--create', '--topic', name,
        '--zookeeper', 'localhost:2181',
        '--partitions', '7',
        '--replication-factor', '1',
    ]
    print(' '.join(cmd))
    rv = run(cmd)
    return rv.returncode == 0


def connect_kafka():
    # Import here so we can run other commands in Python
    from pykafka import KafkaClient

    return KafkaClient(hosts='127.0.0.1:9092')


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
        kafka_cid = get_container_id()
        out = run(['docker', 'ps', '-q'], stdout=PIPE).stdout.decode('utf-8')
        for line in out.splitlines():
            cid = line.strip()
            if kafka_cid.startswith(cid):  # Short/long ID
                raise SystemExit('error: kafka docker running')
        print('warning: ignoring stale id file')

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
    if rv.returncode != 0:
        raise SystemExit(rv.returncode)
    sleep(10)

    rv = 0 if create_topic(args.topic) else 1
    raise SystemExit(rv)

try:
    container_id = get_container_id()
except IOError:
    raise SystemExit('error: container not running')

if args.stop_docker:
    cmd = ['docker', 'rm', '-f', container_id]
    print(' '.join(cmd))
    rv = run(cmd)
    if rv.returncode == 0:
        remove(id_file)
    raise SystemExit(rv.returncode)

if args.create_topic:
    rv = 0 if create_topic(args.topic) else 1
    raise SystemExit(rv)


log = print if args.verbose else lambda x: 1

client = connect_kafka()
topic = client.topics[args.topic.encode()]
log(f'topic = {topic}')
prod = topic.get_producer()

for msg_id in count(1):
    msg = f'Message #{msg_id}'
    log(msg)
    prod.produce(msg.encode())
    sleep(random())
