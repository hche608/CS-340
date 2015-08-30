import threading
import _thread
from random import randint
from time import sleep
from enum import Enum

Type = Enum("Type", "background interactive")
State = Enum("State", "runnable waiting killed")

"""
class Type():
    background, interactive = range(2)
"""

class Process(threading.Thread):
    """A process."""

    next_id = 1

    def __init__(self, iosys, dispatcher, type):
        """Construct a process.
        iosys - the io subsystem so the process can do IO
        dispatcher - so that the process can notify the dispatcher
        type - whether background or interactive
        """
        threading.Thread.__init__(self)
        self.id = Process.next_id
        Process.next_id += 1
        self.iosys = iosys
        self.dispatcher = dispatcher
        self.type = type
        # self.state = State.runnable
        self.panel = None
        self.block_event = threading.Event()
        self.daemon = True

    def run(self):
        """Start the process running."""
        if self.type == Type.background:
            self.run_background()
        elif self.type == Type.interactive:
            self.run_interactive()
        self.dispatcher.proc_finished(self)

    def run_interactive(self):
        """Run as an interactive process."""
        self.block_event.wait() # why is this line here?
        loops = self.ask_user()
        while loops > 0:
            for i in range(loops):
                self.main_process_body()
            self.iosys.write(self, "\n")
            loops = self.ask_user()

    def run_background(self):
        """Run as a background process."""
        loops = randint(10, 160)
        for i in range(loops):
            self.main_process_body()

    def ask_user(self):
        """Ask the user for number of loops."""
        self.iosys.write(self, "How many loops? ")
        input = self.iosys.read(self)
        if self.state == State.killed:
            _thread.exit()
        return int(input)

    def main_process_body(self):
        self.block_event.wait() # waits here until told to progress
        # check to see if supposed to terminate
        if self.state == State.killed:
            _thread.exit()
        self.iosys.write(self, "*")
        sleep(0.1)
