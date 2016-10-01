# -*- coding: utf-8 -*-
"""Provide functions for playing audio queues.

.. module: water_roulette.audio

"""
import os
import inspect
import pygame


#relative to package
MEDIA_PATH = 'media'
MODULE_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))

def play(audio_file, channel):
    """Supply name of audio file in media path
    
       Returns an audio object. Play the audio by calling play()"""
    audio_file = "{}/{}/{}.wav".format(MODULE_PATH, MEDIA_PATH, audio_file)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    channel = pygame.mixer.Channel(channel)
    sound = pygame.mixer.Sound(audio_file)
    channel.queue(sound)
    return channel