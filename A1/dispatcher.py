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
        self.waitingList = []

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        # ...
        if 0 < len(self.runningStack):
            self.pause_system()
        self.runningStack.append(process)
        process.iosys.allocate_window_to_process(process, self.runningStack.index(process))
        process.start()
        self.dispatch_next_process()

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        # ...
        if len(self.runningStack) > 0:
            self.runningStack[len(self.runningStack) - 1].process_event.set()

    def to_top(self, process):
        """Move the process to the top of the stack."""
        # ...
        if process in self.runningStack:
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
        if len(self.runningStack) > 0:
            self.runningStack[len(self.runningStack) - 1].process_event.clear()

    def resume_system(self):
        """Resume running the system."""
        # ...
        self.dispatch_next_process()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...
        process.state = State.killed
        process.iosys.remove_window_from_process(process)
        if process in self.runningStack:
            self.runningStack.remove(process)
            for x in range(len(self.runningStack)):
                self.io_sys.move_process(self.runningStack[x], x)
        elif process in self.waitingList:
            self.waitingList.remove(process)
            for x in range(len(self.waitingList)):
                self.io_sys.move_process(self.waitingList[x], x)
        self.dispatch_next_process()

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...
        if process in self.runningStack:
            self.runningStack.remove(process)
        process.state = State.waiting
        self.waitingList.append(process)
        process.iosys.move_process(process, self.waitingList.index(process))
        process.process_event.clear()
        self.resume_system()

    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        for process in self.runningStack:
            if process.id == id:
                return process
        for process in self.waitingList:
            if process.id == id:
                return process
        return None
