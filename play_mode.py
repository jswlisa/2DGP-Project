import random
from pico2d import *

import game_framework
import game_world

from girl import Girl
from boy import Boy
from waterfront import WaterFront
from enemy import Enemy

girl = None
boy = None
girl_state = True
boy_state = False

def handle_events():
    global girl_state, boy_state

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            girl_state = True
            boy_state = False
            if boy in game_world.world[1]:
                game_world.remove_object(boy)
            if girl not in game_world.world[1]:
                game_world.add_object(girl, 1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            boy_state = True
            girl_state = False
            if girl in game_world.world[1]:
                game_world.remove_object(girl)
            if boy not in game_world.world[1]:
                game_world.add_object(boy, 1)

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if girl_state:
                girl.handle_event(event)
            elif boy_state:
                boy.handle_event(event)

def init():
    global girl
    global boy

    waterfront = WaterFront()
    game_world.add_object(waterfront, 0)

    enemy = Enemy()
    game_world.add_object(enemy, 1)

    girl = Girl()
    # game_world.add_object(girl, 1)

    boy = Boy()
    # game_world.add_object(boy, 1)

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