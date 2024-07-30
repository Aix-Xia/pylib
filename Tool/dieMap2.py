"""
作者：夏季
日期：2023-05-16
功能：画DIE map， 计算DIE count
单位：um
"""
# from package.debug import *
import turtle

def set_header(x, y, to_angle):
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(to_angle)
    turtle.pendown()
# def rectangle(size_x, size_y, pencolor='black', fillcolor='white'):
#     set_header(turtle.xcor()-size_x/2, turtle.ycor()-size_y/2, 0)
#     turtle.pencolor(pencolor)
#     turtle.fillcolor(fillcolor)
#     turtle.begin_fill()
#     for i in range(2):
#         turtle.forward(size_x)
#         turtle.left(90)
#         turtle.forward(size_y)
#         turtle.left(90)
#     turtle.end_fill()
def rectangle(size_x, size_y, pencolor='black', fillcolor=None, pensize=None):
    set_header(turtle.xcor()-size_x/2, turtle.ycor()-size_y/2, 0)
    turtle.pencolor(pencolor)
    turtle.pensize(pensize)
    try:
        turtle.fillcolor(fillcolor)
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(size_x)
            turtle.left(90)
            turtle.forward(size_y)
            turtle.left(90)
        turtle.end_fill()
    except Exception:
        for i in range(2):
            turtle.forward(size_x)
            turtle.left(90)
            turtle.forward(size_y)
            turtle.left(90)
def circle(radius, pencolor='black', fillcolor=None, pensize=None):
    set_header(turtle.xcor()+radius, turtle.ycor(), 90)
    turtle.pencolor(pencolor)
    if pensize == None:
        turtle.pensize()
    else:
        turtle.pensize(pensize)
    try:
        turtle.fillcolor(fillcolor)
        turtle.begin_fill()
        turtle.circle(radius)
        turtle.end_fill()
    except Exception:
        turtle.circle(radius)

class DIE_MAP:
    Multiply = 3 * 10 ** (-3)
    def __init__(self):
        # die size
        self.die_size_x = 8145
        self.die_size_y = 4308
        # scrabe lane size
        self.SCL_size = 60
        # die count in shot
        self.die_count_in_shot_x = 3
        self.die_count_in_shot_y = 7
        # shot grid shift size
        self.grid_shift_x = 8200
        self.grid_shift_y = 15300
        # wafer information
        self.wafer_radius = 150000
        self.trim_size = 3000
        self.active_radius = self.wafer_radius - self.trim_size
        # pointer
            # bottom/left die(in shot) index is (0, 0)
        self.current_die_index_x = 0
        self.current_die_index_y = 0
            # center shot index is (0, 0)
        self.current_shot_index_x = 0
        self.current_shot_index_y = 0
    def set_die_size(self, x, y):
        self.die_size_x = x
        self.die_size_y = y
    def set_SCL_size(self, size):
        self.SCL_size = size
    def set_die_count_in_shot(self, x, y):
        self.die_count_in_shot_x = x
        self.die_count_in_shot_y = y
    def set_grid_shift(self, x, y):
        self.grid_shift_x = x
        self.grid_shift_y = y
    def set_wafer_radius_size(self, radius):
        self.wafer_radius = radius
        self.active_radius = self.wafer_radius - self.trim_size
    def set_trim_size(self, size):
        self.trim_size = size
        self.active_radius = self.wafer_radius - self.trim_size
    def set_pointer(self, die_index_x:int, die_index_y:int, shot_index_x:int, shot_index_y:int):
        self.current_die_index_x = die_index_x
        self.current_die_index_y = die_index_y
        self.current_shot_index_x = shot_index_x
        self.current_shot_index_y = shot_index_y
    @classmethod
    def set_multiply(cls, multiply):
        cls.Multiply = multiply
    def get_shot_count_limit(self):
        shot_count_max_x = int(self.wafer_radius / ((self.die_size_x + self.SCL_size) * self.die_count_in_shot_x)) + 3
        shot_count_max_y = int(self.wafer_radius / ((self.die_size_y + self.SCL_size) * self.die_count_in_shot_y)) + 3
        return shot_count_max_x, shot_count_max_y
    def get_current_shot_coordinate(self):
        shot_coordinate_x = self.current_shot_index_x * (self.die_size_x + self.SCL_size) * self.die_count_in_shot_x + self.grid_shift_x
        shot_coordinate_y = self.current_shot_index_y * (self.die_size_y + self.SCL_size) * self.die_count_in_shot_y + self.grid_shift_y
        return shot_coordinate_x, shot_coordinate_y
    def get_current_die_coordinate(self):
        shot_coordinate_x, shot_coordinate_y = self.get_current_shot_coordinate()
        die_coordinate_x = shot_coordinate_x + (self.current_die_index_x + 0.5 - self.die_count_in_shot_x / 2) * (self.die_size_x + self.SCL_size)
        die_coordinate_y = shot_coordinate_y + (self.current_die_index_y + 0.5 - self.die_count_in_shot_y / 2) * (self.die_size_y + self.SCL_size)
        return die_coordinate_x, die_coordinate_y
    def if_shot_max_in_wafer(self, active_area=True):
        radius = self.active_radius if active_area else self.wafer_radius
        coordinate_x, coordinate_y = self.get_current_shot_coordinate()
        shot_size_x = (self.die_size_x + self.SCL_size) * self.die_count_in_shot_x - self.SCL_size
        shot_size_y = (self.die_size_y + self.SCL_size) * self.die_count_in_shot_y - self.SCL_size
        size_x = max(abs(coordinate_x + shot_size_x / 2), abs(coordinate_x - shot_size_x / 2))
        size_y = max(abs(coordinate_y + shot_size_y / 2), abs(coordinate_y - shot_size_y / 2))
        if size_x ** 2 + size_y ** 2 < radius ** 2:
            return True
        else:
            return False
    def if_shot_min_in_wafer(self, active_area=True):
        radius = self.active_radius if active_area else self.wafer_radius
        coordinate_x, coordinate_y = self.get_current_shot_coordinate()
        shot_size_x = (self.die_size_x + self.SCL_size) * self.die_count_in_shot_x - self.SCL_size
        shot_size_y = (self.die_size_y + self.SCL_size) * self.die_count_in_shot_y - self.SCL_size
        if (coordinate_x + shot_size_x / 2) * (coordinate_x - shot_size_y / 2) > 0:
            size_x = min(abs(coordinate_x + shot_size_x / 2), abs(coordinate_x - shot_size_x / 2))
        else:
            size_x = 0
        if (coordinate_y + shot_size_y / 2) * (coordinate_y - shot_size_y / 2) > 0:
            size_y = min(abs(coordinate_y + shot_size_y / 2), abs(coordinate_y - shot_size_y / 2))
        else:
            size_y = 0
        if size_x ** 2 + size_y ** 2 < radius ** 2:
            return True
        else:
            return False
    def if_die_max_in_wafer(self, active_area=True):
        radius = self.active_radius if active_area else self.wafer_radius
        coordinate_x, coordinate_y = self.get_current_die_coordinate()
        size_x = max(abs(coordinate_x + self.die_size_x / 2), abs(coordinate_x - self.die_size_x / 2))
        size_y = max(abs(coordinate_y + self.die_size_y / 2), abs(coordinate_y - self.die_size_y / 2))
        if size_x ** 2 + size_y ** 2 < radius ** 2:
            return True
        else:
            return False
    def if_die_min_in_wafer(self, active_area=True):
        radius = self.active_radius if active_area else self.wafer_radius
        coordinate_x, coordinate_y = self.get_current_die_coordinate()
        if (coordinate_x + self.die_size_x / 2) * (coordinate_x - self.die_size_x / 2) > 0:
            size_x = min(abs(coordinate_x + self.die_size_x / 2), abs(coordinate_x - self.die_size_x / 2))
        else:
            size_x = 0
        if (coordinate_y + self.die_size_y / 2) * (coordinate_y - self.die_size_y / 2) > 0:
            size_y = min(abs(coordinate_y + self.die_size_y / 2), abs(coordinate_y - self.die_size_y / 2))
        else:
            size_y = 0
        if size_x ** 2 + size_y ** 2 < radius ** 2:
            return True
        else:
            return False
    def get_full_die_count(self, active_area=True):
        shot_count_max_x, shot_count_max_y = self.get_shot_count_limit()
        full_die_count = 0
        for sx in range(-shot_count_max_x, shot_count_max_x+1, 1):
            for sy in range(-shot_count_max_y, shot_count_max_y+1, 1):
                for dx in range(self.die_count_in_shot_x):
                    for dy in range(self.die_count_in_shot_y):
                        self.set_pointer(dx, dy, sx, sy)
                        if self.if_die_max_in_wafer(active_area):
                            full_die_count += 1
        return full_die_count
    def get_partial_die_count(self, active_area=True):
        shot_count_max_x, shot_count_max_y = self.get_shot_count_limit()
        partial_die_count = 0
        for sx in range(-shot_count_max_x, shot_count_max_x+1, 1):
            for sy in range(-shot_count_max_y, shot_count_max_y+1, 1):
                for dx in range(self.die_count_in_shot_x):
                    for dy in range(self.die_count_in_shot_y):
                        self.set_pointer(dx, dy, sx, sy)
                        if not self.if_die_max_in_wafer(active_area) and self.if_die_min_in_wafer(active_area):
                            partial_die_count += 1
        return partial_die_count
    def draw_die_map(self, multiply=None, die_size_wi_scl=True):
        if multiply == None:
            multiply = DIE_MAP.Multiply
        if die_size_wi_scl:
            scl = self.SCL_size
        else:
            scl = 0
        turtle.hideturtle()
        turtle.speed('fastest')
        shot_count_max_x, shot_count_max_y = self.get_shot_count_limit()
        for sx in range(-shot_count_max_x, shot_count_max_x+1, 1):
            for sy in range(-shot_count_max_y, shot_count_max_y+1, 1):
                for dx in range(self.die_count_in_shot_x):
                    for dy in range(self.die_count_in_shot_y):
                        self.set_pointer(dx, dy, sx, sy)
                        pencolor = 'black'
                        pensize = 1
                        if self.if_die_max_in_wafer():
                            fillcolor = 'green'
                        elif not self.if_die_max_in_wafer() and self.if_die_min_in_wafer():
                            fillcolor = 'yellow'
                        elif not self.if_die_max_in_wafer(False) and self.if_die_min_in_wafer(False):
                            fillcolor = 'red'
                        else:
                            continue
                        coordinate_x, coordinate_y = self.get_current_die_coordinate()
                        set_header(multiply*coordinate_x, multiply*coordinate_y, 0)
                        rectangle(multiply*(self.die_size_x + scl), multiply*(self.die_size_y + scl), pencolor, fillcolor, pensize)
        set_header(0, 0, 0)
        circle(multiply * self.wafer_radius, pencolor='black', fillcolor=None, pensize=1)
        set_header(0, 0, 0)
        circle(multiply * self.active_radius, pencolor='gray', fillcolor=None, pensize=1)
        turtle.mainloop()
    def draw_shot_map(self, multiply=None, die_size_wi_scl=True):
        if die_size_wi_scl:
            scl = self.SCL_size
        else:
            scl = 0
        if multiply == None:
            multiply = DIE_MAP.Multiply
        shot_size_x = (self.die_size_x + self.SCL_size) * self.die_count_in_shot_x
        shot_size_y = (self.die_size_y + self.SCL_size) * self.die_count_in_shot_y
        turtle.hideturtle()
        turtle.speed('fastest')
        turtle.delay(0)
        turtle.tracer(False)
        shot_count_max_x, shot_count_max_y = self.get_shot_count_limit()
        for sx in range(-shot_count_max_x, shot_count_max_x + 1, 1):
            for sy in range(-shot_count_max_y, shot_count_max_y + 1, 1):
                self.set_pointer(0, 0, sx, sy)
                if not self.if_shot_min_in_wafer(False):
                    continue
                for dx in range(self.die_count_in_shot_x):
                    for dy in range(self.die_count_in_shot_y):
                        self.set_pointer(dx, dy, sx, sy)
                        pencolor = 'gray'
                        pensize = 1
                        if self.if_die_max_in_wafer(True):
                            fillcolor = 'green'
                        elif not self.if_die_max_in_wafer(True) and self.if_die_min_in_wafer(False):
                            fillcolor = 'yellow'
                        else:
                            fillcolor = 'lightgray'
                        die_coordinate_x, die_coordinate_y = self.get_current_die_coordinate()
                        set_header(multiply*die_coordinate_x, multiply*die_coordinate_y, 0)
                        rectangle(multiply*(self.die_size_x + scl), multiply*(self.die_size_y + scl), pencolor, fillcolor, pensize)
                pencolor = 'black'
                fillcolor = None
                pensize = 2
                shot_coordinate_x, shot_coordinate_y = self.get_current_shot_coordinate()
                set_header(multiply*shot_coordinate_x, multiply*shot_coordinate_y, 0)
                rectangle(multiply*(shot_size_x + scl), multiply*(shot_size_y + scl), pencolor, fillcolor, pensize)
        set_header(0, 0, 0)
        circle(multiply * self.wafer_radius, pencolor='black', fillcolor=None, pensize=1)
        set_header(0, 0, 0)
        circle(multiply * self.active_radius, pencolor='gray', fillcolor=None, pensize=1)
        turtle.tracer(1)
        turtle.mainloop()

def setup_die_map(field_step_size_x,
                   field_step_size_y,
                   field_shot_size_x,
                   field_shot_size_y,
                   grid_shift_x,
                   grid_shift_y,
                   die_count_in_shot_x,
                   die_count_in_shot_y,
                   wafer_radius=150000,
                   trim_size=3000):
    # calculating parameter
    if field_shot_size_x - field_step_size_x == field_shot_size_y - field_step_size_y:
        SCL_size = field_shot_size_x - field_step_size_x
    else:
        raise (ValueError('Data Error, pls check'))
    die_size_x = field_step_size_x / die_count_in_shot_x - SCL_size
    die_size_y = field_step_size_y / die_count_in_shot_y - SCL_size
    # setup die map and scramble
    die_map = DIE_MAP()
    die_map.set_die_size(x=die_size_x, y=die_size_y)
    die_map.set_SCL_size(size=SCL_size)
    die_map.set_grid_shift(x=grid_shift_x, y=grid_shift_y)
    die_map.set_trim_size(size=trim_size)
    die_map.set_die_count_in_shot(x=die_count_in_shot_x, y=die_count_in_shot_y)
    die_map.set_wafer_radius_size(wafer_radius)
    return die_map

if __name__ == '__main__':
    SWAK = setup_die_map(field_step_size_x=25915,
                     field_step_size_y=26868,
                     field_shot_size_x=25990,
                     field_shot_size_y=26943,
                     grid_shift_x=7683,
                     grid_shift_y=8956,
                     die_count_in_shot_x=5,
                     die_count_in_shot_y=3,
                     wafer_radius=150000,
                     trim_size=3000)
    KRNS = setup_die_map(field_step_size_x=24615,
                         field_step_size_y=30576,
                         field_shot_size_x=24675,
                         field_shot_size_y=30636,
                         grid_shift_x=8200,
                         grid_shift_y=15300,
                         die_count_in_shot_x=3,
                         die_count_in_shot_y=7,
                         wafer_radius=150000,
                         trim_size=3000)
    ATNA = setup_die_map(field_step_size_x=21438,
                         field_step_size_y=23998.68,
                         field_shot_size_x=21438,
                         field_shot_size_y=23998.68,
                         grid_shift_x=0,
                         grid_shift_y=0,
                         die_count_in_shot_x=1,
                         die_count_in_shot_y=1,
                         wafer_radius=150000,
                         trim_size=(150-143.5) * 1000)

    map = ATNA

    for trim_size in range(5100, 6100, 10):
        map.set_trim_size(trim_size)
        print(f'TrimSize:{trim_size/1000:.2f}mm;  FullDieCnt:{map.get_full_die_count():-3d}')