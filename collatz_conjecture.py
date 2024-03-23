from pyglet.window import Window
from pyglet.app import run
from pyglet import clock
from pyglet.graphics import Batch
from pyglet.shapes import Line
import math
import pyglet

def get_hailstone_number(number):
    if(number%2 == 0):
        return number//2
    return ((3*number)+1)/2

def get_series(number):
    while number != 1: # The conjecture ( All positive numbers end up in 4 -> 2 -> 1 )
        number = get_hailstone_number(number)
        yield(number)

class Canvas(Window):
    def __init__(self):
        super().__init__()

        self.width = 1200
        self.height = 800

        self.startx = self.width // 5
        self.starty = self.height // 5
        self.num = 2
        self.number_gen = get_series(self.num)
        self.angle = 0
        self.scale = 20
        self.batch = Batch()
        self.lines = []
        self.counter = 2

        self.rotate_left_angle = 20
        self.rotate_right_angle = 8

        self.progress = 1

    def reset(self):
        self.counter += 1
        self.num = self.counter
        self.number_gen = get_series(self.num)

        self.startx = self.width // 5
        self.starty = self.height // 5

        self.angle = 0
        self.progress = 1

    def calculate_color(self, progress):
        start_color = (255,216,167)
        end_color = (171,84,231)

        # Interpolate between start and end color
        r = start_color[0] + (end_color[0] - start_color[0]) * progress
        g = start_color[1] + (end_color[1] - start_color[1]) * progress
        b = start_color[2] + (end_color[2] - start_color[2]) * progress

        return (int(r), int(g), int(b))
        
    def on_update(self, delta_time):

        if(self.num % 2 == 0):
            self.angle += (self.rotate_left_angle*math.pi)/180
        else:
            self.angle -= (self.rotate_right_angle*math.pi)/180

        endx = self.startx + self.scale * math.cos(self.angle)
        endy = self.starty + self.scale * math.sin(self.angle)

        line_color = self.calculate_color(self.progress/1000)
        new_line = Line(self.startx, self.starty, endx, endy, color=line_color, width=3, batch=self.batch)

        self.lines.append(new_line)
        self.startx = endx
        self.starty = endy

        self.progress += 10

        try:
            self.num = next(self.number_gen)
        except:
            self.reset()
            print(self.counter)
        
    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    canvas = Canvas()
    clock.schedule(canvas.on_update)
    run()
    pyglet.app.exit()
