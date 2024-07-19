import numpy


"""
array_x count : 8.5
array_y count : 23 (top and bottom array assemble to one array)
bit line count per array : 1088
word line count per array : 768
word line count per segment : 1536
bytes count per column address : 17 (16 for user, 1 for ecc)
normal column address count : 64
redundancy column address count : 4
total column address count : 68
normal row address count : 16384(16K)
redundancy row address count : 512 (256 for half bank)
total row address count : 16896
total segment count : 11 (2 row array assemble to one segment)
row redundancy location : X10 bottom for top half bank; X21 bottom for bottom half bank;
"""

class MAP():
    def __init__(self):
        self.Reset()
    @property
    def fbc(self):
        return numpy.sum(self.data)
    def Reset(self, data:bool=True, redy:bool=True):
        if data:
            self.data = numpy.zeros((16896, 68), int)
        if redy:
            self.raRepair = [[-1 for ira in range(256)] for isa in range(2)]
            self.caRepair = [[-1 for ica in range(4)] for isa in range(11)]
    def ReadBinFile(self, fr):
        bitmap = numpy.unpackbits(numpy.frombuffer(fr.read(), dtype=numpy.uint8), bitorder="little").astype(numpy.uint8).reshape([16896, -1])[:, :68].astype(int)
        bitmap = numpy.concatenate([bitmap[:8192, :], bitmap[16384:16640, :], bitmap[8192:16384, :], bitmap[16640:, :]])
        self.data = self.data | bitmap
        return int(numpy.sum(bitmap))
    def RepairAnalysis(self):
        pass
    def __SortRepairSource(self):
        pass
    def SaveAscFile(self, filePath:str, uid:int):
        pass