# Fab-File for Testing
from __future__ import with_statement
from __future__ import print_function

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
from fabric.contrib.files import exists

#from lmu_settings_old import hosts as lmu_hosts
from all_hosts import hosts as lmu_hosts

env.hosts = lmu_hosts


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
def check_needs_restart():
    print("["+ env.host_string + "] Run Check is System needs Restart:")
    print("---------------------------------------------")
    with settings(warn_only=True):
        sudo('zypper ps')
    print("\n")

@task
def update_repo():
    with settings(warn_only=True):
        sudo('zypper removerepo SLES-11-ZUV')
        sudo('zypper addrepo http://yup.verwaltung.uni-muenchen.de/ZUV-RPM/ZUV-RPM.repo')
        sudo('rpm --import  http://yup.verwaltung.uni-muenchen.de/ZUV-RPM/repodata/repomd.xml.key')

@task
def linux_updates():
    with settings(warn_only=True):
        result = sudo("zypper update -y")
        if result.return_code == 102:
            print('needs reboot')
            sudo("touch /var/run/reboot-required")
            

@task
def reboot_if_needed():
    if exists("/var/run/reboot-required"):
        print("["+ env.host_string + "] System needs Restart :")
        print("---------------------------------------------")
        reboot()

# @task
# def restart_server():
#     reboot();

@task
@hosts('localhost')
def scan_hostnames():
    import socket
    host_list = []
    for ip_subset in (list(xrange(97,123))+list(xrange(193,252))):
        test_ping = run('ping -c 1 10.153.101.'+str(ip_subset), quiet=True, warn_only=True)
        result = ('10.153.101.'+str(ip_subset), [], '10.153.101.'+str(ip_subset))
        if test_ping.succeeded:
            try: 
                result = socket.gethostbyaddr('10.153.101.'+str(ip_subset))
            except socket.herror:
                pass
            except:
                import ipdb; ipdb.set_trace()
            host_list.append(result)
            print(result)
    hostname_list = list(name[0] for  name in  host_list)
    return hostname_list


@task
def show_release_version():
    with settings(warn_only=True):
        run('cat /etc/SuSE-release')


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
