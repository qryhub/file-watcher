import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

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

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

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
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # end observer
        observer.stop()
        observer.join()
    print("have a nice day bud :)")