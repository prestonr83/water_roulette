import cannons
import audio
import time
import threading

audio.ENGINE.say('Loading')
audio.ENGINE.runAndWait()

def menu_callback():
    print('running callback')
    menu.threads += -1
    if menu.mode != 'ready':
        return
    print('Threads: {}'.format(menu.threads))
    if menu.timeout is False or menu.threads > 0 or menu.selection == 0:
        return
    if menu.result['selected'] is None and menu.duration is None:
        print("selected in result running prompt")
        menu.prompt()
        return
    if menu.result['duration'] is None and menu.threads < 1:
        print("last prompt ran")
        if menu.duration == 0:
            menu.duration = 1
        menu.result['duration'] = menu.duration
        menu.prompt()
        
def timeout(mode):
    if mode == 'all' or mode == 'normal':
        time.sleep(3)
        menu.set_mode(expired=True)
        return
    print('running thread')
    menu.threads += 1
    menu.timeout = True
    time.sleep(3)
    print('done sleeping')
    menu_callback()
    return

BUTTON_TIME = time.time()

def button_callback(channel):
    global BUTTON_TIME
    if time.time() - BUTTON_TIME > .2:
        menu.timeout = False
        menu.prompt()
        print("button pushed")
        timeout_thread = threading.Thread(target=timeout, args=('ready',))
        timeout_thread.start()
        BUTTON_TIME = time.time()

class MenuOptions(object):
    def __init__(self):
        self.threads = 0
        self.selection = None
        self.duration = None
        self.timeout = False
        self.result = {'selected' : None,
                       'duration' : None}
        self.mode = None

    def prompt(self):
        if self.mode != 'ready':
            self.set_mode(expired=False)
        print("Timeout: {}".format(self.timeout))
        if self.selection is None:
            audio.ENGINE.say('Press again to select a cannon')
            audio.ENGINE.runAndWait()
            self.selection = 0
            return
        self.cannon()

    def set_mode(self, expired):
        if expired == True:
            if self.mode == 'all':
                fire('all', 1)
                return
            self.mode = 'ready'
            self.prompt()
            return
        if self.mode is None or self.mode is 'all':
            audio.ENGINE.say('Cannon and duration')
            audio.ENGINE.runAndWait()
            self.mode = 'normal'
            timeout_thread = threading.Thread(target=timeout, args=('normal',))
            timeout_thread.start()
            return
        audio.ENGINE.say('All Cannons')
        audio.ENGINE.runAndWait()
        self.mode = 'all'
        timeout_thread = threading.Thread(target=timeout, args=('all',))
        timeout_thread.start()

    def cannon(self):
        if self.timeout is True:
            if self.result['duration']:
                fire(self.result['selected'], self.result['duration'])
                return
            self.result['selected'] = self.selection
            self.timeout = False
            self.time()
            return
        if self.result['selected'] is not None:
            self.time()
            return
        if self.selection < 6:
            self.selection += 1
            audio.ENGINE.say('Cannon {}'.format(self.selection))
            audio.ENGINE.runAndWait()
            return
        if self.selection == 6:
            self.selection = 1
            audio.ENGINE.say('Cannon {}'.format(self.selection))
            audio.ENGINE.runAndWait()
            return

    def time(self):
        if self.duration is None:
            audio.ENGINE.say('Press again to set a duration')
            audio.ENGINE.runAndWait()
            self.duration = 0
            timeout_thread = threading.Thread(target=timeout)
            timeout_thread.start()
            return
        if self.duration < 6:
            self.duration += 1
            audio.ENGINE.say('{} seconds'.format(self.duration))
            audio.ENGINE.runAndWait()
            return
        if self.duration == 6:
            self.duration = 1
            audio.ENGINE.say('{} second'.format(self.duration))
            audio.ENGINE.runAndWait()
            return
    
    def reset(self):
        print('reset ran')
        self.selection = None
        self.duration = None
        self.timeout = False
        self.result = {'selected' : None,
                       'duration' : None}

menu = MenuOptions()


def fire(cannon, duration):
    if cannon == 'all':
        can = cannons.Cannon(1,1)
        can.fire_all()
    can = cannons.Cannon(cannon,duration)
    can.fire()
    menu.reset()
cannons.GPIO.setup(25, cannons.GPIO.IN, pull_up_down=cannons.GPIO.PUD_UP)
cannons.GPIO.add_event_detect(25, cannons.GPIO.FALLING, callback=button_callback, bouncetime=200)

inc = 0
while True:
    inc += 1
    reset = time.time() - BUTTON_TIME
    if inc > 100:
        print('time since button push: {}'.format(reset))
        inc = 0
    if reset > 20:
        menu.reset()
        BUTTON_TIME = time.time()
    time.sleep(.05)
