import cannons
import random
import time
import menu
import Queue

half_a = cannons.Cannon([1,2,3], .05)
half_b = cannons.Cannon([4,5,6], .05)

c1 = cannons.Cannon([1], .05)
c2 = cannons.Cannon([2], .05)
c3 = cannons.Cannon([3], .05)
c4 = cannons.Cannon([4], .05)
c5 = cannons.Cannon([5], .05)
c6 = cannons.Cannon([6], .05)

cannon_list = [c1,c2,c3,c4,c5,c6]

def run_demo(in_q):
    try:
        for i in range(0, 30):
            half_a.fire()
            time.sleep(.1)
            half_b.fire()
            menu.pause_callback(in_q, 'demo')
        while True:
            fire = random.choice(cannon_list)
            fire.fire()
            time.sleep(.05)
            menu.pause_callback(in_q, 'demo')
    except Exception as e:
        print(e)
        cannons.GPIO.cleanup()
        menu.MENU.reset()