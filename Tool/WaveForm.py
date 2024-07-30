import turtle
from pylib.debug import *

FORMAT = ['NRZ', 'F0', 'F1', 'RZ', 'RO']
ACTIVE = ['keep', 'F0', 'F1']

def set_header(x_coordinate, y_coordinate, to_angel):
    turtle.penup()
    turtle.goto(x_coordinate, y_coordinate)
    turtle.setheading(to_angel)
    turtle.pendown()

def dotted_line(base_long, rate, length):
    turtle.pensize(1)
    for i in range(length//base_long):
        turtle.pendown()
        turtle.forward(base_long * rate)
        turtle.penup()
        turtle.forward(base_long * (1 - rate))
    turtle.forward(base_long * rate)

class TIMING:
    def __init__(self, format:str, edge_1:float, edge_2:float):
        if format not in FORMAT:
            raise(ValueError(error(f'{format} has not define in FORMAT')))
        if edge_1 > 1 or edge_1 < 0:
            raise(ValueError(error(f'{edge_1} has not in limit')))
        if edge_2 > 1 or edge_2 < 0:
            raise(ValueError(error(f'{edge_2} has not in limit')))
        self._format = format
        self._edge_1 = edge_1
        self._edge_2 = edge_2
    @property
    def format(self):
        return self._format
    @property
    def edge_1(self):
        return self._edge_1
    @property
    def edge_2(self):
        return self._edge_2

class PIN:
    def __init__(self, name:str, timing:TIMING, color='black'):
        if type(timing) != TIMING:
            raise(TypeError(error(f'timing type must TIMING')))
        self._name = name
        self._timing = timing
        self._color = color
        self._dlst = []
    @property
    def name(self):
        return self._name
    @property
    def timing(self):
        return self._timing
    @property
    def color(self):
        return self._color
    @property
    def dlst(self):
        return self._dlst
    def set_color(self, color:str):
        self._color = color
    def __call__(self, data):
        self._dlst.append(int(bool(data)))
    def reset(self):
        self._dlst = []


class PINS:
    width_total = 1000
    width_rate = 0.85
    length_total = 1600
    length_name = 100

    font_type = 'bold'
    font_name = '楷书'

    dot_line_base_long = 10
    dot_line_rate = 0.4
    def __init__(self, plst):
        self._plst = plst
        self._pin_count = len(plst)
        self._cycle_count = 0
        self.pin_reset()
    @property
    def plst(self):
        return self._plst
    @property
    def pin_count(self):
        return self._pin_count
    @property
    def cycle_count(self):
        return self._cycle_count
    def pin_reset(self):
        self._cycle_count = 0
        for pin in self.plst:
            pin.reset()
    def add_pattern(self, others:ACTIVE='keep', **kwargs):
        self._cycle_count += 1
        for pin in self.plst:
            if pin.name not in kwargs:
                if others == 'keep':
                    if len(pin.dlst) == 0:
                        pin(0)
                    else:
                        pin(pin.dlst[-1])
                elif others == 'F0':
                    pin(0)
                elif others == 'F1':
                    pin(1)
                else:
                    raise(ValueError(error(f'{others} is not define value')))
            else:
                pin(int(bool(kwargs[pin.name])))
    def add_patterns(self, cycle:int, others:ACTIVE='keep', **kwargs):
        for i in range(cycle):
            dic = {}
            for key, value in kwargs.items():
                dic[key] = 1 if value & (0b1 << (cycle - i - 1)) else 0
            self.add_pattern(others=others, **dic)
    def draw(self, reference_line_x=False, reference_line_y=False):
        turtle.speed('fastest')
        turtle.delay(0)
        turtle.tracer(100)
        turtle.hideturtle()

        width_per_pin = PINS.width_total / self.pin_count
        amplitudes = width_per_pin * PINS.width_rate / 2
        length_per_cycle = (PINS.length_total - PINS.length_name)/self.cycle_count

        # draw
        for pin_index, pin in enumerate(self._plst):
            y_coordinate = PINS.width_total / 2 - (0.5 + pin_index) * width_per_pin
            # write pin name
            turtle.pencolor(pin.color)
            font_size = int(min(width_per_pin, PINS.length_name / 5, PINS.length_name / len(pin.name)))
            font = (PINS.font_name, font_size, PINS.font_type)
            set_header((PINS.length_name - PINS.length_total)/2, y_coordinate-font_size/2, 0)
            turtle.write(pin.name, align='center', font=font)

            # draw reference line x
            turtle.pencolor('black')
            if reference_line_x:
                set_header(PINS.length_name - PINS.length_total / 2, y_coordinate, 0)
                dotted_line(PINS.dot_line_base_long, PINS.dot_line_rate, PINS.length_total - PINS.length_name)

            # draw signal line
            turtle.pencolor(pin.color)
            turtle.pensize(3)
            set_header(PINS.length_name - PINS.length_total / 2, y_coordinate - amplitudes, 0)
            if pin.timing.format == 'F0':
                sign = -1
                turtle.goto(PINS.length_name - PINS.length_total / 2, y_coordinate + sign * amplitudes)
                for i in range(self.cycle_count):
                    turtle.forward(length_per_cycle)
            elif pin.timing.format == 'F1':
                sign = 1
                turtle.goto(PINS.length_name - PINS.length_total / 2, y_coordinate + sign * amplitudes)
                for i in range(self.cycle_count):
                    turtle.forward(length_per_cycle)
            elif pin.timing.format == 'NRZ':
                for idx, data in enumerate(pin.dlst):
                    sign = 1 if data else -1
                    x_coordinate = PINS.length_name - PINS.length_total / 2 + idx * length_per_cycle
                    # dy = width_per_pin * PINS.width_rate / 2 if data else ( -width_per_pin * PINS.width_rate )
                    turtle.forward(length_per_cycle * pin.timing.edge_1)
                    turtle.goto(x_coordinate + length_per_cycle * pin.timing.edge_1, y_coordinate + sign * amplitudes)
                    turtle.forward(length_per_cycle * (1 - pin.timing.edge_1))
            elif pin.timing.format == 'RO':
                for idx, data in enumerate(pin.dlst):
                    sign = 1 if data else -1
                    x_coordinate = PINS.length_name - PINS.length_total / 2 + idx * length_per_cycle
                    # dy = width_per_pin * PINS.width_rate / 2 if data else ( -width_per_pin * PINS.width_rate / 2 )
                    # turtle.goto(x_coordinate, y_coordinate - dy)
                    turtle.forward(length_per_cycle * pin.timing.edge_1)
                    turtle.goto(x_coordinate + length_per_cycle * pin.timing.edge_1, y_coordinate + sign * amplitudes)
                    turtle.forward(length_per_cycle * (pin.timing.edge_2 - pin.timing.edge_1))
                    turtle.goto(x_coordinate + length_per_cycle * pin.timing.edge_2, y_coordinate + amplitudes)
                    turtle.forward(length_per_cycle * (1 - pin.timing.edge_2))
            elif pin.timing.format == 'RZ':
                for idx, data in enumerate(pin.dlst):
                    sign = 1 if data else -1
                    x_coordinate = PINS.length_name - PINS.length_total / 2 + idx * length_per_cycle
                    # dy = width_per_pin * PINS.width_rate / 2 if data else ( -width_per_pin * PINS.width_rate / 2 )
                    # turtle.goto(x_coordinate, y_coordinate - dy)
                    turtle.forward(length_per_cycle * pin.timing.edge_1)
                    turtle.goto(x_coordinate + length_per_cycle * pin.timing.edge_1, y_coordinate + sign * amplitudes)
                    turtle.forward(length_per_cycle * (pin.timing.edge_2 - pin.timing.edge_1))
                    turtle.goto(x_coordinate + length_per_cycle * pin.timing.edge_2, y_coordinate - amplitudes)
                    turtle.forward(length_per_cycle * (1 - pin.timing.edge_2))
            # # draw reference line x
            # turtle.pencolor('black')
            # if reference_line_x:
            #     set_header(PINS.length_name - PINS.length_total / 2, y_coordinate, 0)
            #     dotted_line(PINS.dot_line_base_long, PINS.dot_line_rate, PINS.length_total - PINS.length_name)

        # draw reference line y
        turtle.pencolor('black')
        if reference_line_y:
            for idx in range(self.cycle_count + 1):
                set_header(PINS.length_name - PINS.length_total / 2 + idx * length_per_cycle, PINS.width_total / 2, -90)
                dotted_line(PINS.dot_line_base_long, PINS.dot_line_rate, PINS.width_total)

        turtle.tracer(1)
        turtle.mainloop()


if __name__ == '__main__':
    t_sck = TIMING('RZ', 0.25, 0.75)
    t_cs = TIMING('NRZ', 0, 1)

    Power = PIN('Power', t_cs, 'red')
    Reset = PIN('Reset', t_cs, 'gray')
    ADDR2 = PIN('ADDR2', t_cs)
    ADDR1 = PIN('ADDR1', t_cs)
    ADDR0 = PIN('ADDR0', t_cs)
    SCD = PIN('SCD', t_cs)
    SCK = PIN('SCK', t_sck, 'green')
    ACT = PIN('ACT', t_cs, 'blue')
    YWE = PIN('YWE', t_cs)
    YS = PIN('YS', t_sck)

    plst = [Power, Reset, ADDR2, ADDR1, ADDR0, SCD, SCK, ACT, YWE, YS]
    pins = PINS(plst)
    pins.add_pattern(Power=0, Reset=0, ADDR2=0, ADDR1=0, ADDR0=0, SCD=0, SCK=0, ACT=0, YWE=0, YS=0)
    pins.add_pattern(Power=1)
    pins.add_pattern(Reset=1)
    pins.add_pattern(Reset=0)
    for addr in range(7):
        addr2 = int(bool(addr & 0b100))
        addr1 = int(bool(addr & 0b10))
        addr0 = int(bool(addr & 0b1))
        for i in [1, 0, 1, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            pins.add_pattern(ADDR2=addr2, ADDR1=addr1, ADDR0=addr0, SCK=1, SCD=i)

    for i in range(3):
        pins.add_pattern(SCK=0)

    for i in range(2):
        pins.add_pattern(ACT=1)
        pins.add_pattern()
        pins.add_pattern()

        pins.add_pattern(YWE=1)
        for j in range(4):
            pins.add_pattern(YS=1)
        pins.add_pattern(YWE=0, YS=0)
        for j in range(4):
            pins.add_pattern(YS=1)
        pins.add_pattern(ACT=0, YS=0)
        pins.add_pattern()
        pins.add_pattern()
    pins.add_pattern()
    pins.add_pattern()
    pins.add_pattern()

    pins.add_pattern(Power=0, Reset=0, ADDR2=0, ADDR1=0, ADDR0=0, SCD=0, SCK=0, ACT=0, YWE=0, YS=0)
    pins.add_pattern(ACT=1)
    pins.add_pattern(YWE=1)
    pins.add_pattern(YS=1)
    pins.add_pattern(YWE=0, YS=0, ACT=0)
    # pins.add_pattern(ACT=0)

    # pins.add_pattern(ACT=1)
    pins.add_pattern(ACT=1, YS=1)
    pins.add_pattern(ACT=0, YS=0)

    pins.draw(True)