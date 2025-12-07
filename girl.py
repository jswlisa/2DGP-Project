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
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_down(e) or right_up(e):
            self.girl.dir = self.girl.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.girl.x += self.girl.dir * WALK_SPEED_PPS * game_framework.frame_time
        self.girl.x = clamp(50, self.girl.x, 1200 - 50)

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x, self.girl.y, 297 * 1.5,
                                      168 * 1.5)
        else:
            self.girl.image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x,
                                                self.girl.y, 297 * 1.5, 168 * 1.5)


class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.dir = 0

    def exit(self, e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.idle_image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x + 15, self.girl.y + 10,
                                           297 * 1.6, 168 * 1.6)
        else:
            self.girl.idle_image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x - 15,
                                                     self.girl.y + 10, 297 * 1.6, 168 * 1.6)

class Attack:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.frame = 0
        self.girl.dir = 0

    def exit(self, e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.girl.frame >= 5:
            self.girl.frame = 0
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.girl_attack_image.clip_draw(int(self.girl.frame) * 269, 0, 269, 185, self.girl.x, self.girl.y,
                                                  269 * 1.5, 185 * 1.5)
        else:
            self.girl.girl_attack_image.clip_composite_draw(int(self.girl.frame) * 269, 0, 269, 185, 0, 'h',
                                                            self.girl.x, self.girl.y, 269 * 1.5, 185 * 1.5)

        effect_frame = max(0, int(self.girl.frame - 1.5))
        if self.girl.face_dir == 1:
            self.girl.attack_effect_image.clip_draw(effect_frame * 558, 0, 558, 466, self.girl.x + 80, self.girl.y,
                                                    558 // 3, 466 // 3)
        else:
            self.girl.attack_effect_image.clip_composite_draw(effect_frame * 558, 0, 558, 466, 0, 'h', self.girl.x - 80,
                                                              self.girl.y, 558 // 3, 466 // 3)


class Skill:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.frame = 0
        self.girl.dir = 0

    def exit(self, e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.girl.frame >= 5:
            self.girl.frame = 0
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))
            return

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.girl_skill_image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x + 40,
                                                 self.girl.y + 30, 297 * 3, 168 * 3)
        else:
            self.girl.girl_skill_image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h',
                                                           self.girl.x - 40, self.girl.y + 30, 297 * 3, 168 * 3)


class Jump:
    def __init__(self, girl):
        self.girl = girl
        self.jump_speed = 700.0
        self.gravity = -2000.0
        self.horizontal_speed = WALK_SPEED_PPS

    def enter(self, e):
        if self.girl.y <= self.girl.ground_y + 1:
            self.girl.vy = self.jump_speed

        if self.girl.dir > 0:
            self.girl.dir = 1
            self.girl.face_dir = 1
        elif self.girl.dir < 0:
            self.girl.dir = -1
            self.girl.face_dir = -1
        else:
            self.girl.dir = 0
        self.girl.frame = 0

    def exit(self, e):
        self.girl.vy = 0
        self.girl.dir = 0

    def do(self):
        ft = game_framework.frame_time
        self.girl.vy += self.gravity * ft
        self.girl.y += self.girl.vy * ft
        self.girl.x += self.girl.dir * self.horizontal_speed * ft
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 5

        self.girl.x = clamp(50, self.girl.x, 1200 - 50)

        if self.girl.y <= self.girl.ground_y:
            self.girl.y = self.girl.ground_y
            self.girl.vy = 0
            self.girl.dir = 0
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.idle_image.clip_draw(int(self.girl.frame) * 297, 0, 297, 168, self.girl.x + 15, self.girl.y + 10,
                                           297 * 1.6, 168 * 1.6)
        else:
            self.girl.idle_image.clip_composite_draw(int(self.girl.frame) * 297, 0, 297, 168, 0, 'h', self.girl.x - 15,
                                                     self.girl.y + 10, 297 * 1.6, 168 * 1.6)


class Hit:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.frame = 0
        self.girl.hp -= 20
        if self.girl.hp <= 0:
            self.girl.hp = 0
            self.girl.state_machine.handle_state_event(('DIE', 0))

    def exit(self, e):
        pass

    def do(self):
        self.girl.frame += 8 * 1.0 * game_framework.frame_time
        if self.girl.frame >= 4:
            self.girl.state_machine.handle_state_event(('TIMEOUT', 0))

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.hit_image.clip_draw(int(self.girl.frame) * 256, 0, 256, 168, self.girl.x, self.girl.y, 256 * 1.5, 168 * 1.5)
        else:
            self.girl.hit_image.clip_composite_draw(int(self.girl.frame) * 256, 0, 256, 168, 0, 'h', self.girl.x,
                                                    self.girl.y, 256 * 1.5, 168 * 1.5)


class Die:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.frame = 0

    def exit(self, e):
        pass

    def do(self):
        if self.girl.frame < 4:
            self.girl.frame += 8 * 1.0 * game_framework.frame_time

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.die_image.clip_draw(int(self.girl.frame) * 256, 0, 256, 168, self.girl.x, self.girl.y, 256 * 1.5, 168 * 1.5)
        else:
            self.girl.die_image.clip_composite_draw(int(self.girl.frame) * 256, 0, 256, 168, 0, 'h', self.girl.x,
                                                    self.girl.y, 256 * 1.5, 168 * 1.5)


class Girl:
    def __init__(self):
        self.x, self.y = 400, 180
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.vy = 0
        self.ground_y = 180

        self.max_hp = 456
        self.hp = 456

        self.image = load_image('girl.png')
        self.idle_image = load_image('girl_idle.png')
        self.girl_attack_image = load_image('girl_attack.png')
        self.attack_effect_image = load_image('attack_effect.png')
        self.girl_skill_image = load_image('girl_skill.png')
        self.girl_hp_image = load_image('hp_sprite.png')

        self.hit_image = load_image('girl_hit.png')
        self.die_image = load_image('girl_die.png')

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

        self.girl_hp_image.clip_draw(0, y, 426, 76, self.x, self.y + 110, 426 // 3, 76 // 3)

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
        if group == 'girl:enemy':
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

            if self.x < 25:
                self.x = 25 + 150

            elif self.x > 1200 - 50:
                self.x = (1200 - 50) - 150

            self.x = clamp(25, self.x, 1200 - 50)