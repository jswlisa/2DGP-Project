from pico2d import load_image, draw_rectangle
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_LCTRL, SDLK_LSHIFT, SDLK_LALT
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

def alt_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LALT

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
    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self,e):
        # self.boy.dir = 0
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.boy.x += self.boy.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 50, self.boy.y + 10,
                297 * 1.45, 168 * 1.45)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h',
                self.boy.x - 50, self.boy.y + 10, 297 * 1.45, 168 * 1.45)


class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.dir = 0

    def exit(self,e):
        self.boy.dir = 0

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.idle_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 15, self.boy.y + 10,
                297 * 1.6, 168 * 1.6)
        else:
            self.boy.idle_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h', self.boy.x - 15,
                self.boy.y + 10, 297 * 1.6, 168 * 1.6)

class Attack:
    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.frame = 0
        self.boy.dir = 0

    def exit(self,e):
        self.boy.dir = 0

    def do(self):
        self.boy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # Attack 애니메이션 한 번만 실행 (5프레임 정도로 제한)
        if self.boy.frame >= 5:
            self.boy.frame = 0
            # Attack이 끝나면 Idle로 자동 전환
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))  # TIMEOUT 이벤트를 발생시켜 상태 전환

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.boy_attack_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 60, self.boy.y,
                297 * 1.8, 168 * 1.8)
        else:
            self.boy.boy_attack_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h', self.boy.x - 60,
                self.boy.y, 297 * 1.8, 168 * 1.8)

class Skill:
    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.frame = 0
        self.boy.dir = 0

    def exit(self,e):
        self.boy.dir = 0

    def do(self):
        self.boy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # Skill 애니메이션 한 번만 실행 (5프레임 정도로 제한)
        if self.boy.frame >= 5:
            self.boy.frame = 0
            # Skill이 끝나면 Idle로 자동 전환
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))  # TIMEOUT 이벤트를 발생시켜 상태 전환
            return

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.boy_skill_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168,
                self.boy.x + 80, self.boy.y + 30, 297 * 1.9, 168 * 1.9)
        else: # face_dir == -1: # left
            self.boy.boy_skill_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h',
                self.boy.x - 80, self.boy.y + 30, 297 * 1.9, 168 * 1.9)

class Jump:
    def __init__(self, boy):
        self.boy = boy
        self.jump_speed = 700.0  # 초기 점프 속도 (pixels/sec)
        self.gravity = -2000.0  # 중력 가속도 (pixels/sec^2)
        self.horizontal_speed = WALK_SPEED_PPS

    def enter(self, e):
        # 땅에 있을 때만 점프 가능
        if self.boy.y <= self.boy.ground_y + 1:
            self.boy.vy = self.jump_speed

        # 방향키 입력시
        if self.boy.dir > 0:
            self.boy.dir = 1
            self.boy.face_dir = 1
        elif self.boy.dir < 0:
            self.boy.dir = -1
            self.boy.face_dir = -1
        else:
            # 방향키 누른 상태가 아니면 제자리 점프
            self.boy.dir = 0

        self.boy.frame = 0

    def exit(self, e):
        self.boy.vy = 0
        self.boy.dir = 0

    def do(self):
        ft = game_framework.frame_time

        # 물리 계산
        self.boy.vy += self.gravity * ft
        self.boy.y += self.boy.vy * ft

        # 수평 이동 (self.boy.dir이 0이면 이동 안 함)
        self.boy.x += self.boy.dir * self.horizontal_speed * ft

        # 애니메이션
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 5

        # 착지 체크
        if self.boy.y <= self.boy.ground_y:
            self.boy.y = self.boy.ground_y
            self.boy.vy = 0
            self.boy.dir = 0
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.idle_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168,
                self.boy.x + 15, self.boy.y + 10, 297 * 1.6, 168 * 1.6)
        else:
            self.boy.idle_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h',
                self.boy.x - 15, self.boy.y + 10, 297 * 1.6, 168 * 1.6)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 180
        self.frame = 0
        self.face_dir = 1
        self.dir = 0

        # 수직 물리 속성 추가
        self.vy = 0
        self.ground_y = 180

        self.image = load_image('boy_walk.png')
        self.idle_image = load_image('boy_idle.png')
        self.boy_attack_image = load_image('boy_attack.png')
        self.boy_skill_image = load_image('boy_skill.png')

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.SKILL = Skill(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                            ctrl_down: self.ATTACK, shift_down: self.SKILL, alt_down: self.JUMP},
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE,
                           ctrl_down: self.ATTACK, ctrl_up: self.ATTACK, alt_down: self.JUMP},
                self.ATTACK: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                             timeout: self.IDLE},
                self.SKILL: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                            timeout: self.IDLE}, # TIMEOUT 이벤트가 발생하면 IDLE 상태로 전환
                self.JUMP: {timeout: self.IDLE} # TIMEOUT 이벤트가 발생하면 IDLE 상태로 전환
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 100, self.x + 40, self.y + 80