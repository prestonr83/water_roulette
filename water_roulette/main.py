from . import audio, menu, demo, game

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

audio.play('system', 1)

wait_input()