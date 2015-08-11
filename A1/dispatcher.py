# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by ...

# You are not allowed to use any sleep calls.

from threading import Lock, Event
from process import State

class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8

    def __init__(self):
        """Construct the dispatcher."""
        self.items = []

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        if 0 < len(self.items):
            self.items[len(self.items) - 1].state = State.waiting
            self.items[len(self.items) - 1].event.clear()
        if len(self.items) < self.MAX_PROCESSES:
            self.items.append(process)
            process.iosys.allocate_window_to_process(process, self.items.index(process))
            process.state = State.runnable
            process.start()
            

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        # ...

    def to_top(self, process):
        """Move the process to the top of the stack."""
        self.pause_system()
        self.items.remove(process)
        self.items.append(process)
        self.resume_system()

    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        self.items[len(self.items) - 1].event.clear()


    def resume_system(self):
        """Resume running the system."""
        self.items[len(self.items) - 1].event.set()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        process.iosys.remove_window_from_process(process)
        self.items.remove(process)
        if len(self.items) > 0:
            self.resume_system()
        # ...

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...
        #process.state = State.waiting
        process.event.clear()

    def process_with_id(self, id):
        """Return the process with the id."""
        for process in self.items:
            if process.id == id:
                return process
        return None

