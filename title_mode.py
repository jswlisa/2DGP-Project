import game_framework
from pico2d import *

import instruction_mode

image = None

def pause():
    pass

def resume():
    pass

def init():
    global image, font
    image = load_image('title.png')
    font = load_font('font.ttf', 40)

def finish():
    global image
    del image
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(600, 300)
    font.draw(400, 100, "Press 'SPACE' to Start", (255, 100, 100))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(instruction_mode)