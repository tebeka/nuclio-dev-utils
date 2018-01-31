from shutil import copy, copytree
from subprocess import call
from tempfile import mkdtemp

# Assume we're running from nuclio root
wrapper_jar_dir = 'pkg/processor/runtime/java'


def build_wrapper(jar_file):
    tmp_dir = mkdtemp(prefix="nuclio-java-build")
    build_dir = f'{tmp_dir}/build'

    copytree(wrapper_jar_dir, build_dir)
    copy(jar_file, f'{build_dir}/user-handler.jar')
    exit_val = call(['gradle', 'shadowJar'], cwd=build_dir)
    if exit_val != 0:
        return ''

    return f'{build_dir}/build/libs/nuclio-java-wrapper.jar'
