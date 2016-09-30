import cannons
import random
import time
import menu
import Queue
import audio

NUMBER_OF_CANNONS = []
for x in range(70):
    NUMBER_OF_CANNONS.append(1)
for x in range(20):
    NUMBER_OF_CANNONS.append(3)
for x in range(10):
    NUMBER_OF_CANNONS.append(6)

FIRE_DURATION = 1

def play_round(in_q):
    cannon_quantity = random.choice(NUMBER_OF_CANNONS)
    cannon_list = [1, 2, 3, 4, 5, 6]
    choosen_cannons = []
    for x in range(cannon_quantity):
        cannon = random.choice(cannon_list)
        choosen_cannons.append(cannon)
        cannon_list.remove(cannon)
    menu.pause_callback(in_q, 'game')
    announce_round(in_q, 'wait')
    choosen_cannons = cannons.Cannon(choosen_cannons, FIRE_DURATION)
    fire_tease(in_q)
    choosen_cannons.fire()

def fire_tease(in_q):
    clips = ['gameover', 'kraken', 'redalert', 'lucky', 'turret-target']
    clip = audio.load(random.choice(clips))
    clip.play()
    while clip.get_busy():
        menu.pause_callback(in_q, 'game')
        continue

def announce_round(in_q, round):
    if round == 'wait':
        clip = audio.load('ticktock')
    else:
        clip = audio.load('r{}'.format(round))
    clip.play()
    while clip.get_busy():
        menu.pause_callback(in_q, 'game')
        continue

def play(in_q):
    rounds = 1
    start = audio.load('duckhunt')
    start.play()
    while start.get_busy():
        menu.pause_callback(in_q, 'game')
        continue
    while rounds < 11:
        announce_round(in_q, rounds)
        play_round(in_q)
        rounds += 1
    menu.MENU.reset()