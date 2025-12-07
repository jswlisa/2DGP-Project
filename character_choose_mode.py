from pico2d import *
import game_framework
import play_mode


def pause(): pass


def resume(): pass


def init():
    global image
    image = load_image('character_choose.png')


def finish():
    global image
    del image


def update():
    pass


def draw():
    clear_canvas()
    image.draw(600, 300, 1200, 600)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        # 1번 키: Girl 선택
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            play_mode.character_choice = 'Girl'
            game_framework.change_mode(play_mode)

        # 2번 키: Boy 선택
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            play_mode.character_choice = 'Boy'
            game_framework.change_mode(play_mode)