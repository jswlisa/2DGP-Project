from pico2d import load_image
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_LCTRL, SDLK_LSHIFT
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

def ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def ctrl_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

def shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def shift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT

def timeout(e):
    return e[0] == 'TIMEOUT'

# Girl의 Walk Speed 계산

# Girl Walk Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
WALK_SPEED_KMPH = 20.0  # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

# Girl Action Speed
TIME_PER_ACTION = 0.9
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
            self.girl.image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x, self.girl.y, 297 * 1.5, 168 * 1.5)
        else: # face_dir == -1: # left
            self.girl.image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x, self.girl.y, 297 * 1.5, 168 * 1.5)


class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        self.girl.dir = 0

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.idle_image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x + 15, self.girl.y + 10, 297 * 1.6, 168 * 1.6)
        else:
            self.girl.idle_image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x - 15, self.girl.y + 10, 297 * 1.6, 168 * 1.6)

class Attack:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        self.girl.frame = 0
        self.girl.dir = 0

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # Attack 애니메이션 한 번만 실행 (5프레임 정도로 제한)
        if self.girl.frame >= 5:
            self.girl.frame = 0
            # Attack이 끝나면 Idle로 자동 전환
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))  # TIMEOUT 이벤트를 발생시켜 상태 전환

    def draw(self):
        # 캐릭터 공격 모션 먼저 그리기
        if self.girl.face_dir == 1: # right
            self.girl.girl_attack_image.clip_draw(int(self.girl.frame) * 269, 0, 269, 185, self.girl.x, self.girl.y, 269 * 1.5, 185 * 1.5)
        else: # face_dir == -1: # left
            self.girl.girl_attack_image.clip_composite_draw(int(self.girl.frame) * 269, 0, 269, 185, 0, 'h', self.girl.x, self.girl.y, 269 * 1.5, 185 * 1.5)

        # 이펙트는 약간 지연된 프레임으로 그리기
        effect_frame = max(0, int(self.girl.frame - 1.5))  # 지연된 프레임
        if self.girl.face_dir == 1:
            self.girl.attack_effect_image.clip_draw(effect_frame * 558, 0, 558, 466, self.girl.x + 80, self.girl.y, 558//3, 466//3)
        else:
            self.girl.attack_effect_image.clip_composite_draw(effect_frame * 558, 0, 558, 466, 0, 'h', self.girl.x - 80, self.girl.y, 558 // 3, 466 // 3)

class Skill:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        self.girl.frame = 0
        self.girl.dir = 0

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # Skill 애니메이션 한 번만 실행 (5프레임 정도로 제한)
        if self.girl.frame >= 5:
            self.girl.frame = 0
            # Skill이 끝나면 Idle로 자동 전환
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))  # TIMEOUT 이벤트를 발생시켜 상태 전환
            return

    def draw(self):
        if self.girl.face_dir == 1: # right
            self.girl.girl_skill_image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x + 40, self.girl.y + 30, 297 * 3, 168 * 3)
        else: # face_dir == -1: # left
            self.girl.girl_skill_image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x - 40, self.girl.y + 30, 297 * 3, 168 * 3)

class Girl:
    def __init__(self):
        self.x, self.y = 400, 180
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('girl.png')
        self.idle_image = load_image('girl_idle.png')
        self.girl_attack_image = load_image('girl_attack.png')
        self.attack_effect_image = load_image('attack_effect.png')
        self.girl_skill_image = load_image('girl_skill.png')

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.SKILL = Skill(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                            ctrl_down: self.ATTACK, shift_down: self.SKILL},
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE,
                            ctrl_down: self.ATTACK, ctrl_up: self.ATTACK},
                self.ATTACK: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                              timeout: self.IDLE}, # TIMEOUT 이벤트가 발생하면 IDLE 상태로 전환
                self.SKILL: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                             timeout: self.IDLE}  # TIMEOUT 이벤트가 발생하면 IDLE 상태로 전환
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()