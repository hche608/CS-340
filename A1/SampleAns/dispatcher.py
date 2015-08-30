# You are not allowed to use any sleep calls.

from threading import Lock, Event
from process import State
import sys

class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8

    def __init__(self):
        """Construct the dispatcher."""
        self.runnable_stack = []    # the stack of runnable processes
        self.waiting_list = [None] * Dispatcher.MAX_PROCESSES      # the list of waiting processes
        self.mutex = Lock()         # to prevent race conditions
        self.finished = Event()     # used when waiting for completion
        self.finished.set()

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def num_processes(self):
        """Return the number of unfinished processes."""
        return len(self.runnable_stack) + len(list(filter(None, self.waiting_list)))

    def add_process(self, process):
        """Add and start the process."""
        if self.num_processes() >= Dispatcher.MAX_PROCESSES:
            raise Exception("MAX_PROCESSES exceeded")
        with self.mutex:
            self.pause_current_process()
            process.state = State.runnable
            self.runnable_stack.append(process)
            process.start() # doesn't start running until the event is signalled
            self.io_sys.allocate_window_to_process(process, len(self.runnable_stack) - 1)
            self.dispatch_next_process()
        # process.block_event.set() # signal the process to start running

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        if len(self.runnable_stack) > 0:
            self.finished.clear()
            current_process = self.runnable_stack[-1]
            current_process.block_event.set()
        else:
            self.finished.set() # N.B. remember to clear when running a process

    def pause_current_process(self):
        """Pause the current process."""
        if len(self.runnable_stack) > 0:
            current_process = self.runnable_stack[-1]
            current_process.block_event.clear()

    def kill(self, process):
        """Kill the process, removing it from the system."""
        with self.mutex:
            state = process.state
            process.state = State.killed
            process.block_event.set() # run down and exit
            self.io_sys.remove_window_from_process(process)
            if state == State.runnable:
                position = self.runnable_stack.index(process)
                self.runnable_stack.remove(process)
                for i in range(position, len(self.runnable_stack)):
                    proc = self.runnable_stack[i]
                    self.io_sys.move_process(proc, i)
            elif state == State.waiting:
                self.waiting_list.remove(process)

            self.dispatch_next_process()

    def swap(self, processA, processB):
        """Swap processA with processB in the stack."""
        self.io_sys.swap_windows(processA, processB) # this does the panels
        # also have to do the processes themselves
        pos_A = self.runnable_stack.index(processA)
        pos_B = self.runnable_stack.index(processB)
        self.runnable_stack[pos_A] = processB
        self.runnable_stack[pos_B] = processA

    def to_top(self, process):
        """Move the process to the top of the stack."""
        with self.mutex:
            self.pause_current_process()
            where = self.runnable_stack.index(process)
            while where < len(self.runnable_stack) - 1:
                self.swap(process, self.runnable_stack[where + 1])
                where += 1
            self.dispatch_next_process()


    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        with self.mutex:
            self.pause_current_process()

    def resume_system(self):
        """Resume running the system."""
        with self.mutex:
            self.dispatch_next_process()

    def wait_until_finished(self):
        """Hang around until runnable processes finished."""
        # also shut down the waiting processes
        # self.shutdown_processes(self.waiting_list)
        self.finished.wait()

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        with self.mutex:
            self.runnable_stack.remove(process)
            self.io_sys.remove_window_from_process(process)
            self.dispatch_next_process()

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        with self.mutex:
            self.runnable_stack.remove(process)

            position = self.waiting_list.index(None)
            self.waiting_list[position] = process

            process.state = State.waiting
            self.io_sys.move_process(process, position)
            process.block_event.clear()
            self.dispatch_next_process()

    def wake_up_waiting_proc(self, process):
        """Move the process to the top of the runnable stack and set it running."""
        with self.mutex:
            self.pause_current_process()
            position = self.waiting_list.index(process)
            self.waiting_list[position] = None
            self.runnable_stack.append(process)
            process.state = State.runnable
            self.io_sys.move_process(process, len(self.runnable_stack) - 1)
            self.dispatch_next_process()


    def process_with_id(self, id):
        """Return the process with the id."""
        with self.mutex:
            for process in self.runnable_stack:
                if process.id == id:
                    return process
            for process in self.waiting_list:
                if process and process.id == id:
                    return process
        return None
