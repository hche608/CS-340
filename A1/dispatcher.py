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
        process.process_event.set()

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
            process.iosys.move_process(process, self.runningStack.index(process))
            for x in range(len(self.runningStack)):
                self.runningStack[x].iosys.move_process(self.runningStack[x], x)
            process.process_event.set()

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
        if len(self.runningStack) > 0:
            self.runningStack[len(self.runningStack) - 1].process_event.set()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...
        for process in self.runningStack:
            process.join()

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...
        process.state = State.killed
        process.iosys.remove_window_from_process(process)
        if process in self.waitingList:
            self.waitingList[self.waitingList.index(process)] = None
        if process in self.runningStack:
            self.runningStack.remove(process)
        for x in range(len(self.runningStack)):
            self.runningStack[x].iosys.move_process(self.runningStack[x], x)
        #for x in range(len(self.waitingList)):
        #    if not self.waitingList[x] == None:
        #        self.runningStack[x].iosys.move_process(self.waitingList[x], x)
        self.resume_system()
        
    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...
        process.state = State.waiting
        process.process_event.clear()
        if process in self.runningStack:
            self.runningStack.remove(process)        
        if not process in self.waitingList:
            if None in self.waitingList:
                self.waitingList[self.waitingList.index(None)] = process
            else:
                self.waitingList.append(process)            
        process.iosys.move_process(process, self.waitingList.index(process))               
        self.resume_system()

    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        for process in self.runningStack:
            if process.id == id:
                return process
        for process in self.waitingList:
            if not process == None:
                if process.id == id:
                    return process
        return None
