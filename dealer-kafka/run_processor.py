#!/usr/bin/env python
"""Run the python processor"""

import atexit
from argparse import ArgumentParser, FileType
from os import environ, remove
from os.path import abspath, basename, dirname, exists, splitext
from shutil import rmtree
from subprocess import Popen

here = dirname(abspath(__file__))

default_file = f'{here}/python-handler/handler.py'
default_handler = 'log'

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-f', '--file', help='handler file', type=FileType(), default=default_file)
parser.add_argument(
    '-H', '--handler', help='handler name', default=default_handler)
parser.add_argument(
    '-c', '--count', help='number of processors', type=int, default=1)
args = parser.parse_args()

py_path = dirname(args.file.name)
module_name, _ = splitext(basename(args.file.name))
handler_name = args.handler

cfg_template = '''
metadata:
  name: python handler
spec:
  runtime: python
  handler: {module_name}:{handler_name}
  triggers:
    franz:
      kind: "kafka"
      url: "127.0.0.1:9092"
      attributes:
        topic: trial
      partitions:
        - id: "{partition}"
'''

plat_cfg_template = '''
webAdmin:
  enabled: true
  listenAddress: {address}
'''

wrapper_script = f'{here}/wrapper.py'

env = environ.copy()
env['NUCLIO_PYTHON_PATH'] = py_path
env['NUCLIO_PYTHON_WRAPPER_PATH'] = wrapper_script


def run_processor(i):
    cfg = cfg_template.format(
        module_name=module_name,
        handler_name=handler_name,
        partition=i,
    )
    cfg_file = f'/tmp/kafka-function-{i}.yml'
    with open(cfg_file, 'w') as out:
        out.write(cfg)

    plat_cfg = plat_cfg_template.format(
            address=f':88{i:02d}'
    )
    plat_file = f'/tmp/kafka-platform-{i}.yml'
    with open(plat_file, 'w') as out:
        out.write(plat_cfg)

    cmd = [
        './processor',
        '-config', cfg_file,
        '-platform-config', plat_file,
    ]

    return Popen(cmd, env=env)


def cleanup(processes=None):
    pyc = args.file.name + 'c'
    if exists(pyc):
        remove(pyc)

    pycache = f'{py_path}/__pycache__'
    if exists(pycache):
        rmtree(pycache)

    for p in processes or []:
        p.kill()


cleanup()  # Clean slate

processes = []
for i in range(args.count):
    process = run_processor(i+1)
    processes.append(process)

atexit.register(lambda: cleanup(processes))
input('Hit Enter to quit')
