# You are not allowed to use any sleep calls.

from process import State
import curses
import curses.panel
import sys

WINDOW_HEIGHT = 4
WINDOW_WIDTH = 40

# Only one of these is created and is sent to each process.
# The processes always print and get input via this.

class IO_Sys():
    """The IO subsystem of the SOS."""

    def __init__(self, the_dispatcher, panels):
        """Construct an io system.
        the_dispatcher - the dispatcher
        panels - the curses panels for the program
        """
        self.the_dispatcher = the_dispatcher
        self.panels = panels
        self.process_buffers = dict()    # each process can have an input buffer
        self.runnable_window_boxes = []  # the boxes for the runnable process windows
        self.waiting_windows_boxes = []  # the boxes for waiting process windows
        y = 2
        for i in range(self.the_dispatcher.MAX_PROCESSES):
            self.runnable_window_boxes.append(Process_Window_Box(y, 0, self.panels))
            y += WINDOW_HEIGHT + 2
        y = 2
        for i in range(self.the_dispatcher.MAX_PROCESSES):
            self.waiting_windows_boxes.append(Process_Window_Box(y, WINDOW_WIDTH + 2 + 1, self.panels))
            y += WINDOW_HEIGHT + 2
        self.process_window_box = dict()        # the window box, just for the name
        self.refresh_screen()

    def allocate_window_to_process(self, process, tos):
        """Creates a new process window for the process.
        All processes get created at the top of the runnable stack. Why?
        """
        window = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH)
        window.scrollok(True)
        panel = curses.panel.new_panel(window)
        self.panels.append(panel)
        process.panel = panel
        self.move_process(process, tos)

    def remove_window_from_process(self, process):
        """Remove the process from this window."""
        self.process_window_box.pop(process).set_name("")
        panel = process.panel
        panel.window().erase()
        panel.window().refresh()
        # print("just erased window", file=sys.stderr)
        # panel.hide()
        process.panel = None
        self.panels.remove(panel)
        self.refresh_screen()

    def refresh_screen(self):
        """Refresh the screen contents."""
        curses.panel.update_panels()
        curses.doupdate()

    def move_process(self, process, position):
        """Change the process' window position.
        process     - the process identifier
        position    - the position in the corresponding window list
        """
        if process.state == State.runnable:
            window_box = self.runnable_window_boxes[position]
        else: # must be waiting
            window_box = self.waiting_windows_boxes[position]
        old_window_box = self.process_window_box.pop(process, None)
        if old_window_box:
            old_window_box.set_name("")
        self.process_window_box[process] = window_box
        window_box.set_name(str(process.id))
        new_location = window_box.get_contents_location()
        panel = process.panel
        panel.move(*new_location)
        self.refresh_screen()

    def swap_windows(self, processA, processB):
        """Swap the windows of processA with processB."""
        windowA = self.process_window_box[processA]
        windowB = self.process_window_box[processB]
        self.process_window_box[processA] = windowB
        windowB.set_name(str(processA.id))
        self.process_window_box[processB] = windowA
        windowA.set_name(str(processB.id))
        new_location = windowB.get_contents_location()
        processA.panel.move(*new_location)
        new_location = windowA.get_contents_location()
        processB.panel.move(*new_location)
        self.refresh_screen()

    def write(self, process, data):
        """Writes 'data' to the window associated with 'process'."""
        window = process.panel.window()
        window.addstr(data)
        self.refresh_screen()

    def fill_buffer(self, process, data):
        """Fill the process buffer with data."""
        self.process_buffers[process] = data
        self.the_dispatcher.wake_up_waiting_proc(process)

    def read(self, process):
        """Gets input from the window associated with 'process'."""
        # change the state of the process to waiting
        self.the_dispatcher.proc_waiting(process)
        process.block_event.wait() # waits until input
        data = self.process_buffers.pop(process, "-1") # get the data or -1 if none
        return data

# =======================================================================================================================

class Process_Window_Box():
    """Holds the window border information for a process."""

    def __init__(self, y, x, panels):
        """Construct a process window."""
        self.y = y
        self.x = x
        self.box_around_window = curses.newwin(WINDOW_HEIGHT + 2, WINDOW_WIDTH + 2, y, x)
        panel = curses.panel.new_panel(self.box_around_window)
        panels.append(panel)
        self.set_name("")

    def set_name(self, name):
        """Set the process name."""
        self.box_around_window.box()
        self.box_around_window.addstr(0, 2, " Process: ")
        self.box_around_window.addstr(0, 12, name + " ")
        # self.box_around_window.refresh()

    def get_contents_location(self):
        """Return the (y, x) location of the contents of this window box."""
        return (self.y+1, self.x+1)
