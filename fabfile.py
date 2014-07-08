# Fab-File for Testing
from __future__ import with_statement

from fabric.api import env
from fabric.api import hosts
from fabric.api import local
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import sudo
from fabric.api import settings
from fabric.api import task
from fabric.api import abort

from fabric.contrib.console import confirm

#from lmu_settings_old import hosts as lmu_hosts
from all_hosts import hosts as lmu_hosts
from lmu_settings import roledefs as lmu_roledefs

from lmu_ref_vi5.cert_check_tasks import test_certs_java
from lmu_ref_vi5.cert_check_tasks import test_certs_ssl

env.hosts = lmu_hosts

env.roledefs = lmu_roledefs

@task
def hello():
    run('echo "Echo: Hello World')
    print("Hello World")

@task 
@hosts('localhost')
def print_host_list():
    print("\n".join(lmu_hosts))

@task
def test_certs():
    print("["+ env.host_string + "] Run Cert-Checks:")
    print("---------------------------------------------")
    test_certs_java()
    test_certs_ssl()
    print("\n")

@task
def linux_updates():
    with settings(warn_only=True):
        sudo("zypper update -y")

# @task
# def restart_server():
#     reboot();

@task
@hosts('localhost')
def scan_hostnames():
    import socket
    host_list = []
    for ip_subset in (list(xrange(97,123))+list(xrange(193,251))):
        try: 
            result = socket.gethostbyaddr('10.153.101.'+str(ip_subset))
            test_ping = run('ping -c 1 10.153.101.'+str(ip_subset), quiet=True, warn_only=True)
            if test_ping.succeeded: 
                host_list.append(result)
            print(result)
        except socket.herror:
            pass
    hostname_list = list(name[0] for  name in  host_list)
    return hostname_list

@task
def collect_facts():
    print("["+ env.host_string + "] Collect Server Facts")
    with settings(warn_only=True):
        result = run("uname -a")

@task 
@hosts('localhost')
def write_host_list():
    list_file = open('all_hosts.py', 'w')
    list_file.write("\nhosts = [\n    '")
    list_file.write("',\n    '".join(scan_hostnames()))
    list_file.write("'\n]\n\n")
