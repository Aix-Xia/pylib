import tarfile
import os


# can decompress "tar" or "tar.gz" type file
def DecompressTarGz(fileTar, pathOutput="."):
    with tarfile.open(fileTar, 'r') as fr:
        fr.extractall(path=pathOutput)

def Compress2TarGz(file, fileTarGz, mode='a'):
    fileName = os.path.basename(file)
    if mode not in ('a', 'w'):
        raise(ValueError(f'mode:{mode} has not define!'))
    with tarfile.open(fileTarGz, mode=mode) as fw:
        fw.add(file, arcname=fileName)

def GetFileCountInTarGz(fileTarGz):
    with tarfile.open(fileTarGz, 'r:*') as fr:
        return len(fr.getmembers())

def LoopTarGzFile(fileTarGz, type='name'):
    typeSet = ('name', 'member')
    if type not in typeSet:
        raise(ValueError(f'the type of "{type}" has not define'))
    with tarfile.open(fileTarGz, 'r:*') as fr:
        for member in fr.getmembers():
            if type == 'name':
                yield member.name
            elif type == 'member':
                yield member

def ExtractFileFromTarGz(fileTarGz, fileTarget, folderOutput):
    with tarfile.open(fileTarGz, 'r:*') as fr:
        if type(fileTarget) == str:
            for member in fr.getmembers():
                if member.name == fileTarget:
                    fr.extract(member, folderOutput)
                    break
            else:
                print(f'File {fileTarget} not found in the archive.')
        elif type(fileTarget) == tarfile.TarInfo:
            try:
                fr.extract(fileTarget, folderOutput)
            except Exception:
                print(f'File {fileTarget.name} not found in the archive.')
        else:
            raise(TypeError(f'can not use "{type(fileTarget)}" type parameter'))



if __name__ == '__main__':
    import re
    import progress
    import file

    folderIn = r'G:\bitmap'
    folderOut = r'G:\Resource'

    for wafer_id in os.listdir(folderIn):
        if wafer_id == 'w10':
            continue
        waferIn = os.path.join(folderIn, wafer_id)
        waferOut = os.path.join(folderOut, wafer_id.upper())
        if not os.path.isdir(waferOut):
            os.mkdir(waferOut)
        fileCnt = file.GetFileCount(waferIn)
        print(f'正在处理： {wafer_id}:')
        for index, fileGzName in enumerate(os.listdir(waferIn), 1):
            progress.PrintProgress(index, fileCnt, fileGzName)
            fileGz = os.path.join(waferIn, fileGzName)
            for file in LoopTarGzFile(fileGz, 'member'):
                obj = re.match('.*errorMap_[Xx]\d+[Yy]\d+', file.name)
                if obj == None:
                    continue
                ExtractFileFromTarGz(fileGz, file, waferOut)
