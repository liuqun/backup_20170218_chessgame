#-*-coding:utf8;-*-

# 中国象棋棋盘 90 格的坐标约定从 0,0 到 8,9
# 国际象棋棋盘 64 格的坐标约定从 0,0 到 7,7
# 如果没有棋子则在格子上标记 0, 如果有棋子, 则在该格子上放置棋子 ID
# ID>0 表示有棋子, 注意 ID=0 或 None 都代表格子上没有棋子, ID<0 会导致错误
# 棋子从一个格子走到另一个格子后擦除脚印, 只保留棋子当前位置
# gameBoard.hasPieceAtCoordinate([x,y]) 检查棋盘坐标 x,y 位置, 如果发现有棋子则返回棋子的 ID, 否则默认返回 0(或 None 表示 false)
# gameBoard.dump(sys.stdout) 可以通过终端命令提示符窗口(或指定其他日志文件)查看当前棋盘
class GameBoard:
    """GameBoard for 围棋、象棋等棋类游戏的棋盘建模"""
    def width(self): # 棋盘宽度
        return self.__width
    def height(self): # 棋盘高度
        return self.__height
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__pieceNameList = [] # 存储所有棋子的名字字符串, 初始状态为空列表
        self.__players = {} # 存储每个玩家各自拥有的所有棋子的编号, 以玩家名称为键分别存储
        # __battlefield[y][x] 对应坐标点 x,y 处的棋子ID, 初始值 0 表示格子上没有棋子
        self.__battlefield = [[0 for x in range(width)] for y in range(height)]
        self.__survivors = {} # 字典映射记录棋盘上每个棋子的位置, 以棋子 pieceId 为键, 以绝对坐标为值
    def __del__(self):
        pass
    def dump(self, file):
        borad=[
            '┌┬┬┲┳┱┬┬┐',
            '├┼┼╊╳╉┼┼┤',
            '├╬┼╄╇╃┼╬┤',
            '╠┼╬┼╬┼╬┼╣',
            '├┴┴┴┴┴┴┴┤',
            '├┬┬┬┬┬┬┬┤',
            '╠┼╬┼╬┼╬┼╣',
            '├╬┼╆╈╅┼╬┤',
            '├┼┼╊╳╉┼┼┤',
            '└┴┴┺┻┹┴┴┘']
        borad.reverse()
        debugdumpfile = file
        if not file:
            import os
            # 默认将调试日志文件输出到 os.devnull 不输出调试信息
            debugdumpfile = open(os.devnull, 'wa') # 调试信息的设置
        for y in reversed(range(self.__height)):
            for x in range(self.__width):
                id = self.__battlefield[y][x]
                if not id or id<=0: # 0 表示当前格子无棋子, id=None 时也满足该条件, id<0 为异常状态
                    name = borad[y][x]
                else:
                    name = self.__pieceNameList[id-1] # 备忘: ID 最小值是从 1 开始的, 但数组下标是从 0 开始的
                print(name, end='', file=debugdumpfile)
            print(file=debugdumpfile)
        if not file:
            debugdumpfile.close()
    # row(y) --- 返回 y 行上的所有棋子的编号, y 最小值 0
    def row(self, y):
        if (y<0 or y>=self.__height):
            raise ValueError('Error: Invalid coordinate y=%d (acceptable range: from min=0 to max=%d)' % (y, self.__height-1))
        pieces = {}
        for x in range(self.__width):
            id = self.__battlefield[y][x]
            if id and id>0:
                pieces[x] = id #; pieceName = self.__pieceNameList[id-1] ; print(pieceName, end='')
        return pieces
    # column(x) --- 返回 x 列上的所有棋子的编号, x 最小值 0
    def column(self, x):
        if (x<0 or x>=self.__width):
            raise ValueError('Error: Invalid coordinate x=%d (acceptable range: from min=0 to max=%d)' % (x, self.__width-1))
        pieces = {}
        for y in range(self.__height):
            id = self.__battlefield[y][x]
            if id and id>0:
                pieces[y] = id #; pieceName = self.__pieceNameList[id-1] ; print(pieceName)
        return pieces
    def makeIdForNewChessPiece(self, pieceName="", coordinate=None, playerName=""):
        self.__pieceNameList.append(pieceName)
        pieceId = len(self.__pieceNameList)
        try:
            x,y = coordinate
        except TypeError: # coordinate 必须是 x,y 坐标形式, 否则触发 TypeError 异常
            pass          # 注: 这里允许调用者定义一开始不放在棋盘上的棋子
        else:
            if (x<0 or x>=self.__width):
                raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
            if (y<0 or y>=self.__height):
                raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
            self.__battlefield[y][x] = pieceId
            # 注: 考虑以后需要独立更改 x 和 y 的坐标值, 下面存储坐标用的是 [x,y] 而不是 (x,y)
            self.__survivors[pieceId] = [x, y] # 词典以 pieceId 为键, 以棋子坐标为值
        if playerName not in self.__players:
            self.__players[playerName] = []
        self.__players[playerName].append(pieceId)
        return (pieceId) # 返回值最小从 1 开始表示有棋子, pieceId==0 的棋盘格子无棋子
    def hasPieceAtCoordinate(self, coordinate):
        x,y = coordinate # coordinate 必须是 x,y 坐标形式 ----FIXME: 检查参数
        if (x<0 or x>=self.__width):
            return False
        if (y<0 or y>=self.__height):
            return False
        pieceId = self.__battlefield[y][x]
        return pieceId # 注: pieceId 等于 0 时表示当前格子无棋子
    def findPiece(self, pieceId):
        # 备注: 棋盘上找不到棋子时直接抛出 ValueError 异常, 如果找到则返回坐标
        if not pieceId or pieceId<=0 or pieceId>len(self.__pieceNameList): # None 、负数或 0 均为无效棋子 ID
            raise ValueError('Error: Invalid ID=%s' % (str(pieceId)))
        try:
            x,y = self.__survivors[pieceId]
        except KeyError:
            raise ValueError('Notice: 棋盘上找不到棋子 %s' % (self.__pieceNameList[pieceId]))
        return x,y
    # movePieceToCoordinate(id, (x,y)) --- 将编号为 id 的棋子移动到坐标 (x,y) 处
    def movePieceToCoordinate(self, pieceId, coordinate):
        # 备注: 找不到编号为 pieceId 的棋子时直接抛出 ValueError 异常, 如果找到则移动棋子到新坐标
        if not pieceId or pieceId<=0 or pieceId>len(self.__pieceNameList): # None 、负数或 0 均为无效棋子 ID
            raise ValueError('Error: Invalid ID=%s' % (str(pieceId)))
        x,y = coordinate # coordinate 必须是 x,y 坐标形式 ----FIXME: 检查参数
        if (x<0 or x>=self.__width):
            raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
        if (y<0 or y>=self.__height):
            raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
        try:
            past = self.__survivors[pieceId] # get the piece's coordinate in the past
        except KeyError:
            pass
        else:
            self.__battlefield[past[1]][past[0]] = 0 # clear foot-prints of the past
        try: # 从棋盘上移除被吃掉的棋子
            del self.__survivors[self.__battlefield[y][x]]
        except KeyError:
            pass
        self.__battlefield[y][x] = pieceId
        self.__survivors[pieceId] = [x,y]
    def position(self, playerName=None): # 棋盘上双方或某一方玩家剩余的棋子
        if not playerName:
            return self.__survivors.copy()
        try:
            pieces = self.__players[playerName]
        except KeyError:
            result = {}
        else:
            result = {k:v for k,v in self.__survivors.items() if (k in pieces)}
        return result
    # --- “車”的正十字形最大活动范围：
    def rookMoveRange(self, x, y):
        assert(0 <= x < self.__width)
        assert(0 <= y < self.__height)
        return set((i, y) for i in range(self.__width)) ^ set((x, j) for j in range(self.__height))
    # --- “馬”的最大活动范围：
    def knightMoveRange(self, x, y):
        """ knightMoveRange --- “馬”的最大活动范围
        # 示意图：
        #
        # 　　↖　↗
        # 　↖　｜　↗
        # 　　—馬—
        # 　↙　｜　↘
        # 　　↙　↘
        #
        # 棋子走法：先直走一格再斜走一格，这里暂时不考虑蹩马腿的情况
        # 坐标值计算判定：
        # 起点坐标 (x,y)
        # 终点坐标 (i,j)
        # 例如从 (0,0) 到 (1,2) 或从 (0,0) 到 (2,1)
        # 根据直角三角形勾股定理，斜边的平方等于直角边的平方和
        # c^2 = a^2 + b^2
        #     = (x-i)^2 + (y-j)^2
        #     = 1 + 4
        #     = 5
        """
        assert(0 <= x < self.__width)
        assert(0 <= y < self.__height)
        # 挑出以马为中心, 距离(或斜线距离)为 2 格的 5*5 正方形区域:
        # □☒□☒□
        # ☒　　　☒
        # □　馬　□
        # ☒　　　☒
        # □☒□☒□
        box = NewRangeByDistance(2, x, y)
        # 裁剪掉超出棋盘边界的部分, 同时根据勾股定理判断符合条件的终点坐标：
        return {(i, j) for (i, j) in box if ((0 <= i < self.__width) and (0 <= j < self.__height) and ((x-i)**2 + (y-j)**2 == 5))}
    # --- 国际象棋的“王”的最大活动范围
    def kingMoveRange(self, x, y):
        """ kingMoveRange　--- 国际象棋的“王”可以直走或斜走1格，暂时不考虑“王车易位”特殊情况
        # 示意图：
        # ↖↑↗
        # ←♔→
        # ↙↓↘
        """
        # 以王为中心划出 3*3 的 9 格正方形：
        box = NewRangeByDistance(1, x, y)
        # 裁剪掉超出棋盘边界的部分：
        return {(i, j) for (i, j) in box if ((0 <= i < self.__width) and (0 <= j < self.__height))}
    # --- 国际象棋的“后”的最大活动范围
    def queenMoveRange(self, x, y):
        """ queenMoveRange　--- 国际象棋的“后”可以直走斜走任意格，同时具备車和象的功能
        """
        assert(0 <= x < self.__width)
        assert(0 <= y < self.__height)
        return self.rookMoveRange(x, y) | self.bishopMoveRange(x, y)
    # --- 国际象棋的“象”的最大活动范围
    def bishopMoveRange(self, x, y):
        """ bishopMoveRange　--- 国际象棋的“象”可以斜走任意格
        # 对应的线性方程为：
        # y-y0 = k(x-x0)
        # 斜率 k = ±1
        # y-y0 = ±(x-x0)
        """
        assert(0 <= x < self.__width)
        assert(0 <= y < self.__height)
        return {(i, j) for i in range(self.__width) for j in range(self.__height) if abs(y-j) == abs(x-i)}


# NewRangeByDistance --- 到中心坐标点 (centerX,centerY) 距离为 distance 的点的集合
def NewRangeByDistance(distance, centerX, centerY):
    d = int(distance)
    assert(d > 0)
    return {(centerX+x, centerY+y) for x in range(-d,d+1) for y in range(-d,d+1) if (abs(x)==d or abs(y)==d)}


# NewRectangularRange -- 长方形区域, 定义左下角坐标从 x0,y0 起, 点阵尺寸 = rectangleWidth*rectangleHeight, 点阵最少可以是单行、单列或者单个点
def NewRectangularRange(rectangleWidth, rectangleHeight, x0, y0):
    assert(rectangleWidth > 0)
    assert(rectangleHeight > 0)
    return {(x+x0, y+y0) for x in range(rectangleWidth) for y in range(rectangleHeight)}


# 以下为模块自测试代码
def main():
    global __name__
    print('模块名：', __name__)


if '__main__' == __name__ :
    main()
