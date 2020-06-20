import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import paramiko
import json

scp = None
hostname = ""
port = 0
username = ""
password = ""
local = ""
destination = ""

## create ssh client
ssh = SSHClient()
ssh.load_system_host_keys()

## create event handler
# properties
patterns = ["*.jar"]
ignorePatterns = ""
ignoreDirectories = True
caseSensitive = False

eventHandler = PatternMatchingEventHandler(patterns, ignorePatterns, ignorePatterns, caseSensitive)

# events
def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    print(f"moving {event.src_path} to {destination}...")
    scp.put(event.src_path, destination + event.src_path)

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

def connect_scp():
    print("connecting scp.. check your scp-config.json if this fails...")
    # read properties from scp config
    with open('scp-config.json', 'r' as config):
        data = config.read()
        obj = json.loads(data)
        hostname = str(obj['hostname'])
        port = int(obj['port'])
        username = str(obj['username'])
        password = str(obj['password'])
        local = str(obj['local-path'])
        destination = str(obj['destination-path'])
    # connect ssh
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    # create scp connection
    scp = SCPClient(ssh.get_transport())

# assign events
eventHandler.on_created = on_created
eventHandler.on_deleted = on_deleted
eventHandler.on_modified = on_modified
eventHandler.on_moved = on_moved

## create observer
# properties
path = "."
go_recursively = True
# create observer instance
observer = Observer()
# assign properties
observer.schedule(eventHandler, path, recursive=go_recursively)

## start program
if __name__ == "__main__":
    print("hey, just ignore me... I'm just waiting for file changes...")
    # start the observer
    observer.start()
    connect_scp()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # end observer
        observer.stop()
        observer.join()
        scp.close()
    print("have a nice day bud :)")