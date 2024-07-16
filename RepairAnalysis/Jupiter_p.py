import numpy as np
import concurrent.futures
import re, tarfile, os, csv


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


class MAP():
    def __init__(self):
        self.Reset(True, True)
    def Reset(self, data:bool=True, redundancy:bool=True):
        """
        将data 或 redundancy 初始话
        :param data: 是否做data做reset
        :param redundancy: 是否给redundancy做reset
        :return:
        """
        if data:
            self.data = np.zeros((2208, 68), int)
        if redundancy:
            self.raRepair = [-1 for ira in range(160)]
            self.caRepair = [[-1 for ica in range(4)] for isa in range(3)]
    @property
    def fbc(self):
        """
        :return:目前map 的 fbc
        """
        return np.sum(self.data)
    # def ReadBinFile(self, filePath:str):
    #     fr = open(filePath, 'rb')
    #     bitmap = np.unpackbits(np.frombuffer(fr.read(), dtype=np.uint8), bitorder="little").astype(np.uint8).reshape([2208, -1])[:, :68].astype(int)
    #     fr.close()
    #     bitmap = np.concatenate([bitmap[:736, :], np.concatenate([bitmap[736:1312, :], bitmap[2048:, :]]), bitmap[1312:2048, :]])
    #     self.data = self.data | bitmap
    #     return int(np.sum(bitmap))
    def ReadBinFile(self, fr):
        """
        读取bin格式文件，将bin文件数据与现有的map文件去并集
        :param fr: 以二进制打开的bin文件
        :return: 读入文件的fbc
        """
        bitmap = np.unpackbits(np.frombuffer(fr.read(), dtype=np.uint8), bitorder="little").astype(np.uint8).reshape([2208, -1])[:, :68].astype(int)
        bitmap = np.concatenate([bitmap[:736, :], np.concatenate([bitmap[736:1312, :], bitmap[2048:, :]]), bitmap[1312:2048, :]])
        self.data = self.data | bitmap
        return int(np.sum(bitmap))
    def RepairAnalysis(self):
        """
        做修复分析，返回是否可以修复的结果。分析完后，self.data为修复后的结果， self.raRepair 和 self.caRepair中存储需要修复的id
        :return: 是否可以修复的结果 True：可以修复；  False：不能修复
        """
        result = True
        carc = [0 for sa in range(3)]
        rarc = 0
        for sa in range(3):
            section = self.data[736 * sa : 736 * (sa + 1), :]
            caList = np.where(np.sum(section, axis=0) > 160)[0]
            if caList.size > 4:
                result = False
                caList = np.argsort(-np.sum(section, axis=0), kind='mergesort')[:4]
                carc[sa] = 4
                for ica in range(4):
                    self.caRepair[sa][ica] = int(caList[ica])
            else:
                carc[sa] = caList.size
                for ica in range(caList.size):
                    self.caRepair[sa][ica] = int(caList[ica])

        raList = np.where(np.sum(self.data, axis=1) > 4)[0]
        if raList.size > 160:
            result = False
            raList = np.argsort(-np.sum(self.data, axis=1), kind='mergesort')[:160]
            self.data[raList, :] = 0
            for pra in raList:
                self.raRepair[rarc] = psc2lgc(int(pra))
                rarc += 1
        else:
            self.data[raList, :] = 0
            for pra in raList:
                self.raRepair[rarc] = psc2lgc(int(pra))
                rarc += 1
        for sa in range(3):
            section = self.data[736 * sa : 736 * (sa + 1), :]
            for ca in self.caRepair[sa]:
                if ca != -1:
                    section[:, ca] = 0

        for sa in range(3):
            section = self.data[736 * sa : 736 * (sa + 1), :]
            fbcList = np.sum(section, axis=0)
            rem = np.where(fbcList > 0)[0].size
            rem = 4 - carc[sa] if ((4 - carc[sa]) < rem) else rem
            indexList = np.argsort(-fbcList, kind='mergesort')[:rem]
            section[:, indexList] = 0
            for ca in indexList:
                self.caRepair[sa][carc[sa]] = int(ca)
                carc[sa] += 1

        raList = np.where(np.sum(self.data, axis=1) > 0)[0]
        if rarc + raList.size > 160:
            raList = np.argsort(-np.sum(self.data, axis=1), kind='mergesort')[:160 - rarc]
            self.data[raList, :] = 0
            for pra in raList:
                self.raRepair[rarc] = psc2lgc(int(pra))
                rarc += 1
            result = False
        else:
            self.data[raList, :] = 0
            for pra in raList:
                self.raRepair[rarc] = psc2lgc(int(pra))
                rarc += 1
        return result
    def __SortRepairSource(self):
        caRepair = [[self.caRepair[i][j] for j in range(4)] for i in range(3)]
        raRepair = [self.raRepair[i] for i in range(160)]
        self.Reset(False, True)
        # CA Redundant Sort
        for sa in range(3):
            for index in range(4):
                if caRepair[sa][index] >= 64:
                    self.caRepair[sa][caRepair[sa][index] - 64] = caRepair[sa][index]
            cnt = 0
            for index in range(4):
                if 0 <= caRepair[sa][index] < 64:
                    while self.caRepair[sa][cnt] != -1:
                        cnt += 1
                    self.caRepair[sa][cnt] = caRepair[sa][index]
                    cnt += 1
        # RA Redundant Sort
        for index in range(160):
            if raRepair[index] >= 2048:
                self.raRepair[raRepair[index] - 2048] = raRepair[index]
        cnt = 0
        for index in range(160):
            if 0 <= raRepair[index] < 2048:
                while self.raRepair[cnt] != -1:
                    cnt += 1
                self.raRepair[cnt] = raRepair[index]
                cnt += 1
    def SaveAscFile(self, filePath:str, uid:int):
        """
        将存储在self.raRepair 和 self.caRepair 中的修复信息转换成文件
        :param filePath: 存储信息文本地址
        :param uid: macro id
        :return: None
        """
        self.__SortRepairSource()
        with open(filePath, 'w', encoding='utf-8', newline='') as fw:
            fw.write(f'uid=7{str(hex(uid)).lstrip("0x").rjust(4, "0")}000\n')
            for ra in range(160):
                if self.raRepair[ra] < 0:
                    used = 0
                    repairable = 1
                    cor = 1
                    redy_addr = ra
                    fail_addr = 0
                elif self.raRepair[ra] < 2048:
                    used = 1
                    repairable = 1
                    cor = 1
                    redy_addr = ra
                    fail_addr = self.raRepair[ra]
                elif self.raRepair[ra] < 2208:
                    used = 1
                    repairable = 0
                    cor = 1
                    redy_addr = ra
                    fail_addr = 0
                rc = (used << 30) | (repairable << 29) | (cor << 27) | (redy_addr << 12) | fail_addr
                fw.write(f'b{ra}={str(hex(rc)).lstrip("0x".rjust(8, "0"))}\n')
            for sa in range(3):
                for ca in range(4):
                    if self.caRepair[sa][ca] < 0:
                        used = 0
                        repairable = 1
                        cor = 0
                        redy_addr = 4 * sa + ca
                        fail_addr = 0
                    elif self.caRepair[sa][ca] < 64:
                        used = 1
                        repairable = 1
                        cor = 0
                        redy_addr = 4 * sa + ca
                        fail_addr = self.caRepair[sa][ca]
                    elif self.caRepair[sa][ca] < 68:
                        used = 1
                        repairable = 0
                        cor = 0
                        redy_addr = 4 * sa + ca
                        fail_addr = 0
                    rc = (used << 30) | (repairable << 29) | (cor << 27) | (redy_addr << 12) | fail_addr
                    fw.write(f'b{4 * sa + ca + 160}={str(hex(rc)).lstrip("0x".rjust(8, "0"))}\n')


def DecodeOneDieTarGz(dieFilePath, outputFolderPath):
    """
    将一颗die的6144个bin格式文件的tar.gz格式压缩包dieFilePath 解析成为6144个repair code文件，并存储到outputFolderPath文件夹中
    :param dieFilePath: 一颗die的6144个bin格式文件的tar.gz格式压缩包
    :param outputFolderPath: 用于存储解析后的repair code的文件夹地址
    :return: None
    """
    macro = MAP()
    fw = open(os.path.join(outputFolderPath, 'repair_result.csv'), 'w', encoding='utf-8', newline='')
    writer = csv.writer(fw)
    with tarfile.open(dieFilePath, 'r:*') as fr:
        for member in fr.getmembers():
            uid = int(re.match('uid_(\w+)_msb_0\.bin', member.name).group(1), 16)
            ascFilePath = os.path.join(outputFolderPath, f'macro{uid}rcode.asc')
            macro.Reset()
            fbc = macro.ReadBinFile(fr.extractfile(member))
            result = macro.RepairAnalysis()
            rFBC = macro.fbc
            macro.SaveAscFile(ascFilePath, uid)
            writer.writerow([uid, fbc, int(result), rFBC])
    fw.close()


def DecodeOneDieFolder(dieFolderPath, outputFolderPath):
    """
    将dieFolderPath中的bin文件解析为repair code文件，并存放在outputFolderPath文件夹中
    :param dieFolderPath: 用于存放一颗die的6144个bin格式文件的文件夹地址
    :param outputFolderPath: 用于存放解析后repair code文件 和 sum文件 的文件夹地址
    :return: None
    """
    def BinFileOperation(binFileName):
        binFilePath = os.path.join(dieFolderPath, binFileName)
        uid = int(re.match('uid_(\w+)_msb_0\.bin', binFileName).group(1), 16)
        ascFilePath = os.path.join(outputFolderPath, f'macro{uid}rcode.asc')
        macro = MAP()
        with open(binFilePath, 'rb') as fr:
            macro.ReadBinFile(fr)
        macro.RepairAnalysis()
        macro.SaveAscFile(ascFilePath, uid)
    binFileNameList = os.listdir(dieFolderPath)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(BinFileOperation, binFileNameList)


def DecodeOneWaferFolder(waferfolderPath, outputFolderPath):
    """
    waferfolderPath中的tar.gz格式的die文件 解析为repair code文件，并存放在outputFolderPath文件夹中
    :param waferfolderPath: 用于存放多个die数据tar.gz格式压缩包的文件夹地址
    :param outputFolderPath: 用于存放解析后repair code文件 和 sum文件 的文件夹地址
    :return:
    """
    def DieFileOperation(dieFileName):
        tarGzFilePath = os.path.join(waferfolderPath, dieFileName)
        subOutputFolderPath = os.path.join(outputFolderPath, dieFileName[:-7])
        if not os.path.isdir(subOutputFolderPath):
            os.makedirs(subOutputFolderPath)
        DecodeOneDieTarGz(tarGzFilePath, subOutputFolderPath)
    dieFileNameList = os.listdir(waferfolderPath)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(DieFileOperation, dieFileNameList)


# def ClearFolder(path):
#     if os.path.isfile(path):
#         os.remove(path)
#     elif os.path.isdir(path):
#         for name in os.listdir(path):
#             ClearFolder(os.path.join(path, name))
#         os.rmdir(path)
#     else:
#         raise (TypeError(f'has not define "{path}" type!'))
# def MultiClearFolder(path):
#     def DeleteFolder(name):
#         ClearFolder(os.path.join(path, name))
#     nameList = os.listdir(path)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(DeleteFolder, nameList)

# if __name__ == '__main__':
#     import time
#
#     dieFile = r'G:\Test\temp\errorMap_waferPPP439-10X7Y7.tar.gz'
#     dieFolder = r'G:\Test\temp\binFolder'
#     waferFolder = r'G:\FullWafer\wafer_09_20240524_200M_trim_8'
#     outputFolder = r'G:\Test\temp\ascFolder'
#     if not os.path.isdir(outputFolder):
#         os.mkdir(outputFolder)
#
#     t0 = time.time()
#     DecodeOneWaferFolder(waferFolder, outputFolder)
#     t1 = time.time()
#     print(f'Decode has used: {t1 - t0:.1f}s')
#
#     t0 = time.time()
#     MultiClearFolder(outputFolder)
#     t1 = time.time()
#     print(f'Clear has used: {t1 - t0:.1f}s')