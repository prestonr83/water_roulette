from . import cannons, audio
from Queue import Queue, Empty
from threading import Thread, Event
import time
import sys

BUTTON_TIME = time.time()

def callback():
    MENU.threads += -1
    if not MENU.selection:
        MENU.prompt()
        timeout_thread = Thread(target=timeout)
        timeout_thread.start()
    if MENU.threads > 0:
        return
    if MENU.timeout:
        MENU.evt.set()
        MENU.q.put((MENU.selection, MENU.evt))
        MENU.done = True
        return
    MENU.prompt()

def timeout():
    MENU.threads += 1
    MENU.timeout = True
    time.sleep(3)
    callback()
    return

def button_callback(channel):
    global BUTTON_TIME
    if time.time() - BUTTON_TIME > .2:
        BUTTON_TIME = time.time()
        MENU.timeout = False
        MENU.prompt()
        if MENU.selection != 'Pause':
            timeout_thread = Thread(target=timeout)
            timeout_thread.start()


class MenuOptions(object):
    def __init__(self):
        self.threads = 0
        self.selection = None
        self.timeout = False
        self.done = False
        self.q = Queue()
        self.evt = Event()

    def prompt(self):
        if self.done:
            self.pause_menu()
            return
        self.main_menu()
        return

    def pause_menu(self):
        if self.evt.isSet():
            self.selection = 'Pause'
            self.evt.clear()
            self.q.put((self.selection, self.evt))
            audio.play('pause', 1)
            return
        if not self.evt.isSet():
            if self.selection in ['Pause', 'Exit']:
                self.selection = 'Resume'
                audio.play('resume', 1)
                return
            if self.selection == 'Resume':
                self.selection = 'Reset'
                audio.play('reset', 1)
                return
            if self.selection == 'Reset':
                self.selection = 'Exit'
                audio.play('exit', 1)
                return

    def main_menu(self):
        if self.selection != "game":
            self.selection = "game"
            audio.play('new_game', 1)
            return
        if self.selection != "demo":
            self.selection = "demo"
            audio.play('demo', 1)
            return

    def reset(self):
        self.threads = 0
        self.selection = None
        self.timeout = False
        self.done = False
        self.q = Queue()
        self.evt = Event()

def pause_callback(in_q, selection, clip=None):
    try:
        data, evt = in_q.get_nowait()
    except Empty:
        return
    if data == 'Pause':
        if clip:
            clip.pause()
        evt.wait()
        pause_callback(in_q, selection, clip=clip)
    if data == 'Reset':
        if clip:
            clip.stop()
        MENU.selection = selection
        sys.exit(0)
    if data == 'Exit':
        if clip:
            clip.stop()
        MENU.reset()
        audio.play('menu', 1)
        sys.exit(0)



MENU = MenuOptions()

cannons.GPIO.setup(25, cannons.GPIO.IN, pull_up_down=cannons.GPIO.PUD_UP)
cannons.GPIO.add_event_detect(25, cannons.GPIO.FALLING, 
                              callback=button_callback, bouncetime=200)