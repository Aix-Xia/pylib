import numpy as np
import re

def GetMacroCoordinate(macro_id:int)->list:
    """
    :param macro_id: uid
    :return: [macroX, macroY]
    """
    id_bin_str = bin(macro_id).lstrip('0b').rjust(13, '0')
    x_bin_str = id_bin_str[4:8] + id_bin_str[11:]
    y_bin_str = id_bin_str[:4] + id_bin_str[8:11]
    return [int(x_bin_str, 2), int(y_bin_str, 2)]
def GetMacroInfo(macroFileName:str)->list:
    """
    :param macroFileName: macro file name
    :return: [uid, macroX, macroY]
    """
    obj = re.match('uid_(\w+)_msb_0\.bin', macroFileName)
    if obj:
        uid = int(obj.group(1), 16)
        coor = GetMacroCoordinate(uid)
        return [uid, coor[0], coor[1]]
    else:
        return [None, None, None]

class MAP():
    __totRaCnt = 1472
    __totCaCnt = 68
    __redRaCnt = 45
    __redCaCnt = 4
    def __init__(self):
        self.Reset()
    @property
    def fbc(self):
        return int(np.sum(self.data))
    def Reset(self, data:bool=True, redundancy:bool=True):
        if data:
            self.data = np.zeros((MAP.__totRaCnt, MAP.__totCaCnt), int)
        if redundancy:
            self.raRepair = [-1 for i in range(MAP.__redRaCnt)]
            self.caRepair = [-1 for i in range(MAP.__redCaCnt)]
    def ReadBinFile(self, fr):
        bitmap = np.unpackbits(np.frombuffer(fr.read(), dtype=np.uint8), bitorder="little").astype(np.uint8).reshape([2208, -1])[:, :68].astype(int)
        bitmap = np.concatenate([bitmap[:1312, :], bitmap[2048:, :]])
        self.data = self.data | bitmap
        return int(np.sum(bitmap))
    def RepairAnalysis(self):
        result = True
        carc = 0
        rarc = 0

        # 1.1
        caList = np.where(np.sum(self.data, axis=0) > MAP.__redRaCnt)[0]
        if caList.size > MAP.__redCaCnt:
            result = False
            caList = np.argsort(-np.sum(self.data, axis=0), kind='mergesort')[:MAP.__redCaCnt]
            carc = MAP.__redCaCnt
        else:
            carc = caList.size
        for ica in range(carc):
            self.caRepair[ica] = int(caList[ica])

        # 1.2
        raList = np.where(np.sum(self.data, axis=1) > MAP.__redCaCnt)[0]
        if raList.size > MAP.__redRaCnt:
            result = False
            raList = np.argsort(-np.sum(self.data, axis=1), kind='mergesort')[:MAP.__redRaCnt]
            rarc = MAP.__redRaCnt
        else:
            rarc = raList.size
        self.data[raList, :] = 0
        for ira in range(rarc):
            self.raRepair[ira] = int(raList[ira])

        # 1.3
        self.data[:, caList] = 0

        # 2.1
        fbcList = np.sum(self.data, axis=0)
        rem = np.where(fbcList > 0)[0].size
        rem = MAP.__redCaCnt - carc if ((MAP.__redCaCnt - carc) < rem) else rem
        indexList = np.argsort(-fbcList, kind='mergesort')[:rem]
        self.data[:, indexList] = 0
        for ca in indexList:
            self.caRepair[carc] = int(ca)
            carc += 1

        # 2.2
        raList = np.where(np.sum(self.data, axis=1) > 0)[0]
        if rarc + raList.size > MAP.__redRaCnt:
            result = False
            raList = np.argsort(-np.sum(self.data, axis=1), kind='mergesort')[:MAP.__redRaCnt - rarc]
        self.data[raList, :] = 0
        for pra in raList:
            self.raRepair[rarc] = int(pra)
            rarc += 1
        return result
    def GetRedRACntNeed(self):
        carc = 0
        rarc = 0

        # 1.1
        caList = np.where(np.sum(self.data, axis=0) > MAP.__redRaCnt)[0]
        if caList.size > MAP.__redCaCnt:
            caList = np.argsort(-np.sum(self.data, axis=0), kind='mergesort')[:MAP.__redCaCnt]
            carc = MAP.__redCaCnt
        else:
            carc = caList.size

        # 1.2
        raList = np.where(np.sum(self.data, axis=1) > MAP.__redCaCnt)[0]
        if raList.size > MAP.__redRaCnt:
            raList = np.argsort(-np.sum(self.data, axis=1), kind='mergesort')[:MAP.__redRaCnt]
            rarc = MAP.__redRaCnt
        else:
            rarc = raList.size
        self.data[raList, :] = 0

        # 1.3
        self.data[:, caList] = 0

        # 2.1
        fbcList = np.sum(self.data, axis=0)
        rem = np.where(fbcList > 0)[0].size
        rem = MAP.__redCaCnt - carc if ((MAP.__redCaCnt - carc) < rem) else rem
        indexList = np.argsort(-fbcList, kind='mergesort')[:rem]
        self.data[:, indexList] = 0

        # 2.2
        raList = np.where(np.sum(self.data, axis=1) > 0)[0]
        rarc += raList.size

        return rarc
    @classmethod
    def SetRedundancy(cls, ra:int, ca:int):
        cls.__redCaCnt = ca
        cls.__redRaCnt = ra