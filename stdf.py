
def ReadBytes2Int(fr, _len:int):
    return int.from_bytes(fr.read(_len), 'little')

class REC:
    dataType = {
        # STDF 文件的相关信息
        (0, 10): 'File Attributes Record (FAR)',
        (0, 20): 'Audit Trail Record (ATR)',
        # 以lot为基础的数据
        (1, 10): 'Master Information Record (MIR)',
        (1, 20): 'Master Results Record (MRR)',
        (1, 30): 'Part Count Record (PCR)',
        (1, 40): 'Hardware Bin Record (HBR)',
        (1, 50): 'Software Bin Record (SBR)',
        (1, 60): 'Pin Map Record (PMR)',
        (1, 62): 'Pin Group Record (PGR)',
        (1, 63): 'Pin List Record (PLR)',
        (1, 70): 'Retest Data Record (RDR)',
        (1, 80): 'Site Description Record (SDR)',
        # 以wafer为基础的数据
        (2, 10): 'Wafer Information Record (WIR)',
        (2, 20): 'Wafer Results Record (WCR)',
        (2, 30): 'Wafer Configuration Record (WCR)',
        # 以Die为基础的数据
        (5, 10): 'Part Information Record (PIR)',
        (5, 20): 'Part Results Record (PRR)',
        # 以测试程序中每个测试项为基础的数据
        (10, 30): 'Test Synopsis Record (TSR)',
        # 测试程序中每个测试项的执行情况
        (15, 10): 'Parametric Test Record (PTR)',
        (15, 15): 'Multiple-Result Parametric Record (MPR)',
        (15, 20): 'Functional Test Record (FTR)',
        # 通用数据
        (50, 10): 'Generic Data Record (GDR)',
        (50, 30): 'Datalog Text Record (DTR)',
        # 预留分组
        180: 'has not define',
        181: 'has not define'
    }
    def __init__(self, _len:int, _typ:int, _sub:int):
        self.len = _len
        self.typ = _typ
        self.sub = _sub
    def __str__(self):
        return f'({self.len}, {self.typ}, {self.sub}): {REC.dataType[(self.typ, self.sub)]}'
    def __lenSet(self, value):
        self.__len = value
    def __typSet(self, value):
        self.__typ = value
    def __subSet(self, value):
        self.__sub = value
    len = property(lambda self:self.__len, __lenSet, lambda self:None, 'this is len')
    typ = property(lambda self:self.__typ, __typSet, lambda self:None, 'this is typ')
    sub = property(lambda self:self.__sub, __subSet, lambda self:None, 'this is sub')
    @staticmethod
    def GetRecFromFile(fr):
        _len = ReadBytes2Int(fr, 2)
        _typ = ReadBytes2Int(fr, 1)
        _sub = ReadBytes2Int(fr, 1)
        return REC(_len, _typ, _sub)

path = r'G:\Project\Jupyter\CP_Data\PPQ740\W10\20240724\stdflog\V1.0_PPQ740_PPQ740-10_CACP2024-05803_CP1_20240724_140154.stdf'

with open(path, 'rb') as fr:
    for i in range(6):
        print(ReadBytes2Int(fr, 1))
    for i in range(20):
        rec = REC.GetRecFromFile(fr)
        if rec.len == 0:
            break
        print(rec)
        fr.read(rec.len)