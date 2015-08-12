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
        # ...
        self.runningStack = []
        self.waitingIndex = 0

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        # ...
        if process.state == State.runnable:
            if 0 < len(self.runningStack):
                self.runningStack[len(self.runningStack) - 1].event.clear()
            self.runningStack.append(process)
            process.iosys.allocate_window_to_process(process, self.runningStack.index(process) - self.waitingIndex)
            process.start()
            process.event.set()
        else:
            if 0 < len(self.runningStack):
                self.runningStack[len(self.runningStack) - 1].event.clear()
            self.runningStack.append(process)
            process.iosys.allocate_window_to_process(process, self.waitingIndex)
            self.waitingIndex = self.waitingIndex + 1

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        # ...

    def to_top(self, process):
        """Move the process to the top of the stack."""
        # ...
        self.pause_system()
        self.runningStack.remove(process)
        self.runningStack.append(process)
        self.resume_system()


    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        # ...
        self.runningStack[len(self.runningStack) - 1].event.clear()

    def resume_system(self):
        """Resume running the system."""
        # ...
        self.runningStack[len(self.runningStack) - 1].event.set()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...
        if process.state == State.waiting:
            self.waitingIndex = self.waitingIndex - 1
        process.iosys.remove_window_from_process(process)
        self.runningStack.remove(process)
        if len(self.runningStack) > 0:
            self.resume_system()

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...
        process.event.clear()

    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        for process in self.runningStack:
            if process.id == id:
                return process
        return None

