
def i2b(data:int, length:int)->bytes:
    return data.to_bytes(length, 'little')
def b2i(data:bytes)->int:
    return int.from_bytes(data, 'little')


class BITMAPFILEHEADER:
    _bfType_list = (0x4d42,)
    def __init__(self, bfSize, bfOffBits):
        # bfType, 2 Bytes, 位图文件的类型，必须为BM
        self.bfType = 0x4d42
        """
            bfSize：
                位图文件头的大小（14 Bytes）
                位图信息头的大小（40 Bytes）
                颜色表项 * 4 Bytes
                图像的宽度 * 高度 * 深度 / 8 （字节）
        """
        # bfSize, 4 Bytes, 位图文件的大小，以字节为单位
        self.bfSize = bfSize
        # bfReserved1, 2 Bytes, 位图文件保留字, 必须为 0
        self.bfReserved1 = 0
        # bfReserved2, 2 Bytes, 位图文件保留字, 必须为 0
        self.bfReserved2 = 0
        # bfOffBits, 4 Bytes, 位图数据的起始位置，以字节为单位
        self.bfOffBits = bfOffBits
    def __str__(self):
        result = ''
        result += f'bfType           :  {self.bfType}\n'
        result += f'bfSize           :  {self.bfSize}\n'
        result += f'bfReserved1      :  {self.bfReserved1}\n'
        result += f'bfReserved2      :  {self.bfReserved2}\n'
        result += f'bfOffBits        :  {self.bfOffBits}\n'
        return result

    def _bfType_get(self):
        return b2i(self._bfType)
    def _bfType_set(self, bfType):
        if type(bfType) == bytes:
            bfType = b2i(bfType)
        elif type(bfType) != int:
            raise (TypeError('bfType type error!'))
        if bfType not in BITMAPFILEHEADER._bfType_list:
            raise(ValueError(f'bfType must in {BITMAPFILEHEADER._bfType_list}'))
        self._bfType = i2b(bfType, 2)
    def _bfType_del(self):
        print(f'bfType = {self._bfType} has delete!')
    bfType = property(_bfType_get, _bfType_set, _bfType_del, 'This is bfType')

    def _bfSize_get(self):
        return b2i(self._bfSize)
    def _bfSize_set(self, bfSize):
        if type(bfSize) == bytes:
            bfSize = b2i(bfSize)
        elif type(bfSize) != int:
            raise (TypeError('bfSize type error!'))
        self._bfSize = i2b(bfSize, 4)
    def _bfSize_del(self):
        print(f'bfSize = {self._bfSize} has delete!')
    bfSize = property(_bfSize_get, _bfSize_set, _bfSize_del, 'This is bfSize')

    def _bfReserved1_get(self):
        return b2i(self._bfReserved1)
    def _bfReserved1_set(self, bfReserved1):
        if type(bfReserved1) == bytes:
            bfReserved1 = b2i(bfReserved1)
        elif type(bfReserved1) != int:
            raise(TypeError('bfReserved1 type error!'))
        self._bfReserved1 = i2b(bfReserved1, 2)
    def _bfReserved1_del(self):
        print(f'bfReserved1 = {self._bfReserved1} has delete!')
    bfReserved1 = property(_bfReserved1_get, _bfReserved1_set, _bfReserved1_del, 'This is bfReserved1')

    def _bfReserved2_get(self):
        return b2i(self._bfReserved2)
    def _bfReserved2_set(self, bfReserved2):
        if type(bfReserved2) == bytes:
            bfReserved2 = b2i(bfReserved2)
        elif type(bfReserved2) != int:
            raise (TypeError('bfReserved2 type error!'))
        self._bfReserved2 = i2b(bfReserved2, 2)
    def _bfReserved2_del(self):
        print(f'bfReserved2 = {self._bfReserved2} has delete!')
    bfReserved2 = property(_bfReserved2_get, _bfReserved2_set, _bfReserved2_del, 'This is bfReserved2')

    def _bfOffBits_get(self):
        return b2i(self._bfOffBits)
    def _bfOffBits_set(self, bfOffBits):
        if type(bfOffBits) == bytes:
            bfOffBits = b2i(bfOffBits)
        elif type(bfOffBits) != int:
            raise (TypeError('bfOffBits type error!'))
        self._bfOffBits = i2b(bfOffBits, 4)
    def _bfOffBits_del(self):
        print(f'bfOffBits = {self._bfOffBits} has delete!')
    bfOffBits = property(_bfOffBits_get, _bfOffBits_set, _bfOffBits_del, 'This is bfOffBits')

    @staticmethod
    def CreatFileHeader(fr):
        bfType = b2i(fr.read(2))
        bfSize = b2i(fr.read(4))
        bfReserved1 = b2i(fr.read(2))
        bfReserved2 = b2i(fr.read(2))
        bfOffBits = b2i(fr.read(4))
        fileHeader = BITMAPFILEHEADER(bfSize, bfOffBits)
        fileHeader.bfType = bfType
        fileHeader.bfReserved1 = bfReserved1
        fileHeader.bfReserved2 = bfReserved2
        return fileHeader
    def ReadFile(self, fr):
        self.bfType = b2i(fr.read(2))
        self.bfSize = b2i(fr.read(4))
        self.bfReserved1 = b2i(fr.read(2))
        self.bfReserved2 = b2i(fr.read(2))
        self.bfOffBits = b2i(fr.read(4))
    def Write2File(self, fw):
        fw.write(self._bfType)
        fw.write(self._bfSize)
        fw.write(self._bfReserved1)
        fw.write(self._bfReserved2)
        fw.write(self._bfOffBits)


class BITMAPINFOHEADER:
    _biSize_list = (40,)
    _biPlanes_list = (1,)
    _biBitCount_list = (1, 4, 8, 24, 32)
    _biCompression_list = (0, 1, 2)
    _biClrUsed_list = (0,)
    _biClrImportant_list = (0,)
    def __init__(self, biWidth, biHeight, biBitCount, biPelsPerMeter=0xec4):
        # biSize, 4 Bytes, 本结构所占Bytes数, 一般为40
        self.biSize = 0x28
        # biWidth， 4 Bytes, 位图的宽度，以像素为单位
        self.biWidth = biWidth
        # biHeight, 4 Bytes, 位图的高度，以像素为单位. 如果该值为正数，说明图像是倒向的; 如果该值是一个负数, 说明图像是正向的. 如果该值是负值, 图片不能被压缩
        self.biHeight = biHeight
        # biPlanes, 2 Bytes, 目标设备的级别, 总为1
        self.biPlanes = 0x1
        # biBitCount, 2 Bytes,每个像素需要的bit数. 1（双色）、4（16色）、8（256色）、24（真色彩）、32（增强真色彩）
        self.biBitCount = biBitCount
        # biCompression， 4 Bytes, 位图压缩类型. 0（不压缩）、1（BI_RLE8压缩类型）、2（BI_RLE4压缩类型）
        self.biCompression = 0
        # biSizeImage, 4 BYtes, 位图大小，以byte为单位. 如果biCompression==0时, 可设置为0
        self.biSizeImage = (biWidth * biBitCount + 31) // 32 * 4 * biHeight
        # biXPelsPerMeter, 4 BYtes, 位图水平分辨率, 每米像素数
        self.biXPelsPerMeter = biPelsPerMeter
        # biYPelsPerMeter, 4 BYtes, 位图垂直分辨率, 每米像素数
        self.biYPelsPerMeter = biPelsPerMeter
        # biClrUsed, 4 Bytes, 位图实际使用的颜色表中的颜色数. 设置为0的话，则说明使用所有调色版项
        self.biClrUsed = 0x0
        # biClrImportant, 4 Bytes, 位图显示过程中重要的颜色数.  设置为0的话，则说明都重要
        self.biClrImportant = 0x0
    def __str__(self):
        result = ''
        result += f'biSize           :  {self.biSize}\n'
        result += f'biWidth          :  {self.biWidth}\n'
        result += f'biHeight         :  {self.biHeight}\n'
        result += f'biPlanes         :  {self.biPlanes}\n'
        result += f'biBitCount       :  {self.biBitCount}\n'
        result += f'biCompression    :  {self.biCompression}\n'
        result += f'biSizeImage      :  {self.biSizeImage}\n'
        result += f'biXPelsPerMeter  :  {self.biXPelsPerMeter}\n'
        result += f'biYPelsPerMeter  :  {self.biYPelsPerMeter}\n'
        result += f'bfClrUsed        :  {self.biClrUsed}\n'
        result += f'bfClrImportant   :  {self.biClrImportant}\n'
        return result

    def _biSize_get(self):
        return b2i(self._biSize)
    def _biSize_set(self, biSize):
        if type(biSize) == bytes:
            biSize = b2i(biSize)
        elif type(biSize) != int:
            raise (TypeError('biSize type error!'))
        if biSize not in BITMAPINFOHEADER._biSize_list:
            raise(ValueError(f'biSize must be in {BITMAPINFOHEADER._biSize_list}'))
        self._biSize = i2b(biSize, 4)
    def _biSize_del(self):
        print(f'biSize = {self._biSize} has delete!')
    biSize = property(_biSize_get, _biSize_set, _biSize_del, 'This is biSize')

    def _biWidth_get(self):
        return b2i(self._biWidth)
    def _biWidth_set(self, biWidth):
        if type(biWidth) == bytes:
            biWidth = b2i(biWidth)
        elif type(biWidth) != int:
            raise (TypeError('biWidth type error!'))
        self._biWidth = i2b(biWidth, 4)
    def _biWidth_del(self):
        print(f'biWidth = {self._biWidth} has delete!')
    biWidth = property(_biWidth_get, _biWidth_set, _biWidth_del, 'This is biWidth')

    def _biHeight_get(self):
        return b2i(self._biHeight)
    def _biHeight_set(self, biHeight):
        if type(biHeight) == bytes:
            biHeight = b2i(biHeight)
        elif type(biHeight) != int:
            raise (TypeError('biHeight type error!'))
        self._biHeight = i2b(biHeight, 4)
    def _biHeight_del(self):
        print(f'biHeight = {self._biHeight} has delete!')
    biHeight = property(_biHeight_get, _biHeight_set, _biHeight_del, 'This is biHeight')

    def _biPlanes_get(self):
        return b2i(self._biPlanes)
    def _biPlanes_set(self, biPlanes):
        if type(biPlanes) == bytes:
            biPlanes = b2i(biPlanes)
        elif type(biPlanes) != int:
            raise (TypeError('biPlanes type error!'))
        if biPlanes not in BITMAPINFOHEADER._biPlanes_list:
            raise(ValueError(f'biPlanes must be in {BITMAPINFOHEADER._biPlanes_list}'))
        self._biPlanes = i2b(biPlanes, 2)
    def _biPlanes_del(self):
        print(f'biPlanes = {self._biPlanes} has delete!')
    biPlanes = property(_biPlanes_get, _biPlanes_set, _biPlanes_del, 'This is biPlanes')

    def _biBitCount_get(self):
        return b2i(self._biBitCount)
    def _biBitCount_set(self, biBitCount):
        if type(biBitCount) == bytes:
            biBitCount = b2i(biBitCount)
        elif type(biBitCount) != int:
            raise (TypeError('biBitCount type error!'))
        if biBitCount not in BITMAPINFOHEADER._biBitCount_list:
            raise(ValueError(f'biBitCount must in {BITMAPINFOHEADER._biBitCount_list}'))
        self._biBitCount = i2b(biBitCount, 2)
    def _biBitCount_del(self):
        print(f'biBitCount = {self._biBitCount} has delete!')
    biBitCount = property(_biBitCount_get, _biBitCount_set, _biBitCount_del, 'This is biBitCount')

    def _biCompression_get(self):
        return b2i(self._biCompression)
    def _biCompression_set(self, biCompression):
        if type(biCompression) == bytes:
            biCompression = b2i(biCompression)
        elif type(biCompression) != int:
            raise (TypeError('biCompression type error!'))
        if biCompression not in BITMAPINFOHEADER._biCompression_list:
            raise(ValueError(f'biCompression numst in {BITMAPINFOHEADER._biCompression_list}'))
        self._biCompression = i2b(biCompression, 4)
    def _biCompression_del(self):
        print(f'biCompression = {self._biCompression} has delete!')
    biCompression = property(_biCompression_get, _biCompression_set, _biCompression_del, 'This is biCompression')

    def _biSizeImage_get(self):
        return b2i(self._biSizeImage)
    def _biSizeImage_set(self, biSizeImage):
        if type(biSizeImage) == bytes:
            biSizeImage = b2i(biSizeImage)
        elif type(biSizeImage) != int:
            raise (TypeError('biSizeImage type error!'))
        self._biSizeImage = i2b(biSizeImage, 4)
    def _biSizeImage_del(self):
        print(f'biSizeImage = {self._biSizeImage} has delete!')
    biSizeImage = property(_biSizeImage_get, _biSizeImage_set, _biSizeImage_del, 'This is biSizeImage')

    def _biXPelsPerMeter_get(self):
        return b2i(self._biXPelsPerMeter)
    def _biXPelsPerMeter_set(self, biXPelsPerMeter):
        if type(biXPelsPerMeter) == bytes:
            biXPelsPerMeter = b2i(biXPelsPerMeter)
        elif type(biXPelsPerMeter) != int:
            raise (TypeError('biXPelsPerMeter type error!'))
        self._biXPelsPerMeter = i2b(biXPelsPerMeter, 4)
    def _biXPelsPerMeter_del(self):
        print(f'biXPelsPerMeter = {self._biXPelsPerMeter} has delete!')
    biXPelsPerMeter = property(_biXPelsPerMeter_get, _biXPelsPerMeter_set, _biXPelsPerMeter_del, 'This is biXPelsPerMeter')

    def _biYPelsPerMeter_get(self):
        return b2i(self._biYPelsPerMeter)
    def _biYPelsPerMeter_set(self, biYPelsPerMeter):
        if type(biYPelsPerMeter) == bytes:
            biYPelsPerMeter = b2i(biYPelsPerMeter)
        elif type(biYPelsPerMeter) != int:
            raise (TypeError('biYPelsPerMeter type error!'))
        self._biYPelsPerMeter = i2b(biYPelsPerMeter, 4)
    def _biYPelsPerMeter_del(self):
        print(f'biYPelsPerMeter = {self._biYPelsPerMeter} has delete!')
    biYPelsPerMeter = property(_biYPelsPerMeter_get, _biYPelsPerMeter_set, _biYPelsPerMeter_del, 'This is biYPelsPerMeter')

    def _biClrUsed_get(self):
        return b2i(self._biClrUsed)
    def _biClrUsed_set(self, biClrUsed):
        if type(biClrUsed) == bytes:
            biClrUsed = b2i(biClrUsed)
        elif type(biClrUsed) != int:
            raise (TypeError('biClrUsed type error!'))
        if biClrUsed not in BITMAPINFOHEADER._biClrUsed_list:
            raise(ValueError(f'biClrUsed must be in {BITMAPINFOHEADER._biClrUsed_list}'))
        self._biClrUsed = i2b(biClrUsed, 4)
    def _biClrUsed_del(self):
        print(f'biClrUsed = {self._biClrUsed} has delete!')
    biClrUsed = property(_biClrUsed_get, _biClrUsed_set, _biClrUsed_del, 'This is biClrUsed')

    def _biClrImportant_get(self):
        return b2i(self._biClrImportant)
    def _biClrImportant_set(self, biClrImportant):
        if type(biClrImportant) == bytes:
            biClrImportant = b2i(biClrImportant)
        elif type(biClrImportant) != int:
            raise (TypeError('biClrImportant type error!'))
        if biClrImportant not in BITMAPINFOHEADER._biClrImportant_list:
            raise(ValueError(f'biClrImportant must be in {BITMAPINFOHEADER._biClrImportant_list}'))
        self._biClrImportant = i2b(biClrImportant, 4)
    def _biClrImportant_del(self):
        print(f'biClrImportant = {self._biClrImportant} has delete!')
    biClrImportant = property(_biClrImportant_get, _biClrImportant_set, _biClrImportant_del, 'This is biClrImportant')

    @staticmethod
    def CreatMapHeader(fr):
        biSize = b2i(fr.read(4))
        biWidth = b2i(fr.read(4))
        biHeight = b2i(fr.read(4))
        biPlanes = b2i(fr.read(2))
        biBitCount = b2i(fr.read(2))
        biCompression = b2i(fr.read(4))
        biSizeImage= b2i(fr.read(4))
        biXPelsPerMeter = b2i(fr.read(4))
        biYPelsPerMeter = b2i(fr.read(4))
        biClrUsed = b2i(fr.read(4))
        biClrImportant = b2i(fr.read(4))
        mapHeader = BITMAPINFOHEADER(biWidth, biHeight, biBitCount)
        mapHeader.biSize = biSize
        mapHeader.biPlanes = biPlanes
        mapHeader.biCompression = biCompression
        mapHeader.biSizeImage = biSizeImage
        mapHeader.biXPelsPerMeter = biXPelsPerMeter
        mapHeader.biYPelsPerMeter = biYPelsPerMeter
        mapHeader.biClrUsed = biClrUsed
        mapHeader.biClrImportant = biClrImportant
        return mapHeader
    def ReadFile(self, fr):
        self.biSize = b2i(fr.read(4))
        self.biWidth = b2i(fr.read(4))
        self.biHeight = b2i(fr.read(4))
        self.biPlanes = b2i(fr.read(2))
        self.biBitCount = b2i(fr.read(2))
        self.biCompression = b2i(fr.read(4))
        self.biSizeImage = b2i(fr.read(4))
        self.biXPelsPerMeter = b2i(fr.read(4))
        self.biYPelsPerMeter = b2i(fr.read(4))
        self.biClrUsed = b2i(fr.read(4))
        self.biClrImportant = b2i(fr.read(4))
    def Write2File(self, fw):
        fw.write(self._biSize)
        fw.write(self._biWidth)
        fw.write(self._biHeight)
        fw.write(self._biPlanes)
        fw.write(self._biBitCount)
        fw.write(self._biCompression)
        fw.write(self._biSizeImage)
        fw.write(self._biXPelsPerMeter)
        fw.write(self._biYPelsPerMeter)
        fw.write(self._biClrUsed)
        fw.write(self._biClrImportant)


class RGBQUAD:
    def __init__(self, rgbRed:int=0, rgbGreen:int=0, rgbBlue:int=0):
        self.rgbRed = rgbRed
        self.rgbGreen = rgbGreen
        self.rgbBlue = rgbBlue
        self.rgbReserved = 0
    def __str__(self):
        result = ''
        result += f'rgbRed           :  {self.rgbRed}\n'
        result += f'rgbGreen         :  {self.rgbGreen}\n'
        result += f'rgbBlue          :  {self.rgbBlue}\n'
        result += f'rgbReserved      :  {self.rgbReserved}\n'
        return result
    def __int__(self):
        num = self.rgbBlue
        num += (self.rgbGreen << 8)
        num += (self.rgbRed << 16)
        num += (self.rgbReserved << 24)
        return num

    def _rgbBlue_get(self):
        return b2i(self._rgbBlue)
    def _rgbBlue_set(self, rgbBlue:int):
        if type(rgbBlue) != int:
            raise(TypeError(f'{rgbBlue} is not "int" type'))
        self._rgbBlue = i2b(rgbBlue % 256, 1)
    def _rgbBlue_del(self):
        print(f'rgbBlue = {self._rgbBlue} has delete!')
    rgbBlue = property(_rgbBlue_get, _rgbBlue_set, _rgbBlue_del, 'This is rgbBlue')

    def _rgbGreen_get(self):
        return b2i(self._rgbGreen)
    def _rgbGreen_set(self, rgbGreen:int):
        if type(rgbGreen) != int:
            raise(TypeError(f'{rgbGreen} is not "int" type'))
        self._rgbGreen = i2b(rgbGreen % 256, 1)
    def _rgbGreen_del(self):
        print(f'rgbGreen = {self._rgbGreen} has delete!')
    rgbGreen = property(_rgbGreen_get, _rgbGreen_set, _rgbGreen_del, 'This is rgbGreen')

    def _rgbRed_get(self):
        return b2i(self._rgbRed)
    def _rgbRed_set(self, rgbRed:int):
        if type(rgbRed) != int:
            raise(TypeError(f'{rgbRed} is not "int" type'))
        self._rgbRed = i2b(rgbRed % 256, 1)
    def _rgbRed_del(self):
        print(f'rgbRed = {self._rgbRed} has delete!')
    rgbRed = property(_rgbRed_get, _rgbRed_set, _rgbRed_del, 'This is rgbRed')

    def _rgbReserved_get(self):
        return b2i(self._rgbReserved)
    def _rgbReserved_set(self, rgbReserved:int):
        if type(rgbReserved) != int:
            raise(TypeError(f'{rgbReserved} is not "int" type'))
        self._rgbReserved = i2b(rgbReserved % 256, 1)
    def _rgbReserved_del(self):
        print(f'rgbReserved = {self._rgbReserved} has delete!')
    rgbReserved = property(_rgbReserved_get, _rgbReserved_set, _rgbReserved_del, 'This is rgbReserved')

    def SetColor(self, **kwargs):
        self.rgbRed = kwargs.get('red', self.rgbRed)
        self.rgbGreen = kwargs.get('green', self.rgbGreen)
        self.rgbBlue = kwargs.get('blue', self.rgbBlue)
        self.rgbReserved = kwargs.get('reserved', self.rgbReserved)

    @staticmethod
    def CreateColor(fr):
        rgbBlue = b2i(fr.read(1))
        rgbGreen = b2i(fr.read(1))
        rgbRed = b2i(fr.read(1))
        rgbReserved = b2i(fr.read(1))
        rgb = RGBQUAD(rgbRed, rgbGreen, rgbBlue)
        rgb.rgbReserved = rgbReserved
        return rgb
    def ReadFile(self, fr):
        self.rgbBlue = b2i(fr.read(1))
        self.rgbGreen = b2i(fr.read(1))
        self.rgbRed = b2i(fr.read(1))
        self.rgbReserved = b2i(fr.read(1))
    def Write2File(self, fw):
        fw.write(self._rgbBlue)
        fw.write(self._rgbGreen)
        fw.write(self._rgbRed)
        fw.write(self._rgbReserved)


class LIST:
    def __init__(self, lenght:int, data:int=0, dmax:int=255):
        if type(lenght) != int or type(data) != int:
            raise(TypeError('lenght and data must int type'))
        if lenght <= 0:
            raise(ValueError('lenght must big more than 0'))
        self._lst = [data for i in range(lenght)]
        self.dmax = dmax
    def __len__(self):
        return len(self._lst)
    def __iter__(self):
        index = 0
        while index < len(self):
            yield self._lst[index]
            index += 1
    def __getitem__(self, key):
        return self._lst[key]
    def __setitem__(self, key, value):
        if type(value) != int:
            raise(ValueError('value must int type'))
        if value < self.dmin or value > self.dmax:
            raise(ValueError('value is out of spec'))
        self._lst[key] = value
    def dmax_get(self):
        return self._dmax
    def dmax_set(self, dmax):
        if type(dmax) != int:
            raise(TypeError(f'{dmax} is not int'))
        if dmax <= 0:
            raise(ValueError(f'{dmax} is less 0'))
        self._dmax = dmax
    def dmax_del(self):
        print('dmax has delete!')
    dmax = property(dmax_get, dmax_set, dmax_del, 'This is dmax')

    @property
    def dmin(self):
        return 0
class BITMAPARRAY:
    def __init__(self, width, height, bitCount):
        self._lst = [LIST(width, 0, 2**bitCount - 1) for i in range(height)]
        self._bitCount = bitCount
    @property
    def width(self):
        return len(self._lst[0])
    @property
    def height(self):
        return len(self._lst)
    @property
    def bitCount(self):
        return self._bitCount
    def __getitem__(self, key):
        return self._lst[key]
    def __setitem__(self, key, value):
        for i in range(self.width):
            self[key][i] = value
    def WriteRow(self, iRow, value):
        for iCol in range(self.width):
            self[iRow][iCol] = value
    def WriteCol(self, iCol, value):
        for iRow in range(self.height):
            self[iRow][iCol] = value
    def WriteData(self, iRow, iCol, value):
        self[iRow][iCol] = value
    def WriteAllData(self, value):
        for iRow in range(self.height):
            for iCol in range(self.width):
                self[iRow][iCol] = value
    def Write2File(self, fw):
        if self.bitCount == 1:
            byteCnt_FullByte = self.width // 8
            bitCnt_PartByte = self.width % 8
            byteCnt_supplement = (self.width * self.bitCount + 31) // 32 * 4 - (self.width // 8) - (1 if self.width % 8 else 0)
            for height in range(self.height-1, -1, -1):
                for grp in range(byteCnt_FullByte):
                    data = 0
                    for i in range(8):
                        data = data * 2 + self[height][8*grp+i]
                    fw.write(i2b(data, 1))
                if bitCnt_PartByte != 0:
                    data = 0
                    for i in range(bitCnt_PartByte):
                        data = data | (self[height][8*byteCnt_FullByte + i] << (7 - i))
                    fw.write(i2b(data, 1))
                if byteCnt_supplement != 0:
                    fw.write(i2b(0, byteCnt_supplement))
        elif self.bitCount == 4:
            byteCnt_FullByte = self.width // 2
            bitCnt_PartByte = self.width % 2
            byteCnt_supplement = (self.width * self.bitCount + 31) // 32 * 4 - (self.width // 2) - (1 if self.width % 2 else 0)
            for height in range(self.height-1, -1, -1):
                for grp in range(byteCnt_FullByte):
                    data = 0
                    for i in range(2):
                        data = data * 16 + self[height][2*grp+i]
                    fw.write(i2b(data, 1))
                if bitCnt_PartByte != 0:
                    data = self[height][self.width - 1] * 16
                    fw.write(i2b(data, 1))
                if byteCnt_supplement != 0:
                    fw.write(i2b(0, byteCnt_supplement))
        elif self.bitCount == 8:
            byteCnt_supplement = (self.width * self.bitCount + 31) // 32 * 4 - self.width
            for height in range(self.height-1, -1, -1):
                for i in range(self.width):
                    data = self[height][i]
                    fw.write(i2b(data, 1))
                fw.write(i2b(1, byteCnt_supplement))
        elif self.bitCount == 24:
            byteCnt_supplement = (self.width * self.bitCount + 31) // 32 * 4 - self.width * 3
            for height in range(self.height-1, -1, -1):
                for width in range(self.width):
                    data = self[height][width]
                    fw.write(i2b(data & 255, 1))
                    fw.write(i2b((data >> 8) & 255, 1))
                    fw.write(i2b((data >> 16) & 255, 1))
            if byteCnt_supplement != 0:
                fw.write(i2b(0, byteCnt_supplement))
        elif self.bitCount == 32:
            for height in range(self.height - 1, -1, -1):
                for width in range(self.width):
                    data = self[height][width]
                    fw.write(i2b((data >> 8) & 255, 1))
                    fw.write(i2b((data >> 16) & 255, 1))
                    fw.write(i2b((data >> 24) & 255, 1))
                    fw.write(i2b(data & 255, 1))
        else:
            raise(ValueError('bitCount must be in (1, 4, 8, 24, 32)'))


class BMP:
    def __init__(self, width, height, bitCount):
        # bitCount: 一个单元占用bit数(1, 4, 8, 24, 32)
        bfOffBits = 14 + 40 + (0 if (bitCount==24 or bitCount==32) else (2**bitCount) * 4)
        bfSize = bfOffBits + ((width * bitCount + 31) // 32 * 4 * height)
        self.fileHeader = BITMAPFILEHEADER(bfSize=bfSize, bfOffBits=bfOffBits)
        self.mapHeader = BITMAPINFOHEADER(biWidth=width, biHeight=height, biBitCount=bitCount)
        if bitCount in (1, 4, 8):
            self.rgbquad = [RGBQUAD() for i in range(2**bitCount)]
        elif bitCount in (24, 32):
            self.rgbquad = []
        self.data = BITMAPARRAY(width, height, bitCount)
    def __del__(self):
        pass
    @staticmethod
    def ReadFile(file):
        with open(file, 'rb') as fr:
            fr.seek(18, 0)
            biWidth = b2i(fr.read(4))
            biHeight = b2i(fr.read(4))
            fr.seek(2, 1)
            biBitCount = b2i(fr.read(2))

            biMap = BMP(biWidth, biHeight, biBitCount)
            fr.seek(0, 0)
            biMap.fileHeader.ReadFile(fr)
            fr.seek(14, 0)
            biMap.mapHeader.ReadFile(fr)
            fr.seek(54, 0)
            if biBitCount in (1, 4, 8):
                for i in range(biMap.mapHeader.biBitCount):
                    biMap.rgbquad[i].ReadFile(fr)

            # biMap.WriteAllData(0)
            fr.seek(biMap.fileHeader.bfOffBits, 0)
            if biBitCount == 1:
                byteCnt_supplement = (biMap.mapHeader.biWidth * biBitCount + 31) // 32 * 4 - (biMap.mapHeader.biWidth // 8) - (1 if biMap.mapHeader.biWidth % 8 else 0)
                for iRow in range(biMap.mapHeader.biHeight - 1, -1, -1):
                    for iCol in range(biMap.mapHeader.biWidth):
                        if iCol % 8 == 0:
                            data = b2i(fr.read(1))
                        biMap.WriteData(iRow, iCol, (data >> (7 - (iCol % 8)) & 0x1))
                    fr.seek(byteCnt_supplement, 1)
            elif biBitCount == 4:
                byteCnt_supplement = (biMap.mapHeader.biWidth * biBitCount + 31) // 32 * 4 - (biMap.mapHeader.biWidth // 2) - (1 if biMap.mapHeader.biWidth % 2 else 0)
                for iRow in range(biMap.mapHeader.biHeight - 1, -1, -1):
                    for iCol in range(biMap.mapHeader.biWidth):
                        if iCol % 2 == 0:
                            data = b2i(fr.read(1))
                        biMap.WriteData(iRow, iCol, (data >> (4 - 4 * (iCol % 2)) & 0xf))
                    fr.seek(byteCnt_supplement, 1)
            elif biBitCount == 8:
                byteCnt_supplement = (biMap.mapHeader.biWidth * biBitCount + 31) // 32 * 4 - biMap.mapHeader.biWidth
                for iRow in range(biMap.mapHeader.biHeight - 1, -1, -1):
                    for iCol in range(biMap.mapHeader.biWidth):
                        biMap.WriteData(iRow, iCol, b2i(fr.read(1)))
                    fr.seek(byteCnt_supplement, 1)
            elif biBitCount == 24:
                byteCnt_supplement = (biMap.mapHeader.biWidth * biBitCount + 31) // 32 * 4 - biMap.mapHeader.biWidth * 3
                for iRow in range(biMap.mapHeader.biHeight - 1, -1, -1):
                    for iCol in range(biMap.mapHeader.biWidth):
                        biMap.WriteData(iRow, iCol, b2i(fr.read(3)))
                    fr.seek(byteCnt_supplement, 1)
            elif biBitCount == 32:
                for iRow in range(biMap.mapHeader.biHeight):
                    for iCol in range(biMap.mapHeader.biWidth):
                        biMap.WriteData(iRow, iCol, b2i(fr.read(4)))
            else:
                raise(ValueError('bitCount must be in (1, 4, 8, 24, 32)'))
            return biMap

    def SetColor(self, index, color:RGBQUAD):
        if type(color) == RGBQUAD:
            self.rgbquad[index].SetColor(red=color.rgbRed, green=color.rgbGreen, blue=color.rgbBlue, reserved=color.rgbReserved)
        elif type(color) == tuple or type(color) == list:
            if len(color) == 3:
                self.rgbquad[index].SetColor(red=color[0], green=color[1], blue=color[2])
            elif len(color) == 4:
                self.rgbquad[index].SetColor(red=color[0], green=color[1], blue=color[2], reserved=color[3])
            else:
                raise(ValueError(f'{color} is out of range'))
        else:
            raise(TypeError(f'{type(color).__name__} is not define type!'))
    def WriteRow(self, iRow, value):
        self.data.WriteRow(iRow, value)
    def WriteCol(self, iCol, value):
        self.data.WriteCol(iCol, value)
    def WriteData(self, iRow, iCol, value):
        self.data.WriteData(iRow, iCol, value)
    def WriteAllDate(self, value):
        self.data.WriteAllData(value)
    def ResetData(self):
        self.data.WriteAllData(0)
    def Save(self, file):
        with open(file, 'wb') as fw:
            self.fileHeader.Write2File(fw)
            self.mapHeader.Write2File(fw)
            if self.mapHeader.biBitCount not in (24, 32):
                for rgb in self.rgbquad:
                    rgb.Write2File(fw)
            self.data.Write2File(fw)


if __name__ == '__main__':
    pass