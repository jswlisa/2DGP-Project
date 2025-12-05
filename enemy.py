from pico2d import *
from state_machine import StateMachine
import math
import random

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import game_framework
import game_world

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


def die(e):
    return e[0] == 'DIE'


class Idle:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.enemy.frame = (self.enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.enemy.is_walking = False
        self.enemy.bt.run()

    def draw(self):
        if self.enemy.is_walking:
            if self.enemy.face_dir == 1:
                self.enemy.walk_image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 145,
                                                self.enemy.x + 80, self.enemy.y - 20, 256 * 1.5, 145 * 1.5)
            else:
                self.enemy.walk_image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h',
                                                          self.enemy.x + 80, self.enemy.y - 20, 256 * 1.5, 145 * 1.5)
        else:
            if self.enemy.face_dir == 1:
                self.enemy.image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 145,
                                           self.enemy.x, self.enemy.y, 256 * 2, 145 * 2)
            else:
                self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h',
                                                     self.enemy.x, self.enemy.y, 256 * 2, 145 * 2)


class Hit:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, e):
        self.enemy.dir = 0
        self.enemy.hp -= 76 / 2
        if self.enemy.hp < 0:
            self.enemy.hp = 0

    def exit(self, e):
        self.enemy.dir = 0

    def do(self):
        self.enemy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.enemy.hp <= 0:
            self.enemy.state_machine.handle_state_event(('DIE', 0))
            return
        if self.enemy.frame >= 5:
            self.enemy.frame = 0
            self.enemy.state_machine.handle_state_event(('TIMEOUT', 0))
            return

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.enmey_hit_image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 145, self.enemy.x + 70,
                                                 self.enemy.y - 40, 256 * 1.7, 145 * 1.7)
        else:
            self.enemy.enmey_hit_image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 145, 0, 'h',
                                                           self.enemy.x + 70, self.enemy.y - 40, 256 * 1.7, 145 * 1.7)


class Die:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, e):
        self.enemy.dir = 0
        self.enemy.frame = 0

    def exit(self, e):
        self.enemy.dir = 0

    def do(self):
        self.enemy.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.enemy.frame >= 4:
            self.enemy.frame = 4

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.enemy_die_image.clip_draw(int(self.enemy.frame) * 256, 0, 256, 144, self.enemy.x + 30,
                                                 self.enemy.y - 20, 256 * 1.4, 144 * 1.4)
        else:
            self.enemy.enemy_die_image.clip_composite_draw(int(self.enemy.frame) * 256, 0, 256, 144, 0, 'h',
                                                           self.enemy.x + 30, self.enemy.y - 20, 256 * 1.4, 144 * 1.4)


class Enemy:
    def __init__(self):
        self.x, self.y = 600, 220
        self.image = load_image('enemy.png')
        self.walk_image = load_image('enemy_walk.png')
        self.enmey_hit_image = load_image('enemy_hit.png')
        self.enemy_hp_image = load_image('hp_sprite.png')
        self.enemy_die_image = load_image('enemy_die.png')

        self.frame = 0
        self.dir = 0
        self.face_dir = -1
        self.hp = 456

        self.speed = RUN_SPEED_PPS
        self.tx, self.ty = 1000, 1000

        self.build_behavior_tree()
        self.is_walking = False

        self.IDLE = Idle(self)
        self.HIT = Hit(self)
        self.DIE = Die(self)

        self.state_machine = StateMachine(
            self.IDLE, {
                self.IDLE: {die: self.DIE, Hit: self.HIT},
                self.HIT: {timeout: self.IDLE, die: self.DIE},
                self.DIE: {die: self.DIE}
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


    def get_nearest_player(self):
        candidates = []
        for layer in game_world.world:
            for obj in layer:
                if type(obj).__name__ in ['Girl', 'Boy']:
                    candidates.append(obj)

        if not candidates:
            return None

        closest_player = min(candidates, key=lambda p: (p.x - self.x) ** 2 + (p.y - self.y) ** 2)

        return closest_player

    def is_player_nearby(self, r):
        player = self.get_nearest_player()

        if player is None:
            return BehaviorTree.FAIL

        distance_sq = (player.x - self.x) ** 2 + (player.y - self.y) ** 2

        if distance_sq < r ** 2:
            self.target_player = player
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self):
        if not hasattr(self, 'target_player') or self.target_player is None:
            return BehaviorTree.FAIL

        target_exists = False
        for layer in game_world.world:
            if self.target_player in layer:
                target_exists = True
                break

        if not target_exists:
            self.target_player = None
            return BehaviorTree.FAIL

        player = self.target_player

        self.dir = math.atan2(player.y - self.y, player.x - self.x)
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.face_dir = 1 if player.x > self.x else -1

        self.is_walking = True

        return BehaviorTree.RUNNING


    def build_behavior_tree(self):
        find_player = Condition("플레이어 발견?", self.is_player_nearby, 500)

        chase_player = Action("플레이어 추적", self.move_to_player)

        chase_sequence = Sequence("추적", find_player, chase_player)

        self.bt = Selector("행동 선택", chase_sequence)