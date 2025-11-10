import random
from pico2d import *

import game_framework
import game_world

from girl import Girl
from waterfront import WaterFront
from enemy import Enemy

girl = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            girl.handle_event(event)

def init():
    global girl

    waterfront = WaterFront()
    game_world.add_object(waterfront, 0)

    enemy = Enemy()
    game_world.add_object(enemy, 1)

    girl = Girl()
    game_world.add_object(girl, 1)

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass