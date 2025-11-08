from pico2d import *

class WaterFront:
    def __init__(self):
        self.image = load_image('waterfront(1).png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        # draw_rectangle(*self.get_bb())

    # def get_bb(self):
    #     return 0, 0, 1600-1, 50
    #
    # def handle_collision(self, group, other):
    #     pass