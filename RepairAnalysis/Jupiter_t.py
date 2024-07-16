import csv, os

headerMacro = ['MacroID', 'MacroX', 'MacroY', 'FBC', 'Repair']


def lgc2psc(lra:int):
    if type(lra) != int:
        raise(TypeError(f'lra = {lra} is not int type!'))
    if lra < 0:
        raise(ValueError(f'lra = {lra} out of limit!'))
    elif lra < 1312:
        return lra
    elif lra < 2048:
        return lra + 160
    elif lra < 2208:
        return lra - 736
    else:
        raise (ValueError(f'lra = {lra} out of limit!'))
def psc2lgc(pra:int):
    if type(pra) != int:
        raise(TypeError(f'pra = {pra} is not int type!'))
    if pra < 0:
        raise(ValueError(f'pra = {pra} out of limit!'))
    elif pra < 1312:
        return pra
    elif pra < 1472:
        return pra + 736
    elif pra < 2208:
        return pra - 160
    else:
        raise (ValueError(f'pra = {pra} out of limit!'))
def GetMacroCoordinate(macro_id:int)->list:
    id_bin_str = bin(macro_id).lstrip('0b').rjust(13, '0')
    x_bin_str = id_bin_str[4:8] + id_bin_str[11:]
    y_bin_str = id_bin_str[:4] + id_bin_str[8:11]
    return [int(x_bin_str, 2), int(y_bin_str, 2)]


class MAP:
    bytesCntPerWL = 12
    caCnt = 68
    wlCntPerSector = 736
    sectorCnt = 3
    raCnt = wlCntPerSector * sectorCnt
    raRedundant = 160
    caRedundant = 4
    firstRepairCaFailLimit = 160
    firstRepairRaFailLimit = 4
    def __init__(self):
        self.reserved = None
        self.result = -1    # -1:还未判定   0:没有fail   1:可修复   2:不可修复
        self.data = [[0 for i in range(MAP.caCnt)] for j in range(MAP.raCnt)]
        self.raRepair = [-1 for i in range(MAP.raRedundant)]
        self.caRepair = [[-1 for i in range(MAP.caRedundant)] for j in range(MAP.sectorCnt)]
    def __resultSet(self, value):
        resultList = [-1, 0, 1, 2]  # -1:还未判定   0:没有fail   1:可修复   2:不可修复
        if value not in resultList:
            raise(ValueError(f'{value} is not result value! pls check!'))
        self.__result = value
    result = property(lambda self:self.__result, __resultSet, lambda self:None)
    def Reset(self, data:bool=True, raRepair:bool=True, caRepair:bool=True, result:bool=True):
        if result:
            self.result = -1
        if data:
            for ra in range(MAP.raCnt):
                for ca in range(MAP.caCnt):
                    self.data[ra][ca] = 0
        if raRepair:
            for index in range(MAP.raRedundant):
                self.raRepair[index] = -1
        if caRepair:
            for sa in range(MAP.sectorCnt):
                for index in range(MAP.caRedundant):
                    self.caRepair[sa][index] = -1

    def __GetBLFBC(self, sector:int, ca:int):
        fbc = 0
        for ra in range(sector * MAP.wlCntPerSector, (sector + 1)*MAP.wlCntPerSector):
            if self.data[ra][ca]:
                fbc += 1
        return fbc
    def __GetWLFBC(self, pra:int):
        fbc = 0
        for ca in range(MAP.caCnt):
            if self.data[pra][ca]:
                fbc += 1
        return fbc
    def __GetMapFBC(self):
        fbc = 0
        for ra in range(MAP.raCnt):
            for ca in range(MAP.caCnt):
                if self.data[ra][ca]:
                    fbc += 1
        return fbc
    def GetFailCount(self):
        return self.__GetMapFBC()

    def __ClearWL(self, pra:int):
        for ca in range(MAP.caCnt):
            self.data[pra][ca] = 0
    def __ClearBL(self, sector:int, ca:int):
        for ra in range(sector * MAP.wlCntPerSector, (sector + 1)*MAP.wlCntPerSector):
            self.data[ra][ca] = 0

    def RecordFail(self, ra, ca, addNum=1, Physical=True):
        ra = ra if Physical else lgc2psc(ra)
        self.data[ra][ca] += addNum
    def ReadBinFile(self, fr, addNum=1):
        fbc = 0
        passTypeList = ['ExFileObject', 'BufferedReader'] # 'TextIOWrapper'
        frType = type(fr).__name__
        if frType == 'str':
            fr = open(fr, 'rb')
        elif frType in passTypeList:
            pass
        else:
            raise(TypeError(f'{type(fr).__name__} has not define!'))
        fr.seek(0, 0)
        for ra in range(MAP.raCnt):
            buffer = fr.read(MAP.bytesCntPerWL)
            for ibyte, byte in enumerate(buffer):
                for ibit in range(8):
                    if(byte & 1):
                        self.RecordFail(ra, 8*ibyte+ibit, addNum, False)
                        fbc += 1
                    byte = byte >> 1
                    if byte == 0:
                        break
        if frType == 'str':
            fr.close()
        return fbc

    def __RedundantSort(self):
        caRepair = [[self.caRepair[i][j] for j in range(MAP.caRedundant)] for i in range(MAP.sectorCnt)]
        raRepair = [self.raRepair[i] for i in range(MAP.raRedundant)]
        self.Reset(False, True, True, False)
        # CA Redundant Sort
        for sa in range(MAP.sectorCnt):
            for index in range(MAP.caRedundant):
                if caRepair[sa][index] >= (MAP.caCnt - MAP.caRedundant):
                    self.caRepair[sa][caRepair[sa][index] - MAP.caCnt + MAP.caRedundant] = caRepair[sa][index]
            cnt = 0
            for index in range(MAP.caRedundant):
                if 0 <= caRepair[sa][index] < (MAP.caCnt - MAP.caRedundant):
                    while self.caRepair[sa][cnt] != -1:
                        # self.caRepair[sa][cnt] = -1        # 需要看下是否能需要reset redundancy 的数据
                        cnt += 1
                    self.caRepair[sa][cnt] = caRepair[sa][index]
                    cnt += 1
        # RA Redundant Sort
        for index in range(MAP.raRedundant):
            if raRepair[index] >= (MAP.raCnt - MAP.raRedundant):
                self.raRepair[raRepair[index] - MAP.raCnt + MAP.raRedundant] = raRepair[index]
        cnt = 0
        for index in range(MAP.raRedundant):
            if 0 <= raRepair[index] < (MAP.raCnt - MAP.raRedundant):
                while self.raRepair[cnt] != -1:
                    # self.raRepair[cnt] = -1                  # 需要看下是否能需要reset redundancy 的数据
                    cnt += 1
                self.raRepair[cnt] = raRepair[index]
                cnt += 1
    def __RepairAnalysis(self):
        allPass = 0
        canRepair = 1
        dieFail = 2

        carc = [0 for i in range(MAP.sectorCnt)]
        rarc = 0

        # 统计剩余repair资源
        for sa in range(MAP.sectorCnt):
            for ica in range(MAP.caRedundant):
                if self.caRepair[sa][ica] != -1:
                    carc[sa] += 1
                    self.__ClearBL(sa, self.caRepair[sa][ica])
        for ira in range(MAP.raRedundant):
            if self.raRepair[ira] != -1:
                rarc += 1
                self.__ClearWL(lgc2psc(self.raRepair[ira]))
        self.reserved = self.GetFailCount()
        # 第一轮
        for sa in range(MAP.sectorCnt):
            for ca in range(MAP.caCnt):
                if self.__GetBLFBC(sa, ca) > MAP.firstRepairCaFailLimit:
                    if carc[sa] >= MAP.caRedundant:
                        self.result = dieFail
                        return
                    self.caRepair[sa][carc[sa]] = ca
                    carc[sa] += 1
        for pra in range(MAP.raCnt):
            if self.__GetWLFBC(pra) > MAP.firstRepairRaFailLimit:
                if rarc >= MAP.raRedundant:
                    self.result = dieFail
                    return
                self.raRepair[rarc] = psc2lgc(pra)
                rarc += 1
                self.__ClearWL(pra)
        for sa in range(MAP.sectorCnt):
            for ica in range(carc[sa]):
                self.__ClearBL(sa, self.caRepair[sa][ica])
        # 第二轮
        for sa in range(MAP.sectorCnt):
            for index in range(MAP.caRedundant - carc[sa]):
                temp_cnt = 0
                temp_ca = -1
                for ca in range(MAP.caCnt):
                    cnt = self.__GetBLFBC(sa, ca)
                    if cnt > temp_cnt:
                        temp_cnt = cnt
                        temp_ca = ca
                if temp_cnt == 0:
                    break
                self.caRepair[sa][carc[sa]] = temp_ca
                carc[sa] += 1
                self.__ClearBL(sa, temp_ca)
        for pra in range(MAP.raCnt):
            if self.__GetWLFBC(pra):
                if rarc >= MAP.raRedundant:
                    self.result = dieFail
                    return
                self.raRepair[rarc] = psc2lgc(pra)
                rarc += 1
                self.__ClearWL(pra)
        # 判断是否有fail
        if rarc + sum(carc) == 0:
            self.result = allPass
            return
        else:
            self.result = canRepair
            return
    def RepairAnalysis(self):
        temp = [[self.data[ra][ca] for ca in range(MAP.caCnt)] for ra in range(MAP.raCnt)]
        self.Reset(False, True, True, True)
        self.__RepairAnalysis()
        self.data = temp
        return self.result
    def ReRepairAnalysis(self):
        """
        以后 repair code 的情况下利用剩余的修复资源继续修复
        :return:
        """
        temp = [[self.data[ra][ca] for ca in range(MAP.caCnt)] for ra in range(MAP.raCnt)]
        self.Reset(False, False, False, True)
        self.__RepairAnalysis()
        self.data = temp
        return self.result

    @staticmethod
    def Bin2Csv(binFile, csvFile, physical=True, realData=False):
        macro = MAP()
        macro.ReadFile(binFile)
        macro.SaveMap2Csv(csvFile, physical=physical, realData=realData)
        del macro
    def SaveRepairCode(self, folder, uid:int):
        if type(uid) != int:
            raise(TypeError('uid type must be "int"!'))
        if uid < 0 or uid >= 6144:
            raise(ValueError('uid SEQ must in [0, 6144)!'))
        self.__RedundantSort()
        # 将code存在文件夹中
        fileName = 'macro' + str(uid) + 'rcode.asc'
        file = os.path.join(folder, fileName)
        with open(file, 'w', encoding='utf-8', newline='') as fw:
            fw.write(f'uid=7{str(hex(uid)).lstrip("0x").rjust(4, "0")}000\n')
            for ra in range(MAP.raRedundant):
                if self.raRepair[ra] < 0:
                    used = 0
                    repairable = 1
                    cor = 1
                    redy_addr = ra
                    fail_addr = 0
                elif self.raRepair[ra] < MAP.raCnt - MAP.raRedundant:
                    used = 1
                    repairable = 1
                    cor = 1
                    redy_addr = ra
                    fail_addr = self.raRepair[ra]
                elif self.raRepair[ra] < MAP.raCnt:
                    used = 1
                    repairable = 0
                    cor = 1
                    redy_addr = ra
                    fail_addr = 0
                rc = (used<<30) | (repairable << 29) | (cor << 27) | (redy_addr << 12) | fail_addr
                fw.write(f'b{ra}={str(hex(rc)).lstrip("0x".rjust(8, "0"))}\n')
            for sa in range(MAP.sectorCnt):
                for ca in range(MAP.caRedundant):
                    if self.caRepair[sa][ca] < 0:
                        used = 0
                        repairable = 1
                        cor = 0
                        redy_addr = sa * MAP.caRedundant + ca
                        fail_addr = 0
                    elif self.caRepair[sa][ca] < MAP.caCnt - MAP.caRedundant:
                        used = 1
                        repairable = 1
                        cor = 0
                        redy_addr = sa * MAP.caRedundant + ca
                        fail_addr = self.caRepair[sa][ca]
                    elif self.caRepair[sa][ca] < MAP.caCnt:
                        used = 1
                        repairable = 0
                        cor = 0
                        redy_addr = sa * MAP.caRedundant + ca
                        fail_addr = 0
                    rc = (used << 30) | (repairable << 29) | (cor << 27) | (redy_addr << 12) | fail_addr
                    fw.write(f'b{sa * MAP.caRedundant + ca + MAP.raRedundant}={str(hex(rc)).lstrip("0x".rjust(8, "0"))}\n')
    def SaveMap2Csv(self, csvFile, physical=True, realData=False):
        fw = open(csvFile, 'w', encoding='utf-8', newline='')
        writer = csv.writer(fw)
        if physical:
            if realData:
                for row in self.data:
                    writer.writerow(row)
            else:
                for row0 in self.data:
                    row = [int(bool(i)) for i in row0]
                    writer.writerow(row)
            # for pra in range(MAP.raCnt):
            #     ra = pra if physical else psc2lgc(pra)
            #     row = []
            #     for ca in range(MAP.caCnt):
            #         row.append(self.data[ra][ca] if realData else (1 if self.data[ra][ca] else 0))
            #     writer.writerow(row)
        else:
            if realData:
                for lra in range(MAP.raCnt):
                    row = self.data[lgc2psc(lra)]
                    writer.writerow(row)
            else:
                for lra in range(MAP.raCnt):
                    row = [int(bool(i)) for i in self.data[lgc2psc(lra)]]
                    writer.writerow(row)

        fw.close()

    def DataCompress(self, func, *args):
        for pra in range(MAP.raCnt):
            for ca in range(MAP.caCnt):
                self.data[pra][ca] = func(self.data[pra][ca], *args)

    def DebugClearBit(self, pra:int, ca:int):
        self.data[pra][ca] = 0
    def DebugClearWL(self, pra:int):
        self.__ClearWL(pra)
    def DebugClearBL(self, sector:int, ca:int):
        self.__ClearBL(sector, ca)
    def DebugRepairAnalysis(self, method):
        allPass = 0
        canRepair = 1
        dieFail = 2

        carc = [0 for i in range(MAP.sectorCnt)]
        rarc = 0

        #################################################################################
        tempList = []
        limit = 10
        #################################################################################

        self.Reset(False, True, True, True)
        # 第一轮
        for sa in range(MAP.sectorCnt):
            for ca in range(MAP.caCnt):
                if self.__GetBLFBC(sa, ca) > MAP.firstRepairCaFailLimit:
                    if carc[sa] >= MAP.caRedundant:
                        self.result = dieFail
                        return self.result
                    self.caRepair[sa][carc[sa]] = ca
                    carc[sa] += 1
        for pra in range(MAP.raCnt):
            #################################################################################
            if method == 1:
                if self.__GetWLFBC(pra) > limit:
                    tempList.append(pra ^ 1)
            elif method == 2:
                if self.__GetWLFBC(pra) > limit:
                    tempList.append(pra)
            #################################################################################
            if self.__GetWLFBC(pra) > MAP.firstRepairRaFailLimit:
                if rarc >= MAP.raRedundant:
                    self.result = dieFail
                    return self.result
                self.raRepair[rarc] = psc2lgc(pra)
                rarc += 1
                self.__ClearWL(pra)
        for sa in range(MAP.sectorCnt):
            for ica in range(carc[sa]):
                self.__ClearBL(sa, self.caRepair[sa][ica])
        # 第二轮
        for sa in range(MAP.sectorCnt):
            for index in range(MAP.caRedundant - carc[sa]):
                temp_cnt = 0
                temp_ca = -1
                for ca in range(MAP.caCnt):
                    cnt = self.__GetBLFBC(sa, ca)
                    if cnt > temp_cnt:
                        temp_cnt = cnt
                        temp_ca = ca
                if temp_cnt == 0:
                    break
                self.caRepair[sa][carc[sa]] = temp_ca
                carc[sa] += 1
                self.__ClearBL(sa, temp_ca)
        for pra in range(MAP.raCnt):
            if self.__GetWLFBC(pra):
                if rarc >= MAP.raRedundant:
                    self.result = dieFail
                    return self.result
                self.raRepair[rarc] = psc2lgc(pra)
                rarc += 1
                self.__ClearWL(pra)
        #################################################################################
        if method == 1:
            for pra in tempList:
                if psc2lgc(pra) not in self.raRepair:
                    if rarc >= 160:
                        break
                    self.raRepair[rarc] = psc2lgc(pra)
                    rarc += 1
        elif method == 2:
            spaceLimit = 3
            if len(tempList) >=2:
                raCurrent = tempList[0]
                for pra in tempList[1:]:
                    raSpace = pra - raCurrent - 1
                    if raSpace <= spaceLimit:
                        for i in range(1, raSpace+1):
                            if rarc >= 160:
                                break
                            if psc2lgc(raCurrent + i) not in self.raRepair:
                                self.raRepair[rarc] = psc2lgc(raCurrent + i)
                                rarc += 1
                    raCurrent = pra
        #################################################################################
        # 判断是否有fail
        if rarc + sum(carc) == 0:
            self.result = allPass
            return self.result
        else:
            self.result = canRepair
            return self.result



if __name__ == '__main__':
    pass