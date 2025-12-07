from pico2d import load_image, draw_rectangle, clamp
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_LCTRL, SDLK_LSHIFT, SDLK_LALT
from state_machine import StateMachine
import math
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


def hit_event(e):
    return e[0] == 'HIT'


def die_event(e):
    return e[0] == 'DIE'


PIXEL_PER_METER = (10.0 / 0.3)
WALK_SPEED_KMPH = 20.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Walk:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.boy.x += self.boy.dir * WALK_SPEED_PPS * game_framework.frame_time
        self.boy.x = clamp(50, self.boy.x, 1200 - 50)

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 50, self.boy.y + 10,
                                     297 * 1.45, 168 * 1.45)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h', self.boy.x - 50,
                                               self.boy.y + 10, 297 * 1.45, 168 * 1.45)


class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
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

    def enter(self, e):
        self.boy.frame = 0
        self.boy.dir = 0

    def exit(self, e):
        self.boy.dir = 0

    def do(self):
        self.boy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.boy.frame >= 5:
            self.boy.frame = 0
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.boy_attack_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 60, self.boy.y,
                                                297 * 1.8, 168 * 1.8)
        else:
            self.boy.boy_attack_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h',
                                                          self.boy.x - 60, self.boy.y, 297 * 1.8, 168 * 1.8)


class Skill:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.frame = 0
        self.boy.dir = 0

    def exit(self, e):
        self.boy.dir = 0

    def do(self):
        self.boy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.boy.frame >= 5:
            self.boy.frame = 0
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))
            return

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.boy_skill_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 80, self.boy.y + 30,
                                               297 * 1.9, 168 * 1.9)
        else:
            self.boy.boy_skill_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h',
                                                         self.boy.x - 80, self.boy.y + 30, 297 * 1.9, 168 * 1.9)

class Jump:
    def __init__(self, boy):
        self.boy = boy
        self.jump_speed = 700.0
        self.gravity = -2000.0
        self.horizontal_speed = WALK_SPEED_PPS

    def enter(self, e):
        if self.boy.y <= self.boy.ground_y + 1:
            self.boy.vy = self.jump_speed

        if self.boy.dir > 0:
            self.boy.dir = 1
            self.boy.face_dir = 1
        elif self.boy.dir < 0:
            self.boy.dir = -1
            self.boy.face_dir = -1
        else:
            self.boy.dir = 0
        self.boy.frame = 0

    def exit(self, e):
        self.boy.vy = 0
        self.boy.dir = 0

    def do(self):
        ft = game_framework.frame_time
        self.boy.vy += self.gravity * ft
        self.boy.y += self.boy.vy * ft
        self.boy.x += self.boy.dir * self.horizontal_speed * ft
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 5

        self.boy.x = clamp(50, self.boy.x, 1200 - 50)

        if self.boy.y <= self.boy.ground_y:
            self.boy.y = self.boy.ground_y
            self.boy.vy = 0
            self.boy.dir = 0
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.idle_image.clip_draw(int(self.boy.frame) * 297, 0, 297, 168, self.boy.x + 15, self.boy.y + 10,
                                          297 * 1.6, 168 * 1.6)
        else:
            self.boy.idle_image.clip_composite_draw(int(self.boy.frame) * 297, 0, 297, 168, 0, 'h', self.boy.x - 15,
                                                    self.boy.y + 10, 297 * 1.6, 168 * 1.6)


class Hit:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.frame = 0
        self.boy.hp -= 20
        if self.boy.hp <= 0:
            self.boy.hp = 0
            self.boy.state_machine.handle_state_event(('DIE', 0))

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame += 8 * 1.0 * game_framework.frame_time
        if self.boy.frame >= 4:
            self.boy.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.hit_image.clip_draw(int(self.boy.frame) * 256, 0, 256, 168, self.boy.x, self.boy.y, 256 * 1.8, 168 * 1.5)
        else:
            self.boy.hit_image.clip_composite_draw(int(self.boy.frame) * 256, 0, 256, 168, 0, 'h', self.boy.x,
                                                   self.boy.y, 256 * 1.8, 168 * 1.5)


class Die:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.frame = 0

    def exit(self, e):
        pass

    def do(self):
        if self.boy.frame < 4:
            self.boy.frame += 8 * 1.0 * game_framework.frame_time

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.die_image.clip_draw(int(self.boy.frame) * 256, 0, 256, 168, self.boy.x, self.boy.y, 256 * 1.5, 168 * 1.5)
        else:
            self.boy.die_image.clip_composite_draw(int(self.boy.frame) * 256, 0, 256, 168, 0, 'h', self.boy.x,
                                                   self.boy.y, 256 * 1.5, 168 * 1.5)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 180
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.vy = 0
        self.ground_y = 180

        self.max_hp = 456
        self.hp = 456

        self.image = load_image('boy_walk.png')
        self.idle_image = load_image('boy_idle.png')
        self.boy_attack_image = load_image('boy_attack.png')
        self.boy_skill_image = load_image('boy_skill.png')
        self.boy_hp_image = load_image('hp_sprite.png')

        self.hit_image = load_image('boy_hit.png')
        self.die_image = load_image('boy_die.png')

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.SKILL = Skill(self)
        self.JUMP = Jump(self)
        self.HIT = Hit(self)
        self.DIE = Die(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                            ctrl_down: self.ATTACK, shift_down: self.SKILL, alt_down: self.JUMP,
                            hit_event: self.HIT, die_event: self.DIE},
                self.WALK: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE,
                            ctrl_down: self.ATTACK, ctrl_up: self.ATTACK, alt_down: self.JUMP,
                            hit_event: self.HIT, die_event: self.DIE},
                self.ATTACK: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                              timeout: self.IDLE, hit_event: self.HIT, die_event: self.DIE},
                self.SKILL: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE,
                             timeout: self.IDLE, hit_event: self.HIT, die_event: self.DIE},
                self.JUMP: {timeout: self.IDLE, hit_event: self.HIT, die_event: self.DIE},
                self.HIT: {timeout: self.IDLE, die_event: self.DIE},
                self.DIE: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

        max_sprite_y = 456
        frame_height = 76
        delta = self.max_hp - self.hp
        if delta <= 0:
            frame_index = 0
        else:
            frame_index = math.ceil(delta / frame_height)

        sy = max_sprite_y - frame_index * frame_height
        if sy < 0: sy = 0

        y = max_sprite_y - frame_index * frame_height
        if y < 0: y = 0

        self.boy_hp_image.clip_draw(0, y, 426, 76, self.x, self.y + 110, 426 // 3, 76 // 3)

    def get_bb(self):
        if self.state_machine.cur_state == self.ATTACK:
            if self.face_dir == 1:
                return self.x + 50, self.y - 100, self.x + 130, self.y + 80
            else:
                return self.x - 130, self.y - 100, self.x - 50, self.y + 80
        elif self.state_machine.cur_state == self.SKILL:
            if self.face_dir == 1:
                return self.x - 180, self.y - 100, self.x + 180, self.y + 80
            else:
                return self.x - 180, self.y - 100, self.x + 180, self.y + 80
        else:
            return self.x - 40, self.y - 100, self.x + 40, self.y + 80

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            if self.state_machine.cur_state in [self.ATTACK, self.SKILL]:
                if other.state_machine.cur_state not in [other.DIE, other.HIT]:
                    other.state_machine.handle_state_event(('HIT', 0))
                return

            if self.state_machine.cur_state == self.JUMP:
                return

            if self.state_machine.cur_state in [self.HIT, self.DIE]:
                return

            self.state_machine.handle_state_event(('HIT', 0))

            if self.x < other.x + 40:
                self.x -= 150
            else:
                self.x += 150

            if self.x < 40:
                self.x = 40 + 150

            elif self.x > 1200 - 50:
                self.x = (1200 - 50) - 150

            self.x = clamp(40, self.x, 1200 - 50)