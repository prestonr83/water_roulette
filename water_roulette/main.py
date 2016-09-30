import cannons
import audio
import menu
import time
import demo
import game


def wait_input():
    switcher = {
        'demo' : demo.run_demo,
        'game' : game.play
    }
    while True:
        if menu.MENU.done:
            selection_thread = menu.Thread(target=switcher[menu.MENU.selection],
                                           args=(menu.MENU.q,))
            selection_thread.start()
            selection_thread.join()

audio.load('system').play()

wait_input()