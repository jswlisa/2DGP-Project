from pico2d import load_image, get_time
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT
from state_machine import StateMachine

import game_world
import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

# Girl의 Walk Speed 계산

# Girl Walk Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
WALK_SPEED_KMPH = 20.0  # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

# Girl Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Walk:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_down(e) or right_up(e):
            self.girl.dir = self.girl.face_dir = -1

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.girl.x += self.girl.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.girl.face_dir == 1: # right
            self.girl.image.clip_draw(int(self.girl.frame) * 256, 0, 256, 145, self.girl.x, self.girl.y)
        else: # face_dir == -1: # left
            self.girl.image.clip_composite_draw(int(self.girl.frame) * 256, 0, 256, 145, 0, 'h', self.girl.x, self.girl.y, 256, 145)


class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        self.girl.dir = 0

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.girl.x += self.girl.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.image.clip_draw(int(self.girl.frame) * 256, 0, 256, 145, self.girl.x, self.girl.y, 256, 145)
        else:
            self.girl.image.clip_composite_draw(int(self.girl.frame) * 256, 0, 256, 145, 0, 'h', self.girl.x, self.girl.y, 256, 145)



class Girl:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('girl.png')

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK},
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()