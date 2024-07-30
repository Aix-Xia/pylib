import math
import turtle


class DIE:
    def __init__(self, xCoor:float, yCoor:float, xSize:float, ySize:float):
        self.xSize = xSize
        self.ySize = ySize
        self.xCoor = xCoor
        self.yCoor = yCoor
    def __str__(self):
        return f'(({self.xCoor}, {self.yCoor}), ({self.xSize}, {self.ySize}))'
    def __xSizeSet(self, xSize):
        if type(xSize) not in (int, float):
            raise(TypeError('xSize Type Error!'))
        if xSize <= 0:
            raise(ValueError('xSize Value Error!'))
        self.__xSize = xSize
    xSize = property(lambda self:self.__xSize, __xSizeSet, lambda self:None)
    def __ySizeSet(self, ySize):
        if type(ySize) not in (int, float):
            raise(TypeError('ySize Type Error!'))
        if ySize <= 0:
            raise(ValueError('xSize Value Error!'))
        self.__ySize = ySize
    ySize = property(lambda self:self.__ySize, __ySizeSet, lambda self:None)
    def __xCoorSet(self, xCoor):
        if type(xCoor) not in (int, float):
            raise(TypeError('xCoor Type Error!'))
        self.__xCoor = xCoor
    xCoor = property(lambda self:self.__xCoor, __xCoorSet, lambda self:None)
    def __yCoorSet(self, yCoor):
        if type(yCoor) not in (int, float):
            raise(TypeError('yCoor Type Error!'))
        self.__yCoor = yCoor
    yCoor = property(lambda self:self.__yCoor, __yCoorSet, lambda self:None)
    @property
    def minDistanceOfDie2WaferCenter(self):
        right = self.xCoor + self.xSize / 2
        left = self.xCoor - self.xSize / 2
        xDistance = 0 if (right * left <= 0) else (-right if (right < 0) else left)
        top = self.yCoor + self.ySize / 2
        bottom = self.yCoor - self.ySize / 2
        yDistance = 0 if (top * bottom <= 0) else (-top if (top < 0) else bottom)
        distance = math.sqrt(xDistance ** 2 + yDistance ** 2)
        return distance
    @property
    def maxDistanceOfDie2WaferCenter(self):
        right = self.xCoor + self.xSize / 2
        left = self.xCoor - self.xSize / 2
        xDistance = right if self.xCoor > 0 else left
        top = self.yCoor + self.ySize / 2
        bottom = self.yCoor - self.ySize / 2
        yDistance = top if self.yCoor > 0 else bottom
        distance = math.sqrt(xDistance ** 2 + yDistance ** 2)
        return distance
    def Draw(self, scale=0.001):
        turtle.penup()
        turtle.goto(scale * (self.xCoor - self.xSize / 2), scale * (self.yCoor + self.ySize / 2))
        turtle.setheading(0)
        turtle.pendown()
        for distance in [scale * self.xSize, scale * self.ySize] * 2:
            turtle.forward(distance)
            turtle.right(90)

class CONFIG:
    def __init__(self):
        # unit um
        self.waferRadius = 150000
        self.trimSize = 5000
        self.xInShotSCL = 80
        self.yInShotSCL = 80
        self.xOutShotSCL = 600
        self.yOutShotSCL = 720
        self.xDieSize = 10500
        self.yDieSize = 10000
        self.xDieCnt = 2
        self.yDieCnt = 3
        self.xShotCoor = 0
        self.yShotCoor = 0
    def __waferRadiusSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__waferRadius = value
    waferRadius = property(lambda self:self.__waferRadius, __waferRadiusSet, lambda self:None)
    def __trimSizeSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__trimSize = value
    trimSize = property(lambda self:self.__trimSize, __trimSizeSet, lambda self:None)
    def __xInShotSCLSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value < 0:
            raise(ValueError('Value Error!'))
        self.__xInShotSCL = value
    xInShotSCL = property(lambda self:self.__xInShotSCL, __xInShotSCLSet, lambda self:None)
    def __yInShotSCLSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value < 0:
            raise(ValueError('Value Error!'))
        self.__yInShotSCL = value
    yInShotSCL = property(lambda self:self.__yInShotSCL, __yInShotSCLSet, lambda self:None)
    def __xOutShotSCLSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value < 0:
            raise(ValueError('Value Error!'))
        self.__xOutShotSCL = value
    xOutShotSCL = property(lambda self:self.__xOutShotSCL, __xOutShotSCLSet, lambda self:None)
    def __yOutShotSCLSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value < 0:
            raise(ValueError('Value Error!'))
        self.__yOutShotSCL = value
    yOutShotSCL = property(lambda self:self.__yOutShotSCL, __yOutShotSCLSet, lambda self:None)
    def __xDieSizeSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__xDieSize = value
    xDieSize = property(lambda self:self.__xDieSize, __xDieSizeSet, lambda self:None)
    def __yDieSizeSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__yDieSize = value
    yDieSize = property(lambda self:self.__yDieSize, __yDieSizeSet, lambda self:None)
    def __xDieCntSet(self, value):
        if type(value) not in (int, ):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__xDieCnt = value
    xDieCnt = property(lambda self:self.__xDieCnt, __xDieCntSet, lambda self:None)
    def __yDieCntSet(self, value):
        if type(value) not in (int, ):
            raise(TypeError('Type Error!'))
        if value <= 0:
            raise(ValueError('Value Error!'))
        self.__yDieCnt = value
    yDieCnt = property(lambda self:self.__yDieCnt, __yDieCntSet, lambda self:None)
    def __xShotCoorSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        self.__xShotCoor = value
    xShotCoor = property(lambda self:self.__xShotCoor, __xShotCoorSet, lambda self:None)
    def __yShotCoorSet(self, value):
        if type(value) not in (int, float):
            raise(TypeError('Type Error!'))
        self.__yShotCoor = value
    yShotCoor = property(lambda self:self.__yShotCoor, __yShotCoorSet, lambda self:None)
    @property
    def xShotSize(self):
        return self.xDieSize * self.xDieCnt + self.xInShotSCL * (self.xDieCnt - 1) + self.xOutShotSCL
    @property
    def yShotSize(self):
        return self.yDieSize * self.yDieCnt + self.yInShotSCL * (self.yDieCnt - 1) + self.yOutShotSCL

class SHOT:
    def __init__(self, xCoor, yCoor, xSize, ySize):
        self.__dieList = []
        self.xSize = xSize
        self.ySize = ySize
        self.xCoor = xCoor
        self.yCoor = yCoor
    def __str__(self):
        result = ''
        for die in self.__dieList:
            result = result + str(die) + '\n'
        return result
    def __iter__(self):
        for die in self.__dieList:
            yield die
    def __len__(self):
        return len(self.__dieList)
    def __xSizeSet(self, xSize):
        if type(xSize) not in (int, float):
            raise(TypeError('xSize Type Error!'))
        if xSize <= 0:
            raise(ValueError('xSize Value Error!'))
        self.__xSize = xSize
    xSize = property(lambda self:self.__xSize, __xSizeSet, lambda self:None)
    def __ySizeSet(self, ySize):
        if type(ySize) not in (int, float):
            raise(TypeError('ySize Type Error!'))
        if ySize <= 0:
            raise(ValueError('xSize Value Error!'))
        self.__ySize = ySize
    ySize = property(lambda self:self.__ySize, __ySizeSet, lambda self:None)
    def __xCoorSet(self, xCoor):
        if type(xCoor) not in (int, float):
            raise(TypeError('xCoor Type Error!'))
        for die in self.__dieList:
            die.xCoor = die.xCoor + xCoor - self.xCoor
        self.__xCoor = xCoor
    xCoor = property(lambda self:self.__xCoor, __xCoorSet, lambda self:None)
    def __yCoorSet(self, yCoor):
        if type(yCoor) not in (int, float):
            raise(TypeError('yCoor Type Error!'))
        for die in self.__dieList:
            die.yCoor = die.yCoor + yCoor - self.yCoor
        self.__yCoor = yCoor
    yCoor = property(lambda self:self.__yCoor, __yCoorSet, lambda self:None)
    @property
    def dieCnt(self):
        return len(self.__dieList)
    def AddDie(self, xCoorBaseShotCenter, yCoorBaseShotCenter, xSize, ySize):
        xDieCoor = self.xCoor + xCoorBaseShotCenter
        yDieCoor = self.yCoor + yCoorBaseShotCenter
        self.__dieList.append(DIE(xDieCoor, yDieCoor, xSize, ySize))
    @staticmethod
    def Generate(config:CONFIG):
        shot = SHOT(config.xShotCoor, config.yShotCoor, config.xShotSize, config.yShotSize)
        for x in range(config.xDieCnt):
            for y in range(config.yDieCnt):
                shot.AddDie((config.xOutShotSCL - config.xShotSize) / 2 + config.xDieSize / 2 + (config.xDieSize + config.xInShotSCL) * x,
                            (config.yOutShotSCL - config.yShotSize) / 2 + config.yDieSize / 2 + (config.yDieSize + config.yInShotSCL) * y,
                            config.xDieSize, config.yDieSize)
        return shot
    def Draw(self, scale=0.001):
        for die in self:
            die.Draw(scale)

def GetFullDieCntOnWafer(config:CONFIG):
    # unit:um
    waferRadius = config.waferRadius    # 150000
    trimSize = config.trimSize          # 5000

    xInShotSCL = config.xInShotSCL      # 80
    yInShotSCL = config.yInShotSCL      # 80
    xOutShotSCL = config.xOutShotSCL    # 600
    yOutShotSCL = config.yOutShotSCL    # 720

    xDieSize = config.xDieSize          # 10500
    yDieSize = config.yDieSize          # 10000
    xDieCnt = config.xDieCnt            # 2
    yDieCnt = config.yDieCnt            # 3

    xShotCoorOffset = config.xShotCoor
    yShotCoorOffset = config.yShotCoor

    xShotSize = config.xShotSize
    yShotSize = config.yShotSize

    shot = SHOT(xShotCoorOffset, yShotCoorOffset, xShotSize, yShotSize)
    for x in range(xDieCnt):
        for y in range(yDieCnt):
            xDieCoor = (xOutShotSCL - xShotSize) / 2 + xDieSize / 2 + (xDieSize + xInShotSCL) * x
            yDieCoor = (yOutShotSCL - yShotSize) / 2 + yDieSize / 2 + (yDieSize + yInShotSCL) * y
            shot.AddDie(xDieCoor, yDieCoor, xDieSize, yDieSize)

    xShotCnt = math.floor((waferRadius - trimSize) / xShotSize) + 4
    yShotCnt = math.floor((waferRadius - trimSize) / yShotSize) + 4

    totalFullDieCnt = 0
    for x in range(-xShotCnt, xShotCnt + 1):
        for y in range(-yShotCnt, yShotCnt + 1):
            shot.xCoor = x * xShotSize + xShotCoorOffset
            shot.yCoor = y * yShotSize + yShotCoorOffset
            for die in shot:
                if die.maxDistanceOfDie2WaferCenter < waferRadius - trimSize:
                    totalFullDieCnt += 1
    return totalFullDieCnt

if __name__ == '__main__':
    # maxDieCnt = 0
    # maxX = 0
    # minDieCnt = 10000
    # minX = 0
    # config = CONFIG()
    #
    # for y in range(config.xShotSize // 10):
    #     for x in range(config.xShotSize // 10):
    #         config.xShotCoor = 10 * x
    #         config.yShotCoor = 10 * y
    #         dieCnt = GetFullDieCntOnWafer(config)
    #         if dieCnt > maxDieCnt:
    #             maxDieCnt = dieCnt
    #             maxX = 10 * x
    #         if dieCnt < minDieCnt:
    #             minDieCnt = dieCnt
    #             minX = 10 * x
    #     print(10*y, minDieCnt, maxDieCnt)
    #
    # print('-' * 50)
    # print(maxX, maxDieCnt)
    # print(minX, minDieCnt)

    turtle.tracer(1)
    config = CONFIG()
    shot = SHOT.Generate(config)
    print(shot)
    shot.Draw(0.01)

    turtle.done()