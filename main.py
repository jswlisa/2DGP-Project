from pico2d import *

open_canvas()

image = load_image('girl.png')

frame = 0
x = 0
y = 300
direction = 1

while True:
    frame = (frame + 1) % 5
    x += direction * 5

    if x > 800:
        direction = -1
    elif x < 0:
        direction = 1

    clear_canvas()
    image.clip_draw(frame * 256, 0, 256, 145, x, y)
    update_canvas()

    delay(0.05)

close_canvas()