from jenkins import Jenkins, JenkinsError, NodeLaunchMethod
import os
import signal
import sys
import urllib.request as url
import subprocess
import shutil
import requests
import time

# Paths and URLs
slave_jar = '/var/lib/jenkins/slave.jar'
slave_name = os.environ.get('SLAVE_NAME', f'docker-slave-{os.environ.get("HOSTNAME")}')
jnlp_url = f"{os.environ.get('JENKINS_URL')}/computer/{slave_name}/slave-agent.jnlp"
slave_jar_url = f"{os.environ.get('JENKINS_URL')}/jnlpJars/slave.jar"
print(slave_jar_url)

process = None

def add_host_to_hosts_file(ip, hostname):
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    new_entry = f"{ip} {hostname}\n"
    try:
        with open(hosts_path, 'a') as file:
            file.write(new_entry)
        print(f"Added {ip} {hostname} to hosts file.")
    except PermissionError:
        print("Permission denied: Unable to write to the hosts file. Please check the file permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

add_host_to_hosts_file("10.0.0.20", "eldan-repo.devopshift.com")

def clean_dir(directory):
    """Recursively deletes files and directories in the given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.unlink(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def slave_create(node_name, working_dir, executors, labels):
    """Creates a new Jenkins node."""
    jenkins = Jenkins(os.environ.get('JENKINS_URL'), os.environ.get('JENKINS_USER'), os.environ.get('JENKINS_PASS'))
    jenkins.node_create(node_name, working_dir, num_executors=int(executors), labels=labels, launcher=NodeLaunchMethod.JNLP)

def slave_delete(node_name):
    """Deletes a Jenkins node."""
    jenkins = Jenkins(os.environ.get('JENKINS_URL'), os.environ.get('JENKINS_USER'), os.environ.get('JENKINS_PASS'))
    jenkins.node_delete(node_name)

def slave_download(target):
    """Downloads the Jenkins slave jar to a specified target."""
    if os.path.isfile(slave_jar):
        os.remove(slave_jar)
    loader = url.URLopener()
    loader.retrieve(f"{os.environ.get('JENKINS_URL')}/jnlpJars/slave.jar", target)

def slave_run(slave_jar, jnlp_url):
    """Runs the Jenkins slave."""
    params = ['java', '-jar', slave_jar, '-jnlpUrl', jnlp_url]
    slave_address = os.environ.get('JENKINS_SLAVE_ADDRESS')
    if slave_address:
        params.extend(['-connectTo', slave_address])

    slave_secret = os.environ.get('SLAVE_SECRET')
    if not slave_secret:
        params.extend(['-jnlpCredentials', f"{os.environ.get('JENKINS_USER')}:{os.environ.get('JENKINS_PASS')}"])
    else:
        params.extend(['-secret', slave_secret])
    return subprocess.Popen(params, stdout=subprocess.PIPE)

def signal_handler(sig, frame):
    """Handles incoming signals and terminates the process gracefully."""
    global process
    if process:
        process.send_signal(signal.SIGINT)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def master_ready(url):
    """Checks if the Jenkins master is ready to serve requests."""
    try:
        response = requests.head(url, verify=False, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

while not master_ready(slave_jar_url):
    print("Master not ready yet, sleeping for 10sec!")
    time.sleep(10)

slave_download(slave_jar)
print("Downloaded Jenkins slave jar.")

working_dir = os.environ.get('SLAVE_WORKING_DIR')
if working_dir:
    os.chdir(working_dir)

if os.environ.get('CLEAN_WORKING_DIR') == 'true':
    clean_dir(os.getcwd())
    print("Cleaned up working directory.")

if not os.environ.get('SLAVE_NAME'):
    slave_create(slave_name, os.getcwd(), os.environ.get('SLAVE_EXECUTORS'), os.environ.get('SLAVE_LABELS'))
    print(f"Created temporary Jenkins slave with name {slave_name}.")

process = slave_run(slave_jar, jnlp_url)
print(f"Started Jenkins slave with name {slave_name} and labels [{os.environ.get('SLAVE_LABELS')}].")
process.wait()

print("Jenkins slave stopped.")
if not os.environ.get('SLAVE_NAME'):
    slave_delete(slave_name)
    print("Removed temporary Jenkins slave.")
