from pico2d import load_image, get_time
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT
from state_machine import StateMachine



def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



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
        self.girl.frame = (self.girl.frame + 1) % 5
        self.girl.x += self.girl.dir * 5

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.image.clip_draw(self.girl.frame * 256, 0, 256, 145, self.girl.x, self.girl.y, 256, 145)
        else:
            self.girl.image.clip_composite_draw(self.girl.frame * 256, 0, 256, 145, 0, 'h', self.girl.x, self.girl.y, 256, 145)



class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self,e):
        self.girl.dir = 0

    def exit(self,e):
        self.girl.dir = 0

    def do(self):
        self.girl.frame = (self.girl.frame + 1) % 5
        self.girl.x += self.girl.dir * 5

    def draw(self):
        if self.girl.face_dir == 1:
            self.girl.image.clip_draw(self.girl.frame * 256, 0, 256, 145, self.girl.x, self.girl.y, 256, 145)
        else:
            self.girl.image.clip_composite_draw(self.girl.frame * 256, 0, 256, 145, 0, 'h', self.girl.x, self.girl.y, 256, 145)



class Girl:
    def __init__(self):
        self.x, self.y = 400, 300  # 시작 위치를 화면 중앙으로 변경
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