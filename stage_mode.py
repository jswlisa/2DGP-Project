import game_framework
from pico2d import *
import play_mode

image = None

def pause():
    pass

def resume():
    pass

def init():
    global image

    image = load_image('그림1.png')

def finish():
    global image
    del image   # 메모리 소멸이라고 생각하면 됨
    pass

def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 4400, 2475, 600, 300, 1200, 600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)