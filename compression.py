import tarfile, os
from pylib import progress



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

def LoopFileInTarGz(fileTarGz, type='name'):
    typeSet = ('name', 'member', 'buffer')
    if type not in typeSet:
        raise(ValueError(f'the type of "{type}" has not define'))
    with tarfile.open(fileTarGz, 'r:*') as fr:
        for member in fr.getmembers():
            if type == 'name':
                yield member.name
            elif type == 'member':
                yield member
            elif type == 'buffer':
                yield fr.extractfile(member)

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

def CompressFolder(folderPath):
    def LoopFile(folderPath):
        for file in os.listdir(folderPath):
            path = os.path.join(folderPath, file)
            if os.path.isdir(path):
                for file in LoopFile(path):
                    yield file
            elif os.path.isfile(path):
                yield path
            else:
                raise(ValueError('has not define!'))
    if not os.path.isdir(folderPath):
        raise(ValueError(f'{folderPath} is not folder path!'))
    with tarfile.open(f'{folderPath}.tar.gz', 'w:gz') as fw:
        os.chdir(folderPath)
        for file in LoopFile('.'):
            if os.path.basename(file) == r'Thumbs.db':
                continue
            print('正在压缩：'+file[2:])
            fw.add(file[2:])

if __name__ == '__main__':
    CompressFolder(r'G:\Temp\vblpLoop')

