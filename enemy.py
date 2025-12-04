from pico2d import *
from state_machine import StateMachine

import game_framework

# enemy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# enemy Action Speed
TIME_PER_ACTION = 1.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

def timeout(e):
    return e[0] == 'TIMEOUT'

class Idle:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self,e):
        self.enemy.dir = 0

    def exit(self,e):
        self.enemy.dir = 0

    def do(self):
        self.enemy.frame = (self.enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 145, self.enemy.x, self.enemy.y, 256 * 2, 145 * 2)
        else:
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h',
                self.enemy.x, self.enemy.y, 256 * 2, 145 * 2)

class Hit:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self,e):
        self.enemy.dir = 0
        self.enemy.hp -= 76
        if self.enemy.hp < 0:
            self.enemy.hp = 0

    def exit(self,e):
        self.enemy.dir = 0

    def do(self):
        self.enemy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        if self.enemy.frame >= 10:
            self.enemy.frame = 0
            self.enemy.state_machine.handle_state_event(('TIMEOUT', 0))  # TIMEOUT 이벤트를 발생시켜 상태 전환
            return

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.enmey_hit_image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 145, self.enemy.x - 70, self.enemy.y - 40, 256 * 1.7, 145 * 1.7)
        else:
            self.enemy.enmey_hit_image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h',
                self.enemy.x + 70, self.enemy.y - 40, 256 * 1.7, 145 * 1.7)

class Enemy:
    def __init__(self):
        self.x, self.y = 600, 220
        self.image = load_image('enemy.png')
        self.enmey_hit_image = load_image('enemy_hit.png')
        self.enemy_hp_image = load_image('hp_sprite.png')
        self.frame = 0
        self.dir = 0
        self.face_dir = -1
        self.hp = 456

        self.IDLE = Idle(self)
        self.HIT = Hit(self)
        self.state_machine = StateMachine(
            self.IDLE, {
            self.HIT : {timeout: self.IDLE}
            }
        )
    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        max_sprite_y = 456
        frame_height = 76

        delta = max_sprite_y - self.hp
        if delta <= 0:
            frame_index = 0
        else:
            frame_index = math.ceil(delta / frame_height)

        y = max_sprite_y - frame_index * frame_height
        if y < 0:
            y = 0

        self.enemy_hp_image.clip_draw(0, y, 426, 76, 1000, 550, 426 // 2, 76 // 2)

    def get_bb(self):
        return self.x + 20, self.y - 110, self.x + 130, self.y + 50

    def handle_collision(self, group, other):
        pass