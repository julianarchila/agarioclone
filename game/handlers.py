import pygame 
import math

from pygame.event import Event
from game_state import STATE
from constants import WIN_H, WIN_W


def handle_events(event: Event):
    # print(event)
    if event.type == pygame.QUIT:
        STATE.goOn = False

