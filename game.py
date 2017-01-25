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
# 以下为模块自测试代码
def main():
    import sys
    global __name__
    print('模块名：', __name__)
    print('创建中国象棋初始棋盘')
    brd = GameBoard(9, 10)
    class Player:
         def __init__(self, name):
            self.__name = name
            self.rooks = [None]*2
            self.knights = [None]*2
            self.bishops = [None]*2
            self.guards = [None]*2
            self.general = None
            self.cannons = [None]*2
            self.pawns = [None]*5
    black = Player('黑方')
    black.rooks[0] = brd.makeIdForNewChessPiece("車", (0, 9))
    black.rooks[1] = brd.makeIdForNewChessPiece("車", (8, 9))
    black.knights[0] = brd.makeIdForNewChessPiece("马", (1, 9))
    black.knights[1] = brd.makeIdForNewChessPiece("马", (7, 9))
    black.bishops[0] = brd.makeIdForNewChessPiece('象', (2, 9))
    black.bishops[1] = brd.makeIdForNewChessPiece('象', (6, 9))
    black.guards[0] = brd.makeIdForNewChessPiece('士', (3, 9))
    black.guards[1] = brd.makeIdForNewChessPiece('士', (5, 9))
    black.general = brd.makeIdForNewChessPiece('將', (4, 9))
    black.cannons[0] = brd.makeIdForNewChessPiece('砲', (1, 7))
    black.cannons[1] = brd.makeIdForNewChessPiece('砲', (7, 7))
    black.pawns = [brd.makeIdForNewChessPiece('卒', (0, 6)),
                   brd.makeIdForNewChessPiece('卒', (2, 6)),
                   brd.makeIdForNewChessPiece('卒', (4, 6)),
                   brd.makeIdForNewChessPiece('卒', (6, 6)),
                   brd.makeIdForNewChessPiece('卒', (8, 6))]
    red = Player('红方')
    red.rooks[0] = brd.makeIdForNewChessPiece("俥", (0, 0))
    red.rooks[1] = brd.makeIdForNewChessPiece("俥", (8, 0))
    red.knights[0] = brd.makeIdForNewChessPiece("馬", (1, 0))
    red.knights[1] = brd.makeIdForNewChessPiece("馬", (7, 0))
    red.bishops[0] = brd.makeIdForNewChessPiece('相', (2, 0))
    red.bishops[1] = brd.makeIdForNewChessPiece('相', (6, 0))
    red.guards[0] = brd.makeIdForNewChessPiece('仕', (3, 0))
    red.guards[1] = brd.makeIdForNewChessPiece('仕', (5, 0))
    red.general = brd.makeIdForNewChessPiece('帥', (4, 0))
    red.cannons[0] = brd.makeIdForNewChessPiece('炮', (1, 2))
    red.cannons[1] = brd.makeIdForNewChessPiece('炮', (7, 2))
    red.pawns = [brd.makeIdForNewChessPiece('兵', (0, 3)),
                 brd.makeIdForNewChessPiece('兵', (2, 3)),
                 brd.makeIdForNewChessPiece('兵', (4, 3)),
                 brd.makeIdForNewChessPiece('兵', (6, 3)),
                 brd.makeIdForNewChessPiece('兵', (8, 3))]
    brd.dump(sys.stdout)
    print()

    brd.movePieceToCoordinate(red.cannons[0], (4, 2))
    print('红棋炮二平五：')
    brd.dump(sys.stdout)
    print()

    brd.movePieceToCoordinate(black.knights[0], (2, 7))
    print('黑棋马8进7：')
    brd.dump(sys.stdout)
    print()

    brd.movePieceToCoordinate(red.cannons[0], (4, 6))
    print('红棋炮五进四(吃卒)：')
    brd.dump(sys.stdout)
    print()
    game = """
        車┬象士將士象马車
        ├┼┼╊╳╉┼┼┤
        ├砲马╄╇╃┼砲┤
        卒┼卒┼炮┼卒┼卒
        ├┴┴┴┴┴┴┴┤
        ├┬┬┬┬┬┬┬┤
        兵┼兵┼兵┼兵┼兵
        ├╬┼╆╈╅┼炮┤
        ├┼┼╊╳╉┼┼┤
        俥馬相仕帥仕相馬俥
        """

    brd.movePieceToCoordinate(black.knights[0], (4, 6))
    print('黑棋马7进5(吃炮)：')
    brd.dump(sys.stdout)
    game = """
        車┬象士將士象马車
        ├┼┼╊╳╉┼┼┤
        ├砲┼╄╇╃┼砲┤
        卒┼卒┼马┼卒┼卒
        ├┴┴┴┴┴┴┴┤
        ├┬┬┬┬┬┬┬┤
        兵┼兵┼兵┼兵┼兵
        ├╬┼╆╈╅┼炮┤
        ├┼┼╊╳╉┼┼┤
        俥馬相仕帥仕相馬俥
        """
if '__main__' == __name__ :
    main()
