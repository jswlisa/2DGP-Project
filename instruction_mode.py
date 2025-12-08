from pico2d import *
import game_framework
import character_choose_mode

image = None
font = None


def init():
    global image, font
    try:
        image = load_image('ontheboat(1).png')
    except:
        image = None

    try:
        font = load_font('font.ttf', 40)
    except:
        font = None


def finish():
    global image, font
    if image:
        del image
    if font:
        del font


def update():
    pass


def draw():
    clear_canvas()

    image.draw(600, 300)
    font.draw(500, 500, "HOW TO PLAY", (10, 255, 10))

    font.draw(350, 400, "MOVE : Arrow Keys (Left/Right)", (255, 255, 255))
    font.draw(350, 350, "JUMP : 'Alt'", (255, 255, 255))
    font.draw(350, 300, "ATTACK : 'Ctrl'", (255, 255, 255))
    font.draw(350, 250, "SKILL : 'Shift'", (255, 255, 255))
    font.draw(350, 200, "Exit : 'ESC'", (255, 255, 255))

    font.draw(400, 100, "Press 'SPACE' to Start", (255, 100, 100))

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_mode(character_choose_mode)


def pause(): pass


def resume(): pass