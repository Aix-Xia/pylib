import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import random

def dmin(lst, base=None):
    """get min data in lst"""
    for d in lst:
        if type(d) == list:
            base = dmin(d, base)
        elif type(d) == int or type(d) == float:
            if base == None or d < base:
                base = d
    return base
def dmax(lst, base=None):
    """get max data in lst"""
    for d in lst:
        if type(d) == list:
            base = dmax(d, base)
        elif type(d) == int or type(d) == float:
            if base == None or d > base:
                base = d
    return base
c_list = [(128 / 255, 128 / 255, 128 / 255),
          (128 / 255, 128 / 255, 128 / 255),
          (128 / 255, 128 / 255, 128 / 255),
          (128 / 255, 128 / 255, 128 / 255),
          (144 / 255, 238 / 255, 144 / 255),
          (255 / 255, 165 / 255,   0 / 255),
          (128 / 255, 128 / 255, 128 / 255),
          (238 / 255, 130 / 255, 238 / 255),
          (  0 / 255, 255 / 255, 255 / 255)]

CMD_list = ['PRE', 'ACT', 'WR', 'RD', 'REF']
class PATTERN:
    def __init__(self, RA_Bit_count, CA_Bit_count, defect=None):
        self.wl_count = 2 ** RA_Bit_count
        self.bl_count = 8 * (2 ** CA_Bit_count)
        self.ca = None
        self.ra = None
        self.array = ARRAY(self.wl_count, self.bl_count, defect)
        self.write_map = [[-1 for i in range(self.bl_count)] for j in range(self.wl_count)]
        self.read_map = [[-1 for i in range(self.bl_count)] for j in range(self.wl_count)]
        self.ecr_map = [[-1 for i in range(self.bl_count)] for j in range(self.wl_count)]
        self.ecr_accum = False

    def __write_map(self, lst, data):
        for i in range(8):
            lst[self.ra][8*self.ca+i] = (data>>(7-i))&1
    def __write_ecr(self, data):
        for i in range(8):
            if self.write_map[self.ra][8*self.ca+i] != -1:
                if self.write_map[self.ra][8*self.ca+i] != (data>>(7-i))&1:
                    self.ecr_map[self.ra][8*self.ca+i] = 1
                elif self.ecr_map[self.ra][8*self.ca+i] == -1:
                    self.ecr_map[self.ra][8 * self.ca + i] = 0

    def PRE(self):
        self.array.PRECHARGE()
    def ACT(self, ra):
        self.ra = ra % self.array.WL_count
        self.array.ACTIVE(self.ra)
    def WR(self, ca, data):
        self.ca = ca % (self.bl_count // 8)
        data = data & 0xff
        self.array.WRITE(self.ca, data)
        self.__write_map(self.write_map, data)
    def RD(self, ca):
        self.ca = ca % (self.bl_count // 8)
        data = self.array.READ(self.ca)
        self.__write_map(self.read_map, data)
        self.__write_ecr(data)
        return data
    def REF(self):
        for ra in range(self.wl_count):
            self.ra = ra
            self.array.ACTIVE(self.ra)
            self.array.SENSE()
            self.array.AMPLIFY()
            self.array.WRITEBACK()
    def DELAY(self, time):
        self.array.DELAY(time)

    def __write_1bit(self, wl_index:int, bl_index:int, write_data:{0, 1}):
        ra = wl_index
        ca = bl_index // 8
        bit_index = bl_index % 8
        data = 0
        for i in range(8):
            data <<= 1
            if bit_index == i:
                bit_data = write_data
            else:
                bit_data = self.write_map[ra][ca*8+i]
            data += bit_data

        self.ACT(ra)
        self.WR(ca, data)
        self.PRE()
    def __read_1bit(self, wl_index:int, bl_index:int):
        ra = wl_index
        ca = bl_index // 8
        bit_index = bl_index % 8
        self.ACT(ra)
        data = self.RD(ca)
        self.PRE()
        data = (data>>(7-bit_index))&1
        return data
    def __write_1byte(self, ra:int, ca:int, write_data:int):
        data = write_data % 256
        self.ACT(ra)
        self.WR(ca, data)
        self.PRE()
    def __read_1byte(self, ra:int, ca:int):
        self.ACT(ra)
        data = self.RD(ca)
        self.PRE()
        return data

    # Class 1: Electrical Tests (11).
    """
    The class of electrical base tests consists of checks for contact (1), DC parameters (7), and AC parameters (3).
        1. Contact verifies the connection between the device under test (DUT) and the memory tester.
        2. InpLkH, input leakage-current high, verifies II(L)−max.
        3. InpLkL, input leakage-current low, verifies II(L)−min.
        4. OutpLkH, output leakage-current high, verifies IO(L)−max.
        5. OutpLkL, output leakage-current low, verifies IO(L)−min.
        6. ICC1, operating current, verifies ICC1.
        7. ICC2, standby current, verifies ICC2.
        8. ICC3, refresh current, verifies ICC3.
        9. DataRet, data retention (4n + 6ts): {⇑(wDh); Vcc ← Vcc-min; Del; Vcc ← Vcc-typ; ⇑(rDh)}. 
            In the preceding test description, Del = 1.2tREF, where tREF is the refresh time. Repeat this test for  Dh; 
            Dh is the checkerboard data background, as discussed in a following section about the stresses.
        10.Volatility (6n + 6ts): {⇑(wDh); Vcc ← Vcc-min; ⇑(rDh); Vcc ← Vcc-typ; ⇑(rDh)}. Repeat this test for  Dh.
        11.VccRW (8n + 6ts): {Vcc ← Vcc-max; ⇑(wd); Vcc ← Vcc-min; ⇑(rd); ⇑(wd); Vcc ← Vcc-max; ⇑(rd)}. 
            Repeat this test for d, which is some data background.
    """
    # Class 2: March Tests (18).
    """
    March tests are very popular tests for detecting functional faults such as address decoder and coupling faults. 
    We performed some tests twice; the second time included an extra read operation added to each march element of that test.
    This applies to
        1. MarchC-Rb, where suffix Rb denotes the extra read operation at the beginning of each march element of MarchC-; 
        2. PMOVI-Re, where suffix Re denotes an extra read at the end of each march element of PMOVI; and
        3. MarchU-Rm, with an extra read in the middle of each march element of MarchU.
    D denotes the delay time for data retention faults.4 Given these descriptions, the tests in this class are as follows:
    """
    def Scan(self):
        """
        12 (4n)
            (w0)
            (r0)
            (w1)
            (r1)
        """
        pass
    def MATS_P(self):
        """
        13 (5n)
            (w0)
            ⇑(r0, w1)
            ⇓(r1, w0)
        """
        pass
    def MATS_PP(self):
        """
        14 (6n)
            (w0)
            ⇑(r0, w1)
            ⇓(r1, w0, r0)
        """
        pass
    def MarchA(self):
        """
        15 (15n)
            (w0)
            ⇑(r0, w1, w0, w1)
            ⇑(r1, w0, w1)
            ⇓(r1, w0, w1, w0)
            ⇓(r0, w1, w0)
        """
        pass
    def MarchB(self):
        """
        16 (17n)
            (w0)
            ⇑(r0, w1, r1, w0, r0, w1)
            ⇑(r1, w0, w1)
            ⇓(r1, w0, w1, w0)
            ⇓(r0, w1, w0)
        """
        pass
    def MarchC(self):
        """
        17 (10n)
             (w0)
             ⇑(r0, w1)
             ⇑(r1, w0)
             ⇓(r0, w1)
             ⇓ (r1, w0)
             (r0)
        """
        pass
    def MarchC_Rb(self):
        """
        18 (15n)
            (w0)
            ⇑(r0, r0, w1)
            ⇑(r1, r1, w0)
            ⇓(r0, r0, w1)
            ⇓ (r1, r1, w0)
            (r0, r0)
        """
        pass
    def PMOVI(self):
        """
        19 (13n)
            ⇓(w0)
            ⇑(r0, w1, r1)
            ⇑(r1, w0, r0)
            ⇓(r0, w1, r1)
            ⇓(r1, w0, r0)
        """
        pass
    def PMOVI_Re(self):
        """
        20 (17n)
            ⇓(w0)
            ⇑(r0, w1, r1, r1)
            ⇑(r1, w0, r0, r0)
            ⇓(r0, w1, r1, r1)
            ⇓(r1, w0, r0, r0)
        """
        pass
    def MarchG(self):
        """
        21 (23n + 2D)
            (w0)
            ⇑(r0, w1, r1, w0, r0, w1)
            ⇑(r1, w0, w1)
            ⇓(r1, w0, w1, w0)
            ⇓(r0, w1, w0)
            D
            (r0, w1, r1)
            D
            (r1, w0, r0)
        """
        pass
    def MarchU(self):
        """
        22 (13n)
            (w0)
            ⇑(r0, w1, r1, w0)
            ⇑(r0, w1)
            ⇓(r1, w0, r0, w1)
            ⇓(r1, w0)}
        """
        pass
    def MarchUD(self):
        """
        23 (13n + 2D)
            (w0)
            ⇑(r0, w1, r1, w0)
            D
            ⇑(r0, w1)
            D
            ⇓(r1, w0, r0, w1)
            ⇓(r1, w0)}
        """
        pass
    def MarchU_Rm(self):
        """
        24 (15n)
            (w0)
            ⇑(r0, w1, r1, r1, w0)
            ⇑(r0, w1)
            ⇓(r1, w0, r0, r0, w1)
            ⇓(r1, w0)
        """
        pass
    def MarchLR(self):
        """
        25 (14n)
            (w0)
            ⇓(r0, w1)
            ⇑(r1, w0, r0, w1)
            ⇑(r1, w0)
            ⇑(r0, w1, r1, w0)
            ⇓(r0)
        """
        pass
    def MarchLA(self):
        """
        26 (22n)
            (w0)
            ⇑(r0, w1, w0, w1, r1)
            ⇑(r1, w0, w1, w0, r0)
            ⇓(r0, w1, w0, w1, r1)
            ⇓(r1, w0, w1, w0, r0)
            ⇓(r0)
        """
        pass
    def MarchY(self):
        """
        27 (8n)
            {(w0)
            ⇑(r0, w1, r1)
            ⇓(r1, w0, r0)
            (r0)
        """
        pass
    def XMOVI(self):
        """
        28 (17n × log2n)
            Repeat PMOVI for X-address：
            increment = 2ei(0 ≤ i ≤ 9)
        """
        pass
    def YMOVI(self):
        """
        29 (17n × log2n)
            Repeat PMOVI for Y-address
            increment = 2ei(0 ≤ i ≤ 9).
        """
        pass
    # Class 3: Base-cell tests (6).
    """
    We designed this class of tests to detect the influence of a disturbance of the base cell on other cells, 
    or vice versa. They use the following notation:
        1. The term row denotes the address incrementing along a row of the base cell, skipping the base cell.
        2. The term col denotes the address incrementing along a column of the base cell, skipping the base cell.
        3. The symbol  indicates addressing of the north (N), east (E), south (S), or west (W) neighbors of the base cell.
        4. The notation w1b indicates a w1 in the base cell.
        5. The notation r0b indicates an r0 from the base cell.
    """
    def Butterfly(self):
        """
        30 (14n)
            ⇑(w0)
            ⇑(w1b, (r0), w0b)
            ⇑(w1)
            ⇑(w0b, (r1), w1b)
        """
        pass
    def GalCol(self):
        """
        31 (2n + 4n√n)
            ⇑(w0)
            ⇑(w1b, col(r0, r1b), w0b)
            ⇑(w1)
            ⇑(w0b, col(r1, r0b), w1b)
        """
        pass
    def GalRow(self):
        """
        32 (2n + 4n√n)
            ⇑(w0)
            ⇑(w1b, row(r0, r1b), w0b)
            ⇑(w1)
            ⇑(w0b, row(r1, r0b), w1b)
        """
        pass
    def WalkCol(self):
        """
        33 (6n + 2n√n)
            ⇑(w0)
            ⇑(w1b, col(r0), r1b, w0b)
            ⇑(w1)
            ⇑(w0b, col(r1), r0b, w1b)
        """
        pass
    def WalkRow(self):
        """
        34 (6n + 2n√n)
            ⇑(w0)
            ⇑(w1b, row(r0), r1b, w0b)
            ⇑(w1)
            ⇑(w0b, row(r1), r0b, w1b)
        """
        pass
    def SlidDiag(self):
        """
        35 (4n√n)
            For each diagonal element, denoted by d,
            perform the test for each diagonal,
            denoted by ⇑d:
                ⇑(w0)
                ⇑d(w1d, r, w0d)
                ⇑(w1)
                ⇑d(w0d, r, w1d)
        """
        pass
    # Class 4: Repetitive test (3).
    """
    Repetitive tests perform multiple read or write operations to a single cell; 
    denoted by rxy or rwy, these tests repeat the rx or wx operation y times. 
    Repeating the tests makes partial fault effects become full fault effects. 
    The  denotes an address increment along the main diagonal.
    """
    def HammerR(self):
        """
        36 (40n):
            ⇑(w0)
            ⇑(r0, w1, r116, w0)
            ⇑(w1)
            ⇑(r1, w0, r016, w1)
        """
        pass
    def Hammer(self):
        """
        37 (4n + 2002√n):
            ⇑(w0)
            (w1b1000, row(r0), r1b, col(r0), r1b, w0b)
            ⇑(w1)
            (w0b1000, row(r1), r0b, col(r1), r0b, w1b)
        """
        pass
    def HammerW(self):
        """
        38 (4n + 2√n):
            ⇑(w0)
            (w1b16, col(r0), w0b)
            ⇑(w1)
            (w0b16, col(r1), w1b)
        """
        pass

    def DONE(self, save_map=False, path='./', file_name='0.png'):
        if self.ecr_accum:
            ecr_switch = {-1:0, 0:4, 1:7}
            for r in range(self.wl_count):
                for c in range(self.bl_count):
                    self.ecr_map[r][c] = ecr_switch[self.ecr_map[r][c]]
        else:
            for r in range(self.wl_count):
                for c in range(self.bl_count):
                    if self.write_map[r][c] == -1 and self.read_map[r][c] == -1:
                        self.ecr_map[r][c] = 0
                    elif self.write_map[r][c] == -1 and self.read_map[r][c] == 0:
                        self.ecr_map[r][c] = 1
                    elif self.write_map[r][c] == -1 and self.read_map[r][c] == 1:
                        self.ecr_map[r][c] = 2
                    elif self.write_map[r][c] == 0 and self.read_map[r][c] == -1:
                        self.ecr_map[r][c] = 3
                    elif self.write_map[r][c] == 0 and self.read_map[r][c] == 0:
                        self.ecr_map[r][c] = 4
                    elif self.write_map[r][c] == 0 and self.read_map[r][c] == 1:
                        self.ecr_map[r][c] = 5
                    elif self.write_map[r][c] == 1 and self.read_map[r][c] == -1:
                        self.ecr_map[r][c] = 6
                    elif self.write_map[r][c] == 1 and self.read_map[r][c] == 0:
                        self.ecr_map[r][c] = 7
                    elif self.write_map[r][c] == 1 and self.read_map[r][c] == 1:
                        self.ecr_map[r][c] = 8

        dmi = dmin(self.ecr_map)
        dma = dmax(self.ecr_map)
        cmap = LinearSegmentedColormap.from_list('define', c_list[dmi: dma + 1])
        if dmi == dma:
            cmap = LinearSegmentedColormap.from_list('define', [c_list[dmi], c_list[dma]])

        rate = min(16/self.array.BL_count, 8/self.array.WL_count)
        fig = plt.figure(figsize=(rate * self.array.BL_count, rate * self.array.WL_count))
        ax = fig.add_subplot(111)

        ax.imshow(self.ecr_map, cmap=cmap)
        ax.set_yticks(list(range(self.array.WL_count)))
        ax.set_xticks(list(range(self.array.BL_count)))
        ax.set_xlabel('BL')
        ax.set_ylabel('WL')

        linewidth = 10 * rate
        for i in range(self.array.WL_count + 1):
            ax.plot((-0.5, self.array.BL_count - 0.5), (i - 0.5, i - 0.5), color='white', linewidth=linewidth)
        for i in range(self.array.BL_count + 1):
            ax.plot((i - 0.5, i - 0.5), (-0.5, self.array.WL_count - 0.5), color='white', linewidth=linewidth)
        ax.set_axis_off()

        if save_map:
            plt.savefig(path + file_name)
        else:
            plt.show()

        self.array.inital()


STATUS = ('FORCE', 'SENSE')
UNIT = {'voltage' : 'V',
        'capacitance' : 'fF',
        'resistance' : 'KΩ'}
CMD = ('ACT', 'WR', 'RD', 'PRE')
DEFECT_TYPE = ('OPEN', 'SHORT')
ITEM_list = ['WL', 'BL', 'TISO', 'SN', 'SNC']

class ITEM:
    def __init__(self, name:ITEM_list, x:int, y:int):
        name = name.upper()
        if name not in ITEM_list:
            raise('****** Item Error : %s is not define Item ******'%name)
        self.name = name
        self.x = x
        self.y = y
        self.order = ITEM_list.index(self.name)

class DEFECT:
    def __init__(self, defect_type:DEFECT_TYPE, defect_item0:ITEM, defect_item1=None, resistance_short=0):
        defect_type = defect_type.upper()
        if defect_type not in DEFECT_TYPE:
            raise('****** Defect Type Error : %s is not define defect_type ******'%defect_type)
        self.defect_type = defect_type
        if self.defect_type == 'OPEN':
            self.defect_item0 = defect_item0
            self.defect_item1 = defect_item1
        elif self.defect_type == 'SHORT' and defect_item0.order <= defect_item1.order:
            self.defect_item0 = defect_item0
            self.defect_item1 = defect_item1
        elif self.defect_type == 'SHORT' and defect_item0.order > defect_item1.order:
            self.defect_item0 = defect_item1
            self.defect_item1 = defect_item0
        self.resistance_short = resistance_short
        self.defect_check()
    def defect_check(self):
        if self.defect_type == 'SHORT':
            if self.defect_item0.name == self.defect_item1.name == 'WL' and self.defect_item0.y == self.defect_item1.y:
                raise('****** Defect Error: the same WL can not short ******')
            elif self.defect_item0.name == self.defect_item1.name == 'BL' and self.defect_item0.x == self.defect_item1.x:
                raise ('****** Defect Error: the same BL can not short ******')
            elif self.defect_item0.name == self.defect_item1.name == 'TISO':
                raise ('****** Defect Error: TISO can not short ******')
            elif self.defect_item0.name == self.defect_item1.name == 'SN' and self.defect_item0.x == self.defect_item1.x and self.defect_item0.y == self.defect_item1.y:
                raise ('****** Defect Error: the same SN can not short ******')

class POINT:
    leackage_rate = 0.99253456
    leackage_time_base = 100           # ns
    def __init__(self, name:str, x:int, y:int, voltage:float, resistance:float, capacitance:float, status:STATUS):
        self.name = name
        self.x = x
        self.y = y
        self.capacitance = capacitance
        self.voltage = voltage
        self.status = status
        self.resistance = resistance
        self.logic = 0
    def __repr__(self):
        return '(name: %s, x: %d, y: %d, voltage: %.2f, resistance: %.2f, capacitance: %.2f, status: %s)\n'%(self.name, self.x, self.y, self.voltage, self.resistance, self.capacitance, self.status)
        # return '%.3f\t'%self.voltage
    def get_logic(self, center, sense_margin):
        if self.voltage <= center - sense_margin:
            self.logic = 0
        elif self.voltage >= center + sense_margin:
            self.logic = 1
        else:
            rate_0 = (center + sense_margin - self.voltage) / (2 * sense_margin)
            rate = random.random()
            if rate < rate_0:
                self.logic = 0
            else:
                self.logic = 1
        return self.logic
    def leackage(self, voltage_target, delay_time):
        self.voltage = voltage_target + (self.voltage - voltage_target)/abs(self.voltage - voltage_target) * (abs(self.voltage - voltage_target))*(POINT.leackage_rate ** (delay_time / POINT.leackage_time_base))
    @staticmethod
    def charge_share(*args):
        """charge share"""
        charge_total = 0
        capacitance_total = 0
        force_point_count = 0
        force_voltage = None
        for point in args:
            charge_total += (point.voltage * point.capacitance)
            capacitance_total += point.capacitance
            if point.status == 'FORCE':
                force_point_count += 1
                force_voltage = point.voltage
        if force_point_count == 0:
            final_voltage = charge_total / capacitance_total
        elif force_point_count == 1:
            final_voltage = force_voltage
        else:
            raise('****** Count Error : FORCE Point count must 0 or 1 ******')
        for point in args:
            point.voltage = final_voltage
    @staticmethod
    def component_voltage(point_list, resistance_list):
        if len(point_list) - len(resistance_list) != 1:
            raise('****** Count Error : the count of point_list must more resistance_list than 1 ******')
        force_point_index_list = []
        for i, point in enumerate(point_list):
            if point.status == 'FORCE':
                force_point_index_list.append(i)
        if len(force_point_index_list) == 0:
            raise('****** Count Error : has not Force Point ******')
        elif len(force_point_index_list) == 1:
            for point in point_list:
                point.voltage = point_list[force_point_index_list[0]].voltage
        else:
            if force_point_index_list[0] != 0:
                for point in point_list[:force_point_index_list[0]]:
                    point.voltage = point_list[force_point_index_list[0]].voltage
            if force_point_index_list[-1] != len(point_list)-1:
                for point in point_list[force_point_index_list[-1]+1:]:
                    point.voltage = point_list[force_point_index_list[-1]].voltage
            for i in range(len(force_point_index_list)-1):
                plst = point_list[force_point_index_list[i] : force_point_index_list[i+1]+1]
                rlst = resistance_list[force_point_index_list[i] : force_point_index_list[i+1]]
                for i in range(1, len(plst)-1):
                    plst[i].voltage = (plst[0].voltage * sum(rlst[i:]) + plst[-1].voltage * sum(rlst[:i]))/(sum(rlst))
    @staticmethod
    def get_force_count(*args):
        count = 0
        for p in args:
            if p.status == 'FORCE':
                count += 1
        return count
    @staticmethod
    def get_force_index(*args):
        index = None
        if POINT.get_force_count(*args) == 1:
            for i, point in enumerate(args):
                if point.status == 'FORCE':
                    index = i
                    break
        return index
    @staticmethod
    def line_short(plst1, resistance1, short_index1, plst2, resistance2, short_index2, short_resistance):
        if len(plst1) <= short_index1:
            raise ('****** Index Error : the count of point_list must more than short index ******')
        force_count1 = POINT.get_force_count(*plst1)
        force_count2 = POINT.get_force_count(*plst2)
        force_index1 = POINT.get_force_index(*plst1)
        force_index2 = POINT.get_force_index(*plst2)
        if force_count1 + force_count2 <= 1:
            POINT.charge_share(*plst1, *plst2)
        elif force_count1 == 1 and force_count2 == 1:
            plst = []
            rlst = []
            if force_index1 < short_index1:
                plst.extend(plst1[force_index1: short_index1 + 1])
                rlst.extend([resistance1] * (short_index1 - force_index1))
            elif force_index1 >= short_index1:
                plst.extend(plst1[short_index1: force_index1 + 1][::-1])
                rlst.extend([resistance1] * (force_index1 - short_index1))
            rlst.append(short_resistance)
            if force_index2 < short_index2:
                plst.extend(plst2[force_index2: short_index2 + 1][::-1])
                rlst.extend([resistance2] * (short_index2 - force_index2))
            elif force_index2 >= short_index2:
                plst.extend(plst2[short_index2: force_index2 + 1])
                rlst.extend([resistance2] * (force_index2 - short_index2))
            POINT.component_voltage(plst, rlst)
            min1 = min(short_index1, force_index1)
            max1 = max(short_index1, force_index1)
            min2 = min(short_index2, force_index2)
            max2 = max(short_index2, force_index2)
            for point in plst1[:min1]:
                point.voltage = plst1[min1].voltage
            for point in plst1[max1 + 1:]:
                point.voltage = plst1[max1].voltage
            for point in plst2[:min2]:
                point.voltage = plst2[min2].voltage
            for point in plst2[max2 + 1:]:
                point.voltage = plst2[max2].voltage
        else:
            raise ('****** Force Point Count Error : has not devolop this function ******')

class RESISTANCE:
    def __init__(self, point0:POINT, point1:POINT, resistance):
        self.point0 = point0
        self.point1 = point1
        self.resistance = resistance

class LINE:
    def __init__(self, POINT_list, RESISTANCE_list):
        if len(POINT_list) - len(RESISTANCE_list) != 1:
            raise('****** Count Error: POINT_list count must more RESISTANCE_list count than 1')
        self.POINT_list = POINT_list
        self.RESISTANCE_list = RESISTANCE_list

class CAPACITANCE:
    def __init__(self, top_electrode:POINT, bottom_electrode:POINT, capacitance:float):
        self.top_electrode = top_electrode
        self.bottom_electrode = bottom_electrode
        self.capacitance = capacitance

class TRANSISTOR:
    def __init__(self, gate:POINT, source:POINT, drain:POINT, vth:float):
        self.gate = gate
        self.source = source
        self.drain = drain
        self.vth = vth

class ARRAY:
    Bit_count = 8

    # sense margin 50mv
    sense_margin = 0.05     # V

    # voltage unit: V
    VTH = 0.3
    VCP = 0.55
    VPP = 2.2
    VWLN = -0.5
    VBB = -0.8
    VBLP = 0.55
    VSN = 0
    VSP = 1.1

    # capacitance unit: fF
    capacitance_CAP = 3.5
    capacitance_BL = 11.985
    capacitance_WL = 22.446
    capacitance_TISO = 10
    capacitance_WLD = 10000000
    capacitance_SA = 10000000
    capacitance_TISO_Drive = 10000000

    # resistance unit: kΩ
    resistance_WL = 46.5
    resistance_BL = 30.1
    resistance_TISO = resistance_WL

    def __init__(self, WL_count, BL_count, defect=None):
        if BL_count % ARRAY.Bit_count != 0:
            raise('****** Number Error: BL_count must is an integer multiple of Bit_count ******')
        self.WL_count = WL_count
        self.BL_count = BL_count
        self.defect = defect
        self.top_electrode = [[POINT('TE', x, y, ARRAY.VCP, 0, ARRAY.capacitance_CAP, 'SENSE') for x in range(BL_count)] for y in range(WL_count)]   ###
        self.bottom_electrode = [[POINT('BE', x, y, ARRAY.VCP, 0, ARRAY.capacitance_CAP, 'SENSE') for x in range(BL_count)] for y in range(WL_count)]
        self.gate = [[POINT('GATE', x, y, ARRAY.VWLN, 0, ARRAY.capacitance_WL/BL_count, 'SENSE') for x in range(BL_count)] for y in range(WL_count)]
        self.drain = [[POINT('DRAIN', x, y, ARRAY.VBLP, 0, ARRAY.capacitance_BL/WL_count, 'SENSE') for x in range(BL_count)] for y in range(WL_count)]
        self.tiso = [[POINT('TISO', x, y, ARRAY.VBB, 0, ARRAY.capacitance_TISO/BL_count, 'SENSE') for x in range(BL_count)] for y in range(int(WL_count/2)+1)]
        self.__get_WLD()
        self.__get_SA()
        self.__get_TISO_Drive()
        self.POINT_WL = [[self.WLD[y][0]]+[self.gate[y][x] for x in range(BL_count)]+[self.WLD[y][-1]] for y in range(WL_count)]
        # self.RESIST_WL = [[RESISTANCE(self.POINT_WL[y][x], self.POINT_WL[y][x+1], ARRAY.resitance_WL/(BL_count+1)) for x in range(BL_count+1)] for y in range(WL_count+1)]
        self.POINT_BL = [[self.SA[x][0]]+[self.drain[y][x] for y in range(WL_count)]+[self.SA[x][-1]] for x in range(BL_count)]
        # self.RESIST_BL = [[RESISTANCE]]
        self.POINT_TISO = [[self.TISO_Drive[y][0]]+[self.tiso[y][x] for x in range(BL_count)]+[self.TISO_Drive[y][-1]] for y in range(int(WL_count / 2) + 1)]
        self.ra_address = -1
        self.ca_address = -1
    def __get_WLD(self):
        self.WLD = []
        for i in range(self.WL_count):
            if i % 4 == 0 or i % 4 == 3:
                self.WLD.append([POINT('WLD', 0, i, ARRAY.VWLN, 0, ARRAY.capacitance_WLD, 'FORCE'), POINT('DUMMY', -1, i, ARRAY.VWLN, 0, 0, 'SENSE')])
            elif i % 4 == 1 or i % 4 == 2:
                self.WLD.append([POINT('DUMMY', 0, i, ARRAY.VWLN, 0, 0, 'SENSE'), POINT('WLD', -1, i, ARRAY.VWLN, 0, ARRAY.capacitance_WLD, 'FORCE')])
    def __get_SA(self):
        self.SA = []
        for i in range(self.BL_count):
            if i % 2 == 0:
                self.SA.append([POINT('SA', i, 0, ARRAY.VBLP, 0, ARRAY.capacitance_SA, 'FORCE'), POINT('DUMMY', i, -1, ARRAY.VBLP, 0, 0, 'SENSE')])
            elif i % 2 == 1:
                self.SA.append([POINT('DUMMY', i, 0, ARRAY.VBLP, 0, 0, 'SENSE'), POINT('SA', i, -1, ARRAY.VBLP, 0, ARRAY.capacitance_SA, 'FORCE')])
    def __get_TISO_Drive(self):
        self.TISO_Drive = []
        for i in range(int(self.WL_count/2)+1):
            if i % 2 == 0:
                self.TISO_Drive.append([POINT('DUMMY', 0, i, ARRAY.VBB, 0, 0, 'SENSE'), POINT('TISO_Drive', 0, i, ARRAY.VBB, 0, ARRAY.capacitance_TISO_Drive, 'FORCE')])

            elif i % 2 == 1:
                self.TISO_Drive.append([POINT('TISO_Drive', 0, i, ARRAY.VBB, 0, ARRAY.capacitance_TISO_Drive, 'FORCE'), POINT('DUMMY', 0, i, ARRAY.VBB, 0, 0, 'SENSE')])

    def inital(self):
        self.PRECHARGE()
        for wl_index in range(self.WL_count):
            for bl_index in range(self.BL_count):
                self.bottom_electrode[wl_index][bl_index].voltage = ARRAY.VBLP
        self.PRECHARGE()
        self.ra_address = -1
        self.ca_address = -1

    def __ACTIVE_NORMAL(self):
        POINT.charge_share(*self.POINT_WL[self.ra_address])
    def __ACTIVE_WL_OPEN(self):
        POINT.charge_share(*self.POINT_WL[self.ra_address][:self.defect.defect_item0.x + 1])
        POINT.charge_share(*self.POINT_WL[self.ra_address][self.defect.defect_item0.x + 1:])
    def __ACTIVE_WL_WL_SHORT(self):
        POINT.line_short(self.POINT_WL[self.defect.defect_item0.y], ARRAY.resistance_WL / (self.BL_count + 1),
                         self.defect.defect_item0.x + 1,
                         self.POINT_WL[self.defect.defect_item1.y], ARRAY.resistance_WL / (self.BL_count + 1),
                         self.defect.defect_item1.x + 1,
                         self.defect.resistance_short)
    def __ACTIVE_WL_BL_SHORT(self):
        POINT.line_short(self.POINT_WL[self.ra_address], ARRAY.resistance_WL / (self.BL_count + 1),
                         self.defect.defect_item0.x + 1,
                         self.POINT_BL[self.defect.defect_item1.x][1:-1], ARRAY.resistance_BL / (self.WL_count + 1),
                         self.defect.defect_item1.y + 1,
                         self.defect.resistance_short)
        # plst = []
        # plst.extend(self.POINT_WL[self.ra_address])
        # for i in range(self.WL_count):
        #     plst.append(self.drain[i][self.defect.defect_item1.x])
        # POINT.charge_share(*plst)
    def __ACTIVE_WL_TISO_SHORT(self):
        POINT.line_short(self.POINT_WL[self.ra_address], ARRAY.resistance_WL / (self.BL_count + 1),
                         self.defect.defect_item0.x + 1,
                         self.POINT_TISO[self.defect.defect_item1.y], ARRAY.resistance_TISO / (self.BL_count + 1),
                         self.defect.defect_item1.x + 1,
                         self.defect.resistance_short)
    def __ACTIVE_WL_SN_SHORT(self):
        plst = []
        plst.extend(self.POINT_WL[self.ra_address])
        plst.append(self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x])
        POINT.charge_share(*plst)
    def ACTIVE(self, ra_address:int): # open WL
        self.ra_address = ra_address
        self.POINT_WL[self.ra_address][0].voltage = ARRAY.VPP
        self.POINT_WL[self.ra_address][-1].voltage = ARRAY.VPP
        if self.defect == None:
            self.__ACTIVE_NORMAL()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item0.y == self.ra_address:
            self.__ACTIVE_WL_OPEN()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'WL' and (self.defect.defect_item0.y == self.ra_address or self.defect.defect_item1.y == self.ra_address):
            self.__ACTIVE_WL_WL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'BL' and self.defect.defect_item0.y == self.ra_address:
            self.__ACTIVE_WL_BL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'TISO' and self.defect.defect_item0.y == self.ra_address:
            self.__ACTIVE_WL_TISO_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'SN' and self.defect.defect_item0.y == self.ra_address:
            self.__ACTIVE_WL_SN_SHORT()
        else:
            self.__ACTIVE_NORMAL()

    def __SENSE_NORMAL(self):
        for bl_index in range(self.BL_count):
            plst = []
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __SENSE_BL_OPEN(self):
        for bl_index in range(self.BL_count):
            if self.defect.defect_item0.x == bl_index:
                plst0 = []
                plst1 = []
                for wl_index in range(self.WL_count):
                    if wl_index < self.defect.defect_item0.y:
                        plst0.append(self.drain[wl_index][bl_index])
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst0.append(self.bottom_electrode[wl_index][bl_index])
                    else: # elif wl_index >= self.defect.defect_item0.y:
                        plst1.append(self.drain[wl_index][bl_index])
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst1.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst0)
                POINT.charge_share(*plst1)
            else:
                plst = []
                for wl_index in range(self.WL_count):
                    plst.append(self.drain[wl_index][bl_index])
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def __SENSE_SN_OPEN(self):
        for bl_index in range(self.BL_count):
            plst = []
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH and not (bl_index == self.defect.defect_item0.x and wl_index == self.defect.defect_item0.y):
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __SENSE_WL_BL_SHORT(self):
        for bl_index in range(self.BL_count):
            plst = []
            if self.defect.defect_item1.x == bl_index:
                plst.extend(self.POINT_WL[self.defect.defect_item0.y][:])
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __SENSE_WL_SN_SHORT(self):
        for bl_index in range(self.BL_count):
            plst = []
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
                    if self.defect.defect_item1.x == bl_index and self.defect.defect_item1.y == wl_index:
                        plst.extend(self.POINT_WL[self.defect.defect_item0.y])
            POINT.charge_share(*plst)
    def __SENSE_BL_BL_SHORT(self):
        short_bl_index0 = self.defect.defect_item0.x
        short_bl_index1 = self.defect.defect_item1.x
        short_bl_index = (min(short_bl_index0, short_bl_index1), max(short_bl_index0, short_bl_index1))
        for bl_index in range(self.BL_count):
            if bl_index == short_bl_index[1]:
                continue
            plst = []
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
                if bl_index == short_bl_index[0]:
                    plst.append(self.drain[wl_index][short_bl_index[1]])
                    if self.gate[wl_index][short_bl_index[1]].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][short_bl_index[1]])
            POINT.charge_share(*plst)
    def __SENSE_BL_TISO_SHORT(self):
        for bl_index in range(self.BL_count):
            plst = []
            if self.defect.defect_item0.x == bl_index:
                plst.extend(self.POINT_TISO[self.defect.defect_item1.y][:])
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __SENSE_TISO_SN_SHORT(self):
        for bl_index in range(self.BL_count):
            plst = []
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
                    if self.defect.defect_item1.x == bl_index and self.defect.defect_item1.y == wl_index:
                        plst.extend(self.POINT_TISO[self.defect.defect_item0.y])
            POINT.charge_share(*plst)
    def __SENSE_SN_SN_SHORT(self):
        d0x = self.defect.defect_item0.x
        d0y = self.defect.defect_item0.y
        d1x = self.defect.defect_item1.x
        d1y = self.defect.defect_item1.y
        for bl_index in range(self.BL_count):
            if bl_index == d0x or bl_index == d1x:
                if self.gate[d0y][d0x].voltage >= ARRAY.VTH and self.gate[d1y][d1x].voltage >= ARRAY.VTH:
                    plst = []
                    for wl_index in range(self.WL_count):
                        plst.append(self.drain[wl_index][d0x])
                        plst.append(self.drain[wl_index][d1x])
                        if self.gate[wl_index][d0x].voltage >= ARRAY.VTH:
                            plst.append(self.bottom_electrode[wl_index][d0x])
                        if self.gate[wl_index][d1x].voltage >= ARRAY.VTH:
                            plst.append(self.bottom_electrode[wl_index][d1x])
                    POINT.charge_share(*plst)
                elif self.gate[d0y][d0x].voltage >= ARRAY.VTH and self.gate[d1y][d1x].voltage < ARRAY.VTH:
                    if bl_index == d0x:
                        plst = []
                        for wl_index in range(self.WL_count):
                            plst.append(self.drain[wl_index][bl_index])
                            if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                                plst.append(self.bottom_electrode[wl_index][bl_index])
                        plst.append(self.bottom_electrode[d1y][d1x])
                        POINT.charge_share(*plst)
                    elif bl_index == d1x:
                        plst = []
                        for wl_index in range(self.WL_count):
                            plst.append(self.drain[wl_index][bl_index])
                            if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                                plst.append(self.bottom_electrode[wl_index][bl_index])
                        POINT.charge_share(*plst)
                elif self.gate[d0y][d0x].voltage < ARRAY.VTH and self.gate[d1y][d1x].voltage >= ARRAY.VTH:
                    if bl_index == d0x:
                        plst = []
                        for wl_index in range(self.WL_count):
                            plst.append(self.drain[wl_index][bl_index])
                            if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                                plst.append(self.bottom_electrode[wl_index][bl_index])
                        POINT.charge_share(*plst)
                    elif bl_index == d1x:
                        plst = []
                        for wl_index in range(self.WL_count):
                            plst.append(self.drain[wl_index][bl_index])
                            if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                                plst.append(self.bottom_electrode[wl_index][bl_index])
                        plst.append(self.bottom_electrode[d0y][d0x])
                        POINT.charge_share(*plst)
                elif self.gate[d0y][d0x].voltage < ARRAY.VTH and self.gate[d1y][d1x].voltage < ARRAY.VTH:
                    plst = []
                    for wl_index in range(self.WL_count):
                        plst.append(self.drain[wl_index][bl_index])
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst.append(self.bottom_electrode[wl_index][bl_index])
                    POINT.charge_share(*plst)
            else:
                plst = []
                for wl_index in range(self.WL_count):
                    plst.append(self.drain[wl_index][bl_index])
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def SENSE(self):
        if self.defect == None:
            self.__SENSE_NORMAL()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'BL':
            self.__SENSE_BL_OPEN()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'SN':
            self.__SENSE_SN_OPEN()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'BL':
            self.__SENSE_WL_BL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'SN':
            self.__SENSE_WL_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item1.name == 'BL':
            self.__SENSE_BL_BL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item1.name == 'TISO':
            self.__SENSE_BL_TISO_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'TISO' and self.defect.defect_item1.name == 'SN':
            self.__SENSE_TISO_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'SN' and self.defect.defect_item1.name == 'SN':
            self.__SENSE_SN_SN_SHORT()
        else:
            self.__SENSE_NORMAL()

    def __AMPLIFY_NORMAL(self):
        for bl_index in range(self.BL_count):
            self.POINT_BL[bl_index][0].voltage = self.POINT_BL[bl_index][1].voltage
            self.POINT_BL[bl_index][0].get_logic(ARRAY.VBLP, ARRAY.sense_margin)
            self.POINT_BL[bl_index][-1].voltage = self.POINT_BL[bl_index][-2].voltage
            self.POINT_BL[bl_index][-1].get_logic(ARRAY.VBLP, ARRAY.sense_margin)
    def __AMPLIFY_BLn0_OPEN(self):
        for bl_index in range(self.BL_count):
            if bl_index != self.defect.defect_item0.x:
                self.POINT_BL[bl_index][0].voltage = self.POINT_BL[bl_index][1].voltage
                self.POINT_BL[bl_index][0].get_logic(ARRAY.VBLP, ARRAY.sense_margin)
            self.POINT_BL[bl_index][-1].voltage = self.POINT_BL[bl_index][-2].voltage
            self.POINT_BL[bl_index][-1].get_logic(ARRAY.VBLP, ARRAY.sense_margin)
    def AMPLIFY(self):
        if self.defect == None:
            self.__AMPLIFY_NORMAL()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item0.y == 0:
            self.__AMPLIFY_BLn0_OPEN()
        else:
            self.__AMPLIFY_NORMAL()

    def __WRITEBACK_NORMAL(self):
        for bl_index in range(self.BL_count):
            plst = [self.POINT_BL[bl_index][0], self.POINT_BL[bl_index][-1]]
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __WRITEBACK_BL_OPEN(self):
        for bl_index in range(self.BL_count):
            if self.defect.defect_item0.x == bl_index:
                plst0 = [self.POINT_BL[bl_index][0]]
                plst1 = [self.POINT_BL[bl_index][-1]]
                for wl_index in range(self.WL_count):
                    if wl_index < self.defect.defect_item0.y:
                        plst0.append(self.drain[wl_index][bl_index])
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst0.append(self.bottom_electrode[wl_index][bl_index])
                    else:  # elif wl_index >= self.defect.defect_item0.y:
                        plst1.append(self.drain[wl_index][bl_index])
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst1.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst0)
                POINT.charge_share(*plst1)
            else:
                plst = [self.POINT_BL[bl_index][0], self.POINT_BL[bl_index][-1]]
                for wl_index in range(self.WL_count):
                    plst.append(self.drain[wl_index][bl_index])
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def __WRITEBACK_SN_OPEN(self):
        for bl_index in range(self.BL_count):
            plst = [self.POINT_BL[bl_index][0], self.POINT_BL[bl_index][-1]]
            for wl_index in range(self.WL_count):
                plst.append(self.drain[wl_index][bl_index])
                if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH and not (bl_index == self.defect.defect_item0.x and wl_index == self.defect.defect_item0.y):
                    plst.append(self.bottom_electrode[wl_index][bl_index])
            POINT.charge_share(*plst)
    def __WRITEBACK_WL_BL_SHORT(self):
        plst = []
        rlst = []
        if self.defect.defect_item0.y % 4 == 0 or self.defect.defect_item0.y % 4 == 3:
            plst.extend(self.POINT_WL[self.defect.defect_item0.y][:self.defect.defect_item0.x + 2])
            rlst.extend([ARRAY.resistance_WL / (self.WL_count + 1)] * (self.defect.defect_item0.x + 1))
            rlst.append(self.defect.resistance_short)
        elif self.defect.defect_item0.y % 4 == 1 or self.defect.defect_item0.y % 4 == 2:
            plst.extend(self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1:][::-1])
            rlst.extend([ARRAY.resistance_WL / (self.WL_count + 1)] * (self.BL_count - self.defect.defect_item0.x))
            rlst.append(self.defect.resistance_short)
        if self.defect.defect_item1.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1:])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item1.y))
        elif self.defect.defect_item1.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 2][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item1.y + 1))
        POINT.component_voltage(plst, rlst)
        if self.defect.defect_item0.y % 4 == 0 or self.defect.defect_item0.y % 4 == 3:
            for point in self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 2:]:
                point.voltage = self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1].voltage
        elif self.defect.defect_item0.y % 4 == 1 or self.defect.defect_item0.y % 4 == 2:
            for point in self.POINT_WL[self.defect.defect_item0.y][:self.defect.defect_item0.x + 1]:
                point.voltage = self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1].voltage
        if self.defect.defect_item1.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        elif self.defect.defect_item1.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        for bl_index in range(self.BL_count):
            if bl_index == self.defect.defect_item1.x:
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        self.bottom_electrode[wl_index][bl_index].voltage = self.drain[wl_index][bl_index].voltage
            else:
                plst = []
                plst.extend(self.POINT_BL[bl_index])
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def __WRITEBACK_WL_SN_SHORT(self):
        if self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage < ARRAY.VTH:
            self.__WRITEBACK_NORMAL()
            self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage = self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage
        else:
            self.__WRITEBACK_WL_BL_SHORT()
    def __WRITEBACK_BL_BL_SHORT(self):
        plst = []
        rlst = []
        if self.defect.defect_item0.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 2])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item0.y + 1))
            rlst.append(self.defect.resistance_short)
        elif self.defect.defect_item0.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1:][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item0.y))
            rlst.append(self.defect.resistance_short)
        if self.defect.defect_item1.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 2][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item1.y + 1))
        elif self.defect.defect_item1.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1:])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item1.y))
        POINT.component_voltage(plst, rlst)
        if self.defect.defect_item0.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        elif self.defect.defect_item0.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        if self.defect.defect_item1.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        elif self.defect.defect_item1.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        for bl_index in range(self.BL_count):
            if bl_index == self.defect.defect_item0.x or bl_index == self.defect.defect_item1.x:
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        self.bottom_electrode[wl_index][bl_index].voltage = self.drain[wl_index][bl_index].voltage
            else:
                plst = []
                plst.extend(self.POINT_BL[bl_index])
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def __WRITEBACK_BL_TISO_SHORT(self):
        plst = []
        rlst = []
        if self.defect.defect_item0.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 2])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item0.y + 1))
            rlst.append(self.defect.resistance_short)
        elif self.defect.defect_item0.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1:][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item0.y))
            rlst.append(self.defect.resistance_short)
        if self.defect.defect_item1.y % 2 == 0:
            plst.extend(self.POINT_TISO[self.defect.defect_item1.y][self.defect.defect_item1.x + 1:])
            rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.BL_count - self.defect.defect_item1.x))
        elif self.defect.defect_item1.x % 2 == 1:
            plst.extend(self.POINT_TISO[self.defect.defect_item1.y][self.defect.defect_item1.x + 1:][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.defect.defect_item1.x + 1))
        POINT.component_voltage(plst, rlst)
        if self.defect.defect_item0.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        elif self.defect.defect_item0.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        for bl_index in range(self.BL_count):
            if bl_index == self.defect.defect_item0.x:
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        self.bottom_electrode[wl_index][bl_index].voltage = self.drain[wl_index][bl_index].voltage
            else:
                plst = []
                plst.extend(self.POINT_BL[bl_index])
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
    def __WRITEBACK_TISO_SN_SHORT(self):
        if self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage < ARRAY.VTH:
            self.__WRITEBACK_NORMAL()
        else:
            plst = []
            rlst = []
            if self.defect.defect_item1.x % 2 == 0:
                plst.extend(self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 2])
                rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item1.y + 1))
                rlst.append(self.defect.resistance_short)
            elif self.defect.defect_item1.x % 2 == 1:
                plst.extend(self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1:][::-1])
                rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item1.y))
                rlst.append(self.defect.resistance_short)
            if self.defect.defect_item0.y % 2 == 0:
                plst.extend(self.POINT_TISO[self.defect.defect_item0.y][self.defect.defect_item0.x + 1:])
                rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.BL_count - self.defect.defect_item0.x))
            elif self.defect.defect_item0.y % 2 == 1:
                plst.extend(self.POINT_TISO[self.defect.defect_item0.y][:self.defect.defect_item0.x + 2][::-1])
                rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.defect.defect_item0.x + 1))
            POINT.component_voltage(plst, rlst)
            if self.defect.defect_item1.x % 2 == 0:
                for point in self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 2:]:
                    point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
            elif self.defect.defect_item1.x % 2 == 1:
                for point in self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 1]:
                    point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
            for bl_index in range(self.BL_count):
                if bl_index == self.defect.defect_item1.x:
                    for wl_index in range(self.WL_count):
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            self.bottom_electrode[wl_index][bl_index].voltage = self.drain[wl_index][bl_index].voltage
                else:
                    plst = []
                    plst.extend(self.POINT_BL[bl_index])
                    for wl_index in range(self.WL_count):
                        if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                            plst.append(self.bottom_electrode[wl_index][bl_index])
                    POINT.charge_share(*plst)
    def __WRITEBACK_SN_SN_SHORT(self):
        if self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage >= ARRAY.VTH and self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage >= ARRAY.VTH:
            self.__WRITEBACK_BL_BL_SHORT()
        elif self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage >= ARRAY.VTH and self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage < ARRAY.VTH:
            self.__WRITEBACK_NORMAL()
            self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage = self.bottom_electrode[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage
        elif self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage < ARRAY.VTH and self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage >= ARRAY.VTH:
            self.__WRITEBACK_NORMAL()
            self.bottom_electrode[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage = self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage
        elif self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage < ARRAY.VTH and self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage < ARRAY.VTH:
            self.__WRITEBACK_NORMAL()
    def WRITEBACK(self):
        for bl_index in range(self.BL_count):
            if self.POINT_BL[bl_index][-1 * (bl_index % 2)].logic == 0:
                self.POINT_BL[bl_index][-1 * (bl_index % 2)].voltage = ARRAY.VSN
            elif self.POINT_BL[bl_index][-1 * (bl_index % 2)].logic == 1:
                self.POINT_BL[bl_index][-1 * (bl_index % 2)].voltage = ARRAY.VSP
        if self.defect == None:
            self.__WRITEBACK_NORMAL()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'BL':
            self.__WRITEBACK_BL_OPEN()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'SN':
            self.__WRITEBACK_SN_OPEN()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'BL':
            self.__WRITEBACK_WL_BL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'SN':
            self.__WRITEBACK_WL_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item1.name == 'BL':
            self.__WRITEBACK_BL_BL_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item1.name == 'TISO':
            self.__WRITEBACK_BL_TISO_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'TISO' and self.defect.defect_item1.name == 'SN':
            self.__WRITEBACK_TISO_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'SN' and self.defect.defect_item1.name == 'SN':
            self.__WRITEBACK_SN_SN_SHORT()
        else:
            self.__WRITEBACK_NORMAL()

    def __PRECHARGE_NORMAL(self):
        for wl in self.POINT_WL:
            POINT.charge_share(*wl)
        for bl in self.POINT_BL:
            POINT.charge_share(*bl)
    def __PRECHARGE_WL_OPEN(self):
        POINT.charge_share(*self.POINT_WL[self.defect.defect_item0.y][:self.defect.defect_item0.x+1])
        POINT.charge_share(*self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x+1:])
        for wl_index, wl in enumerate(self.POINT_WL):
            if wl_index == self.defect.defect_item0.y:
                continue
            POINT.charge_share(*wl)
        for bl in self.POINT_BL:
            POINT.charge_share(*bl)
    def __PRECHARGE_BL_OPEN(self):
        POINT.charge_share(*self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 1])
        POINT.charge_share(*self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1:])
        for wl in self.POINT_WL:
            POINT.charge_share(*wl)
        for bl_index, bl in enumerate(self.POINT_BL):
            if bl_index == self.defect.defect_item0.x:
                continue
            POINT.charge_share(*bl)
    def __PRECHARGE_WL_BL_SHORT(self):
        plst = []
        rlst = []
        if self.defect.defect_item0.y % 4 == 0 or self.defect.defect_item0.y % 4 == 3:
            plst.extend(self.POINT_WL[self.defect.defect_item0.y][:self.defect.defect_item0.x + 2])
            rlst.extend([ARRAY.resistance_WL / (self.BL_count + 1)] * (self.defect.defect_item0.x + 1))
            rlst.append(self.defect.resistance_short)
        elif self.defect.defect_item0.y % 4 == 1 or self.defect.defect_item0.y % 4 == 2:
            plst.extend(self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1:][::-1])
            rlst.extend([ARRAY.resistance_WL / (self.BL_count + 1)] * (self.BL_count - self.defect.defect_item0.x))
            rlst.append(self.defect.resistance_short)
        if self.defect.defect_item1.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1:])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item1.y))
        elif self.defect.defect_item1.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 2][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item1.y + 1))
        POINT.component_voltage(plst, rlst)
        if self.defect.defect_item0.y % 4 == 0 or self.defect.defect_item0.y % 4 == 3:
            for point in self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 2:]:
                point.voltage = self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1].voltage
        elif self.defect.defect_item0.y % 4 == 1 or self.defect.defect_item0.y % 4 == 2:
            for point in self.POINT_WL[self.defect.defect_item0.y][:self.defect.defect_item0.x + 1]:
                point.voltage = self.POINT_WL[self.defect.defect_item0.y][self.defect.defect_item0.x + 1].voltage
        if self.defect.defect_item1.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        elif self.defect.defect_item1.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item1.x][:self.defect.defect_item1.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item1.x][self.defect.defect_item1.y + 1].voltage
        for wl_index, wl in enumerate(self.POINT_WL):
            if wl_index != self.defect.defect_item0.y:
                POINT.charge_share(*wl)
        for bl_index in range(self.BL_count):
            if bl_index == self.defect.defect_item1.x:
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        self.bottom_electrode[wl_index][bl_index].voltage = self.drain[wl_index][bl_index].voltage
            else:
                plst = []
                plst.extend(self.POINT_BL[bl_index])
                for wl_index in range(self.WL_count):
                    if self.gate[wl_index][bl_index].voltage >= ARRAY.VTH:
                        plst.append(self.bottom_electrode[wl_index][bl_index])
                POINT.charge_share(*plst)
        plst = []
        plst.extend(self.POINT_WL[self.defect.defect_item0.y])
        plst.extend(self.POINT_BL[self.defect.defect_item1.x][1:-1])
        POINT.charge_share(*plst)
    def __PRECHARGE_WL_SN_SHORT(self):
        for wl_index, wl in enumerate(self.POINT_WL):
            plst = []
            if wl_index == self.defect.defect_item0.y:
                plst.append(self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x])
            plst.extend(wl)
            POINT.charge_share(*plst)
        for bl in self.POINT_BL:
            POINT.charge_share(*bl)
    def __PRECHARGE_BL_TISO_SHORT(self):
        plst = []
        rlst = []
        if self.defect.defect_item0.x % 2 == 0:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 2])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.defect.defect_item0.y + 1))
            rlst.append(self.defect.resistance_short)
        elif self.defect.defect_item0.x % 2 == 1:
            plst.extend(self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1:][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.WL_count + 1)] * (self.WL_count - self.defect.defect_item0.y))
            rlst.append(self.defect.resistance_short)
        if self.defect.defect_item1.y % 2 == 0:
            plst.extend(self.POINT_TISO[self.defect.defect_item1.y][self.defect.defect_item1.x + 1:])
            rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.BL_count - self.defect.defect_item1.x))
        elif self.defect.defect_item1.x % 2 == 1:
            plst.extend(self.POINT_TISO[self.defect.defect_item1.y][:self.defect.defect_item1.x + 2][::-1])
            rlst.extend([ARRAY.resistance_BL / (self.BL_count + 1)] * (self.defect.defect_item1.x + 1))
        POINT.component_voltage(plst, rlst)
        if self.defect.defect_item0.x % 2 == 0:
            for point in self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 2:]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        elif self.defect.defect_item0.x % 2 == 1:
            for point in self.POINT_BL[self.defect.defect_item0.x][:self.defect.defect_item0.y + 1]:
                point.voltage = self.POINT_BL[self.defect.defect_item0.x][self.defect.defect_item0.y + 1].voltage
        for wl in self.POINT_WL:
            POINT.charge_share(*wl)
        for bl_index, bl in enumerate(self.POINT_BL):
            if bl_index == self.defect.defect_item0.x:
                continue
            POINT.charge_share(*bl)
    def __PRECHARGE_TISO_SN_SHORT(self):
        for wl in self.POINT_WL:
            POINT.charge_share(*wl)
        for bl in self.POINT_BL:
            POINT.charge_share(*bl)
        self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage = ARRAY.VBB
    def __PRECHARGE_SN_SN_SHORT(self):
        for wl in self.POINT_WL:
            POINT.charge_share(*wl)
        for bl in self.POINT_BL:
            POINT.charge_share(*bl)
        POINT.charge_share(*[self.bottom_electrode[self.defect.defect_item0.y][self.defect.defect_item0.x], self.bottom_electrode[self.defect.defect_item1.y][self.defect.defect_item1.x]])
    def PRECHARGE(self):
        for wl in self.POINT_WL:
            wl[0].voltage = ARRAY.VWLN
            wl[-1].voltage = ARRAY.VWLN
        for bl in self.POINT_BL:
            bl[0].voltage = ARRAY.VBLP
            bl[-1].voltage = ARRAY.VBLP
        if self.defect == None:
            self.__PRECHARGE_NORMAL()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'WL':
            self.__PRECHARGE_WL_OPEN()
        elif self.defect.defect_type == 'OPEN' and self.defect.defect_item0.name == 'BL':
            self.__PRECHARGE_BL_OPEN()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'BL':
            self.__PRECHARGE_WL_BL_SHORT()
        # elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'TISO':
        #     self.__PRECHARGE_WL_TISO_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'WL' and self.defect.defect_item1.name == 'SN':
            self.__PRECHARGE_WL_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'BL' and self.defect.defect_item1.name == 'TISO':
            self.__PRECHARGE_BL_TISO_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'TISO' and self.defect.defect_item1.name == 'SN':
            self.__PRECHARGE_TISO_SN_SHORT()
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'SN' and self.defect.defect_item1.name == 'SN':
            self.__PRECHARGE_SN_SN_SHORT()
        else:
            self.__PRECHARGE_NORMAL()

    def READ(self, ca_address:int): # read logic data from SA
        self.ca_address = ca_address
        self.SENSE()
        self.AMPLIFY()
        self.WRITEBACK()
        dout = 0
        for bl_index in range(self.ca_address * 8, self.ca_address * 8 + 8):
            dout = dout << 1
            dout = dout + self.POINT_BL[bl_index][-1 * (bl_index % 2)].logic
        return dout
    def WRITE(self, ca_address, data): # write logic data into SA
        self.ca_address = ca_address
        self.SENSE()
        self.AMPLIFY()
        for bl_index in range(ca_address * 8, ca_address * 8 + 8):
            self.POINT_BL[bl_index][-1 * (bl_index % 2)].logic = ((data >> (7 - (bl_index % 8))&1))
        self.WRITEBACK()

    def __DELAY_NORMAL(self, time):
        for wl_index in range(self.WL_count):
            for bl_index in range(self.BL_count):
                if self.gate[wl_index][bl_index].voltage < ARRAY.VTH:
                    self.bottom_electrode[wl_index][bl_index].leackage(ARRAY.VCP, time)
    def __DELALY_OTHERS_SN_SHORT(self, time):
        for wl_index in range(self.WL_count):
            for bl_index in range(self.BL_count):
                if self.gate[wl_index][bl_index].voltage < ARRAY.VTH:
                    if self.defect.defect_item1.x == bl_index and self.defect.defect_item1.y == wl_index:
                        continue
                    self.bottom_electrode[wl_index][bl_index].leackage(ARRAY.VCP, time)
    def __DELAY_SN_SN_SHORT(self, time):
        if self.gate[self.defect.defect_item0.y][self.defect.defect_item0.x].voltage < ARRAY.VTH and self.gate[self.defect.defect_item1.y][self.defect.defect_item1.x].voltage < ARRAY.VTH:
            self.__DELAY_NORMAL(time)
        else:
            for wl_index in range(self.WL_count):
                for bl_index in range(self.BL_count):
                    if self.gate[wl_index][bl_index].voltage < ARRAY.VTH:
                        if (self.defect.defect_item0.x == bl_index and self.defect.defect_item0.y == wl_index) or (self.defect.defect_item1.x == bl_index and self.defect.defect_item1.y == wl_index):
                            continue
                        self.bottom_electrode[wl_index][bl_index].leackage(ARRAY.VCP, time)
    def DELAY(self, time):
        if self.defect == None:
            self.__DELAY_NORMAL(time)
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name != 'SN' and self.defect.defect_item1.name == 'SN':
            self.__DELALY_OTHERS_SN_SHORT(time)
        elif self.defect.defect_type == 'SHORT' and self.defect.defect_item0.name == 'SN' and self.defect.defect_item1.name == 'SN':
            self.__DELAY_SN_SN_SHORT(time)
        else:
            self.__DELAY_NORMAL(time)

def NOTs(data, length=8):
    data_str = bin(data).lstrip('0b').rjust(length, '0')
    data_rst = '0b'
    for i in data_str:
        if i == '0':
            data_rst += '1'
        else:
            data_rst += '0'
    return eval(data_rst)

class debug:
    @staticmethod
    def print_mark(*args):
        print('********** debug mark **********')
        print(*args)
    @staticmethod
    def print_point(plst):
        if type(plst) == list:
            for point in plst:
                debug.print_point(point)
            print()
        elif type(plst) == POINT:
            print(plst, end='')
        else:
            raise ('****** type Error ******')
    @staticmethod
    def print_name(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_name(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%s' % (plst.name), end='\t')
        else:
            raise ('****** type Error ******')
    @staticmethod
    def print_voltage(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_voltage(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%.3f' % plst.voltage, end='\t')
        else:
            print('****** type Error ******')
    @staticmethod
    def print_logic(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_logic(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%d' % plst.logic, end='\t')
        else:
            raise ('****** type Error ******')
    @staticmethod
    def print_status(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_status(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%s'%(plst.status[0]), end='\t')
        else:
            raise('****** type Error ******')
    @staticmethod
    def print_voltage_logic(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_voltage_logic(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%.3f(%d)' % (plst.voltage, plst.logic), end='\t')
        else:
            raise ('****** type Error ******')
    @staticmethod
    def print_voltage_status(plst, mark='', n=0):
        if n == 0:
            print(mark, ':')
        if type(plst) == list:
            n += 1
            for point in plst:
                debug.print_voltage_status(point, mark=mark, n=n)
            print()
        elif type(plst) == POINT:
            print('%.3f(%s)' % (plst.voltage, plst.status[0]), end='\t')
        else:
            raise ('****** type Error ******')

def __ArrayDebug():
    ARRAY_TEST = 0
    DEBUG_TEST = 1
    OTHER_TEST = 2

    index = ARRAY_TEST

    if index == ARRAY_TEST:
        wl_count = 4
        bl_count = 8

        item0 = ITEM('WL', 4, 2)
        item1 = ITEM('WL', 4, 3)
        defect = DEFECT('SHORT', item0, item1, 1)
        # defect = None

        a = ARRAY(wl_count, bl_count, defect)
        a.PRECHARGE()

        # Write
        print('WRITE:')
        for ra in range(wl_count):
            for ca in range(bl_count//8):
                data0 = 0xaa
                if ra % 2 == 0:
                    data = data0
                else:
                    data = NOTs(data0)
                print('0x%s'%(hex(data).lstrip('0x').rjust(2, '0')), end='\t')
                a.ACTIVE(ra)
                a.WRITE(ca, data)
                a.PRECHARGE()
            print()
        print()

        # Read
        print('READ:')
        for ra in range(wl_count):
            for ca in range(bl_count//8):
                a.ACTIVE(ra)
                data = a.READ(ca)
                print('0x%s'%(hex(data).lstrip('0x').rjust(2, '0')), end='\t')
                a.PRECHARGE()
            print()

    elif index == DEBUG_TEST:
        wl_count = 4
        bl_count = 8

        item0 = ITEM('SN', 4, 2)
        item1 = ITEM('SN', 5, 2)
        defect = DEFECT('SHORT', item0, item1, 1)

        a = ARRAY(wl_count, bl_count, defect)

        a.PRECHARGE()
        print('Write data:')
        for ra in range(wl_count):
            for ca in range(int(bl_count / 8)):
                if ra % 2 == 0:
                    data = 0xaa
                else:
                    data = 0x55
                print('%s'%(str(hex(data))), end='\t')
                a.ACTIVE(ra)
                a.WRITE(ca, data)
                a.PRECHARGE()
                # breakpoint()
            print()

        print()
        print('Read data:')
        for ra in range(wl_count):
            for ca in range(int(bl_count / 8)):
                a.ACTIVE(ra)
                data = a.READ(ca)
                print('%s' % (str(hex(data))), end='\t')
                a.PRECHARGE()
            print()

    elif index == OTHER_TEST:
        a = [[[POINT('g%d'%g, c, r, 0, 0, 0, 'SENSE') for c in range(10)] for r in range(10)]for g in range(2)]
        debug.print_point(a)

def shrmoo_pattern(i):
    parm = [
        (8, 0x00, False, False),
        (8, 0xff, False, False),
        (8, 0x55, True, False),
        (1, 0x00, False, False),
        (1, 0xff, False, False),
        (1, 0x55, True, False),
        (8, 0x00, False, True),
        (8, 0xff, False, True),
        (8, 0x55, True, True),
        (1, 0x00, False, True),
        (1, 0xff, False, True),
        (1, 0x55, True, True),
    ]
    WL_group, data0, ra_bit0_eq1_invert, inverted_sequence_W_R = parm[i]

    # WL_group = 1
    # data0 = 0x55
    # ra_bit0_eq1_invert = False
    # inverted_sequence_W_R = False
    continue_w_r = True

    ra_bit_count = 3            # 8 WLs
    ca_bit_count = 1            # 16 BLs
    item0 = ITEM('TISO', 7, 2)
    item1 = ITEM('SN', 7, 4)
    defect = DEFECT('SHORT', item0, item1, 0)


    p = PATTERN(ra_bit_count, ca_bit_count, defect)
    p.PRE()
    if inverted_sequence_W_R:
        for group_index in range(2**ra_bit_count//WL_group)[::-1]:
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('WR %d' %ra)
                for ca in range(2**ca_bit_count):
                    if ra % 2 == 1 and ra_bit0_eq1_invert:
                        data = NOTs(data0, 8)
                    else:
                        data = data0
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    else:
        for group_index in range(2**ra_bit_count//WL_group):
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('WR %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ra % 2 == 1 and ra_bit0_eq1_invert:
                        data = NOTs(data0, 8)
                    else:
                        data = data0
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    p.DONE()

def special_pattern():
    WL_group = 1
    data0 = 0x55
    ra_bit0_eq1_invert = False
    inverted_sequence_W_R = False
    continue_w_r = True

    ra_bit_count = 3            # 8 WLs
    ca_bit_count = 1            # 16 BLs
    item0 = ITEM('SN', 6, 4)
    item1 = ITEM('SN', 7, 3)
    defect = DEFECT('SHORT', item0, item1, 0)


    p = PATTERN(ra_bit_count, ca_bit_count, defect)
    p.PRE()
    if inverted_sequence_W_R:
        for group_index in range(2**ra_bit_count//WL_group)[::-1]:
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('WR %d' %ra)
                for ca in range(2**ca_bit_count):
                    if ra % 2 == 1 and ra_bit0_eq1_invert:
                        data = NOTs(data0, 8)
                    else:
                        data = data0
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    else:
        for group_index in range(2**ra_bit_count//WL_group):
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('WR %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ra % 2 == 1 and ra_bit0_eq1_invert:
                        data = NOTs(data0, 8)
                    else:
                        data = data0
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    p.DONE()

def random_pattern(i):
    parm = [
        (8, False),
        (1, False),
        (8, True),
        (1, True),
    ]
    WL_group, inverted_sequence_W_R = parm[i]

    continue_w_r = True

    ra_bit_count = 3            # 8 WLs
    ca_bit_count = 1            # 16 BLs
    item0 = ITEM('SN', 6, 4)
    item1 = ITEM('SN', 7, 3)
    defect = DEFECT('SHORT', item0, item1, 0)


    p = PATTERN(ra_bit_count, ca_bit_count, defect)
    p.PRE()
    if inverted_sequence_W_R:
        for group_index in range(2**ra_bit_count//WL_group)[::-1]:
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('WR %d' %ra)
                for ca in range(2**ca_bit_count):
                    data = random.randint(0, 255)
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group)[::-1]:
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    else:
        for group_index in range(2**ra_bit_count//WL_group):
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('WR %d' % ra)
                for ca in range(2**ca_bit_count):
                    data = random.randint(0, 255)
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.WR(ca, data)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
            for wl_index in range(WL_group):
                ra = group_index * WL_group + wl_index
                # print('RD %d' % ra)
                for ca in range(2**ca_bit_count):
                    if ca == 0 or not continue_w_r:
                        p.ACT(ra)
                    p.RD(ca)
                    if ca == 2**ca_bit_count-1 or not continue_w_r:
                        p.PRE()
    p.DONE()






if __name__ == '__main__':
    for i in range(12):
        shrmoo_pattern(i)
    # for i in range(4):
    #     random_pattern(i)