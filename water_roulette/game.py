from . import cannons, menu, audio
import random


NUMBER_OF_CANNONS = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]

FIRE_DURATION = 1

PAUSE = menu.pause_callback

def play_round(in_q):
    cannon_quantity = random.choice(NUMBER_OF_CANNONS)
    cannon_list = [1, 2, 3, 4, 5, 6]
    choosen_cannons = []
    for x in range(cannon_quantity):
        cannon = random.choice(cannon_list)
        choosen_cannons.append(cannon)
        cannon_list.remove(cannon)
    PAUSE(in_q, 'game')
    announce_round(in_q, 'wait')
    choosen_cannons = cannons.Cannon(choosen_cannons, FIRE_DURATION)
    fire_tease(in_q)
    choosen_cannons.fire()

def fire_tease(in_q):
    clips = ['gameover', 'kraken', 'redalert', 
             'lucky', 'turret-target', 'firewhenready']
    clip = audio.play(random.choice(clips), 2)
    while clip.get_busy():
        PAUSE(in_q, 'game', clip=clip)
        clip.unpause()
        continue


def announce_round(in_q, round):
    if round == 'wait':
        clip = audio.play('ticktock', 2)
    else:
        clip = audio.play('r{}'.format(round), 2)
    while clip.get_busy():
        PAUSE(in_q, 'game', clip=clip)
        clip.unpause()
        continue

def play(in_q):
    rounds = 1
    start = audio.play('duckhunt', 2)
    while start.get_busy():
        PAUSE(in_q, 'game', clip=start)
        start.unpause()
        continue
    while rounds < 11:
        announce_round(in_q, rounds)
        play_round(in_q)
        rounds += 1
    menu.MENU.reset()