from pico2d import load_image, get_time
from state_machine import StateMachine



class Girl:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if(right_down(e) or left_up(e)):
            self.girl.dir = self.girl.face_dir = 1
        elif(left_down(e) or right_up(e)):
            self.girl.dir = self.girl.face_dir = -1


    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('girl.png')

        self.state_machine  = StateMachine(
            self.draw(),
            {
                self.WALK: {right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK},

            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #들어온 외부 키 입력 등을 상태 머신에 전달하기 위해서
        #튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()