from . import cannons, menu
import random
import time

HALF_A = cannons.Cannon([1,2,3], .05)
HALF_B = cannons.Cannon([4,5,6], .05)

C1 = cannons.Cannon([1], .05)
C2 = cannons.Cannon([2], .05)
C3 = cannons.Cannon([3], .05)
C4 = cannons.Cannon([4], .05)
C5 = cannons.Cannon([5], .05)
C6 = cannons.Cannon([6], .05)

CANNON_LIST = [C1,C2,C3,C4,C5,C6]

PAUSE = menu.pause_callback

def run_demo(in_q):
    try:
        for _ in range(30):
            HALF_A.fire()
            time.sleep(.1)
            HALF_B.fire()
            PAUSE(in_q, 'demo')
        while True:
            fire = random.choice(CANNON_LIST)
            fire.fire()
            time.sleep(.05)
            PAUSE(in_q, 'demo')
    except Exception as e:
        print(e)
        cannons.GPIO.cleanup()
        menu.MENU.reset()