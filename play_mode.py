from pico2d import *
import game_framework
import game_world

from girl import Girl
from boy import Boy
from waterfront import WaterFront
from enemy import Enemy

character_choice = 'Girl'

stage = 1
clear_image = None
is_cleared = False
clear_timer = 0.0

ui_font = None
game_over_font = None
stage_message_font = None
is_game_over = False

bgm = None

stage_message = ""
message_timer = 0.0

girl = None
boy = None


def init():
    global girl, boy
    global character_choice
    global clear_image, is_cleared, clear_timer
    global stage
    global ui_font, game_over_font, stage_message_font, is_game_over
    global bgm

    try:
        if clear_image is None:
            clear_image = load_image('game_clear.png')
    except:
        print("game_clear.png 이미지를 찾을 수 없습니다.")
        clear_image = None

    try:
        if ui_font is None:
            ui_font = load_font('font.ttf', 40)
        if game_over_font is None:
            game_over_font = load_font('font.ttf', 100)
        if stage_message_font is None:
            stage_message_font = load_font('font.ttf', 50)
    except:
        print("'font.ttf' 파일을 찾을 수 없습니다!")
        ui_font = None
        game_over_font = None
        stage_message_font = None

    is_cleared = False
    is_game_over = False
    clear_timer = 0.0

    waterfront = WaterFront()
    game_world.add_object(waterfront, 0)

    create_enemy_by_stage(stage)

    if character_choice == 'Girl':
        girl = Girl()
        game_world.add_object(girl, 1)
        boy = None
        for obj in game_world.world[1]:
            if isinstance(obj, Enemy):
                game_world.add_collision_pair('girl:enemy', girl, obj)

    elif character_choice == 'Boy':
        boy = Boy()
        game_world.add_object(boy, 1)
        girl = None
        for obj in game_world.world[1]:
            if isinstance(obj, Enemy):
                game_world.add_collision_pair('boy:enemy', boy, obj)


def finish():
    global clear_image
    global bgm

    game_world.clear()
    pass


def update():
    global is_cleared, clear_timer, stage, is_game_over

    game_world.update()
    game_world.handle_collisions()

    if not is_game_over:
        if girl and girl.state_machine.cur_state == girl.DIE:
            is_game_over = True
            print("상태 변경: GAME OVER")
        elif boy and boy.state_machine.cur_state == boy.DIE:
            is_game_over = True
            print("상태 변경: GAME OVER")

    if not is_game_over:
        enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]

        all_dead = True
        if not enemies:
            all_dead = True
        else:
            for e in enemies:
                if e.state_machine.cur_state != e.DIE:
                    all_dead = False
                    break

        if all_dead and not is_cleared:
            is_cleared = True
            clear_timer = get_time()
            print(f"상태 변경: Stage {stage} Cleared!")

        if is_cleared:
            if get_time() - clear_timer > 3.0:
                stage += 1
                restart_game()


def draw():
    clear_canvas()
    game_world.render()

    if ui_font:
        ui_font.draw(540, 550, f"STAGE {stage}", (255, 255, 255))

    if is_cleared:
        if clear_image:
            clear_image.draw(600, 300)
        else:
            if ui_font: ui_font.draw(500, 400, "STAGE CLEAR!", (0, 255, 0))

    if stage_message and not is_cleared and not is_game_over:
        if get_time() - message_timer < 3.0:
            if stage_message_font:
                stage_message_font.draw(500, 400, stage_message, (255, 255, 0))

    if is_game_over:
        if game_over_font:
            game_over_font.draw(450, 300, "GAME OVER", (255, 0, 0))

            if stage_message_font:
                stage_message_font.draw(350, 200, "Press 'R' to Restart 'ESC' to Exit", (255, 255, 255))

    update_canvas()


def handle_events():
    global stage, is_game_over
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            if is_game_over:
                stage = 1
                is_game_over = False
                restart_game()

        else:
            if not is_game_over:
                if girl: girl.handle_event(event)
                if boy: boy.handle_event(event)


def pause(): pass


def resume(): pass



def create_enemy_by_stage(current_stage):
    global stage_message, message_timer

    stage_message = f"STAGE {current_stage} START!"
    message_timer = get_time()

    if current_stage == 1:
        enemy = Enemy()
        game_world.add_object(enemy, 1)
    else:
        enemy1 = Enemy()
        enemy1.x = 800
        enemy1.hp = 456 + (current_stage * 50)
        game_world.add_object(enemy1, 1)

        if current_stage >= 3:
            enemy2 = Enemy()
            enemy2.x = 1000
            enemy2.hp = 456 + (current_stage * 50)
            game_world.add_object(enemy2, 1)


def restart_game():
    game_world.clear()
    init()