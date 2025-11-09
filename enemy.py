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
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h', self.enemy.x, self.enemy.y, 256 * 2, 145 * 2)

class Enemy:
    def __init__(self):
        self.x, self.y = 600, 220
        self.image = load_image('enemy.png')
        self.frame = 0
        self.dir = 0
        self.face_dir = -1

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE, self.IDLE
        )
    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
