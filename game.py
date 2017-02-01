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
        self.__players = {}  # 存储每个玩家各自拥有的所有棋子的编号, 以玩家编号为键分别存储
        # __battlefield[y][x] 对应坐标点 x,y 处的棋子ID, 初始值 0 表示格子上没有棋子
        self.__battlefield = [[0 for x in range(width)] for y in range(height)]
        self.__survivors = {} # 字典映射记录棋盘上每个棋子的位置, 以棋子 pieceId 为键, 以绝对坐标为值
    def dump(self, file):
        board = [
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
        board.reverse()
        debugdumpfile = file
        if not file:
            import os
            # 默认将调试日志文件输出到 os.devnull 不输出调试信息
            debugdumpfile = open(os.devnull, 'wa') # 调试信息的设置
        for y in reversed(range(self.__height)):
            for x in range(self.__width):
                id = self.__battlefield[y][x]
                if not id or id<=0: # 0 表示当前格子无棋子, id=None 时也满足该条件, id<0 为异常状态
                    name = board[y][x]
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
    def make_id_for_new_chess_piece(self, owner, name="？", coordinate=None):
        self.__pieceNameList.append(name)
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
        if owner not in self.__players:
            self.__players[owner] = []
        self.__players[owner].append(pieceId)
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
    def position(self, owner=None):  # 棋盘上双方或某一方玩家剩余的棋子
        if owner is None:  # 若未指定查询对象，则默认返回双方所有棋子
            return self.__survivors.copy()
        try:
            pieces = self.__players[owner]
        except KeyError:
            result = {}
        else:
            result = {k:v for k,v in self.__survivors.items() if (k in pieces)}
        return result


# 以下为模块自测试代码
def main():
    global __name__
    print('模块名：', __name__)


if '__main__' == __name__ :
    main()
