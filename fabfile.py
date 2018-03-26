"""Running remote jobs on a CI machine

You'll need fabric3 installed.
To install a machine run
    fab install

To run tests run
    fab test
"""
from os import environ
# from os.path import expanduser

from fabric.api import env, execute, run, settings, sudo, task
from fabric.context_managers import shell_env

ci_host = environ.get('NUCLIO_CI_HOST', '35.204.211.55')
# key_file = environ.get('NUCLIO_CI_KEY', expanduser('~/.ssh/nuclio-ci.pem'))

# user = 'ubuntu'
user = 'miki'
env['user'] = user
env['host_string'] = ci_host
# env['key_filename'] = key_file
src_dir = '~/go/src/github.com/nuclio/nuclio'


@task
def install_docker():
    sudo('apt-get update')
    packages = [
        'apt-transport-https',
        'ca-certificates',
        'curl',
        'make',
        'software-properties-common',
        'tmux',
    ]
    sudo(f'apt-get install -y {" ".join(packages)}')
    run('curl -o key -fsSL https://download.docker.com/linux/ubuntu/gpg')
    sudo('apt-key add key')
    run('rm key')
    version = str(run('lsb_release -cs'))
    url = 'https://download.docker.com/linux/ubuntu'
    repo = f'deb [arch=amd64] {url} {version} edge'
    sudo(f'sudo add-apt-repository "{repo}"')
    sudo('apt-get update')
    sudo('apt-get install -y docker-ce')
    sudo('groupadd docker', warn_only=True)
    sudo(f'usermod -aG docker {user}')


@task
def install_docker_gce():
    sudo('apt-get update')
    packages = [
        'apt-transport-https',
        'ca-certificates',
        'curl',
        'make',
        'software-properties-common',
    ]
    sudo(f'apt-get install -y {" ".join(packages)}')
    run('curl -o key -fsSL https://download.docker.com/linux/debian/gpg')
    sudo('apt-key add key')
    run('rm key')
    version = str(run('lsb_release -cs'))
    url = 'https://download.docker.com/linux/debian'
    repo = f'deb [arch=amd64] {url} {version} stable'
    sudo(f'sudo add-apt-repository "{repo}"')
    sudo('apt-get update')
    sudo('apt-get install -y docker-ce')
    sudo('groupadd docker', warn_only=True)
    sudo(f'usermod -aG docker {user}')


@task
def install_go():
    run('curl -LO https://dl.google.com/go/go1.10.linux-amd64.tar.gz')
    run('tar xzf go1.10.linux-amd64.tar.gz')
    run('rm go1.10.linux-amd64.tar.gz')
    sudo('mv go /opt')
    run('echo \'export PATH=/opt/go/bin:$PATH\' >> ~/.bashrc')
    run('echo \'export GOPATH=${HOME}/go\' >> ~/.bashrc')


@task
def clone_nuclio():
    run(f'git clone https://github.com/tebeka/nuclio.git {src_dir}')
    with settings(cwd=src_dir), shell_env(GOPATH=f'/home/{user}/go'):
        run('git remote add nuclio https://github.com/nuclio/nuclio.git')
        run('git fetch nuclio')
    packages = [
        'github.com/nuclio/amqp',
        'github.com/nuclio/logger',
        'github.com/nuclio/nuclio-sdk-go',
        'github.com/v3io/v3io-go-http',
    ]
    for pkg in packages:
        run(f'/opt/go/bin/go get {pkg}')
    run('mkdir -p ~/go/bin')


@task
def install():
    execute(install_docker)
    execute(install_go)
    execute(clone_nuclio)


@task
def make_images():
    with settings(cwd=src_dir), shell_env(GOPATH=f'/home/{user}/go'):
        run('make build')


@task
def run_tests(branch):
    with settings(cwd=src_dir), shell_env(GOPATH=f'/home/{user}/go'):
        run(f'git checkout {branch}')
        run('git pull')
        run('2>&1 make test | tee ~/nuclio-test-$(date +%Y%m%dT%H%M%S).log')
        # run('make lint test')
