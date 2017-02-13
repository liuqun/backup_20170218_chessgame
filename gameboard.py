# -*-coding:utf8;-*-
import abc


class AbstractGameBoard(metaclass=abc.ABCMeta):
    """AbstractGameBoard for 围棋、象棋等棋类游戏的棋盘建模"""

    def width(self):
        """棋盘宽度"""
        return self.__width

    def height(self):
        """棋盘高度"""
        return self.__height

    @abc.abstractmethod
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__piece_name_list = []  # 存储所有棋子的名字字符串, 初始状态为空列表
        self.__players = {}  # 存储每个玩家各自拥有的所有棋子的编号, 以棋子编号为键分别存储每个棋子对应哪一位玩家
        # __battlefield[y][x] 对应坐标点 x,y 处的棋子ID, 初始值 0 表示格子上没有棋子
        self.__battlefield = [[0 for x in range(width)] for y in range(height)]
        self.__survivors = {}  # 字典映射记录棋盘上每个棋子的位置, 以棋子 pieceId 为键, 以绝对坐标为值

    @abc.abstractmethod
    def dump(self, file):
        """dump(sys.stdout) -- 通过终端命令提示符窗口(或指定其他日志文件)查看当前棋盘"""
        pass

    def make_id_for_new_chess_piece(self, owner, name="？", coordinate=None):
        self.__piece_name_list.append(name)
        piece_id = len(self.__piece_name_list)
        try:
            x, y = coordinate
        except TypeError:  # coordinate 必须是 x,y 坐标形式, 否则触发 TypeError 异常
            pass  # 注: 这里允许调用者定义一开始不放在棋盘上的棋子
        else:
            if x < 0 or x >= self.__width:
                raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
            if y < 0 or y >= self.__height:
                raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
            self.__battlefield[y][x] = piece_id
            # 注: 考虑以后需要独立更改 x 和 y 的坐标值, 下面存储坐标用的是 [x,y] 而不是 (x,y)
            self.__survivors[piece_id] = [x, y]  # 词典以 piece_id 为键, 以棋子坐标为值
        self.__players[piece_id] = owner
        return piece_id  # 返回值最小从 1 开始表示有棋子, piece_id==0 的棋盘格子无棋子

    def change_piece_name(self, piece_id, new_name):
        if not piece_id or piece_id <= 0:
            raise ValueError('invaild piece_id=%(pid)d' % {'pid': piece_id})
        try:
            self.__piece_name_list[piece_id - 1] = new_name
        except IndexError:
            raise ValueError('invaild piece_id=%(pid)d' % {'pid': piece_id})

    def get_piece_name_by_piece_id(self, piece_id):
        if not piece_id or piece_id <= 0:
            raise ValueError('invaild piece_id=%(pid)d' % {'pid': piece_id})
        try:
            return self.__piece_name_list[piece_id - 1]
        except IndexError:
            raise ValueError('invaild piece_id=%(pid)d' % {'pid': piece_id})

    def has_piece_at_coordinate(self, coordinate):
        """has_piece_at_coordinate((x,y)) -- 检查棋盘坐标 x,y 位置, 如果发现有棋子则返回棋子的 ID, 否则默认返回 0(或 None 表示 false)"""
        x, y = coordinate  # coordinate 必须是 x,y 坐标形式 ----FIXME: 检查参数
        if x < 0 or x >= self.__width:
            return False
        if y < 0 or y >= self.__height:
            return False
        piece_id = self.__battlefield[y][x]
        return piece_id  # 注: piece_id 等于 0 时表示当前格子无棋子

    def find_piece(self, piece_id):
        # 备注: 棋盘上找不到棋子时直接抛出 ValueError 异常, 如果找到则返回坐标
        if not piece_id or piece_id <= 0 or piece_id > len(self.__piece_name_list):  # None 、负数或 0 均为无效棋子 ID
            raise ValueError('Error: Invalid ID=%s' % (str(piece_id)))
        try:
            x, y = self.__survivors[piece_id]
        except KeyError:
            raise ValueError('Notice: 棋盘上找不到棋子 %s' % (self.__piece_name_list[piece_id]))
        return x, y

    def move_piece_to_coordinate(self, piece_id, coordinate):
        """move_piece_to_coordinate(id, (x,y)) -- 将编号为 id 的棋子移动到坐标 (x,y) 处

        备注: 找不到编号为 piece_id 的棋子时直接抛出 ValueError 异常, 如果找到则移动棋子到新坐标
        """
        if not piece_id or piece_id <= 0 or piece_id > len(self.__piece_name_list):  # None 、负数或 0 均为无效棋子 ID
            raise ValueError('Error: Invalid ID=%s' % (str(piece_id)))
        x, y = coordinate  # coordinate 必须是 x,y 坐标形式 ----FIXME: 检查参数
        if x < 0 or x >= self.__width:
            raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
        if y < 0 or y >= self.__height:
            raise ValueError('Error: Invalid coordinate=%s' % (str(coordinate)))
        try:
            past = self.__survivors[piece_id]  # get the piece's coordinate in the past
        except KeyError:
            pass
        else:
            self.__battlefield[past[1]][past[0]] = 0  # clear foot-prints of the past
        try:  # 从棋盘上移除被吃掉的棋子
            del self.__survivors[self.__battlefield[y][x]]
        except KeyError:
            pass
        self.__battlefield[y][x] = piece_id
        self.__survivors[piece_id] = [x, y]

    def owner_of_piece(self, piece_id):
        """查询指定棋子的拥有者"""
        owner = None
        if not piece_id:
            return owner  # 注: 空格 piece_id = 0 对应拥有者 owner = None
        if piece_id < 0 or piece_id > len(self.__piece_name_list):
            raise ValueError('Error: invalid piece_id={}'.format(piece_id))
        owner = self.__players[piece_id]
        return owner


class ChineseXiangqiBoard(AbstractGameBoard):
    """中国象棋棋盘"""
    def __init__(self):
        super().__init__(9, 10)

    def dump(self, file):
        """dump(sys.stdout) -- 通过终端命令提示符窗口(或指定其他日志文件)查看当前棋盘"""
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
        debug_dump_file = file
        if not file:
            import os
            # 默认将调试日志文件输出到 os.devnull 不输出调试信息
            debug_dump_file = open(os.devnull, 'wa')  # 调试信息的设置
        print('１２３４５６７８９', file=debug_dump_file)
        for y in reversed(range(self.height())):
            for x in range(self.width()):
                piece_id = self.has_piece_at_coordinate(coordinate=(x, y))
                if not piece_id or piece_id <= 0:  # 0 表示当前格子无棋子, None 也表示当前格子无棋子, <0 为异常状态
                    name = board[y][x]
                else:
                    name = self.get_piece_name_by_piece_id(piece_id)
                print(name, end='', file=debug_dump_file)
            print(file=debug_dump_file)
        print('九八七六五四三二一', file=debug_dump_file)
        if not file:
            debug_dump_file.close()


class ChessBoard(AbstractGameBoard):
    """国际象棋棋盘"""
    def __init__(self):
        super().__init__(8, 8)

    def dump(self, file):
        """dump(sys.stdout) -- 通过终端命令提示符窗口(或指定其他日志文件)查看当前棋盘"""
        board = [
            '　█　█　█　█',
            '█　█　█　█　',
            '　█　█　█　█',
            '█　█　█　█　',
            '　█　█　█　█',
            '█　█　█　█　',
            '　█　█　█　█',
            '█　█　█　█　']
        board.reverse()
        debug_dump_file = file
        if not file:
            import os
            # 默认将调试日志文件输出到 os.devnull 不输出调试信息
            debug_dump_file = open(os.devnull, 'wa')  # 调试信息的设置
        for y in reversed(range(self.height())):
            print('%(row_number)d ' % {'row_number': y+1}, end='', file=debug_dump_file)
            for x in range(self.width()):
                piece_id = self.has_piece_at_coordinate(coordinate=(x, y))
                if not piece_id or piece_id <= 0:  # 0 表示当前格子无棋子, None 也表示当前格子无棋子, <0 为异常状态
                    name = board[y][x]
                else:
                    name = self.get_piece_name_by_piece_id(piece_id)
                print(name, end='', file=debug_dump_file)
            print(file=debug_dump_file)
        print('  ＡＢＣＤＥＦＧＨ', file=debug_dump_file)
        if not file:
            debug_dump_file.close()


def main():
    brd = ChessBoard()
    import sys
    brd.dump(file=sys.stdout)
    print(file=sys.stdout)

    class Player:
        def __init__(self, name):
            self.__name = str(name)
            self.rooks = [None]*2
            self.knights = [None]*2
            self.bishops = [None]*2
            self.king = None
            self.queen = None
            self.pawns = [None]*8

        def name(self):
            return str(self.__name) # 不允许改名, 如果需要改名只能去创建另一个新的 Player 对象

    players = {
        0: Player('白棋'),
        1: Player('黑棋')}
    for i in players.keys():
        players[i].king = brd.make_id_for_new_chess_piece(i)
        players[i].queen = brd.make_id_for_new_chess_piece(i)
        players[i].rooks[0] = brd.make_id_for_new_chess_piece(i)
        players[i].rooks[1] = brd.make_id_for_new_chess_piece(i)
        players[i].knights[0] = brd.make_id_for_new_chess_piece(i)
        players[i].knights[1] = brd.make_id_for_new_chess_piece(i)
        players[i].bishops[0] = brd.make_id_for_new_chess_piece(i)
        players[i].bishops[1] = brd.make_id_for_new_chess_piece(i)
        for j in range(8):
            players[i].pawns[j] = brd.make_id_for_new_chess_piece(i)
    current_battle_field = {
        players[0].king: {'name': 'Ｋ', 'coordinate':(4, 0)},
        players[1].king: {'name': 'ｋ', 'coordinate':(4, 7)},
        players[0].queen: {'name': 'Ｑ', 'coordinate':(3, 0)},
        players[1].queen: {'name': 'ｑ', 'coordinate':(3, 7)},
        players[0].rooks[0]: {'name': 'Ｒ', 'coordinate':(0, 0)},
        players[0].rooks[1]: {'name': 'Ｒ', 'coordinate':(7, 0)},
        players[1].rooks[0]: {'name': 'ｒ', 'coordinate':(0, 7)},
        players[1].rooks[1]: {'name': 'ｒ', 'coordinate':(7, 7)},
        players[0].knights[0]: {'name': 'Ｎ', 'coordinate':(1, 0)},
        players[0].knights[1]: {'name': 'Ｎ', 'coordinate':(6, 0)},
        players[1].knights[0]: {'name': 'ｎ', 'coordinate':(1, 7)},
        players[1].knights[1]: {'name': 'ｎ', 'coordinate':(6, 7)},
        players[0].bishops[0]: {'name': 'Ｂ', 'coordinate':(2, 0)},
        players[0].bishops[1]: {'name': 'Ｂ', 'coordinate':(5, 0)},
        players[1].bishops[0]: {'name': 'ｂ', 'coordinate':(2, 7)},
        players[1].bishops[1]: {'name': 'ｂ', 'coordinate':(5, 7)},
    }
    for i in range(8):
        k = players[0].pawns[i]
        v = {'name': 'Ｐ', 'coordinate':(i, 1)}
        current_battle_field[k] = v
        k = players[1].pawns[i]
        v = {'name': 'ｐ', 'coordinate':(i, 6)}
        current_battle_field[k] = v

    for k, v in current_battle_field.items():
        name = v['name']
        coordinate = v['coordinate']
        brd.change_piece_name(k, name)
        brd.move_piece_to_coordinate(k, coordinate)
    brd.dump(file=sys.stdout)
    print(file=sys.stdout)

    # 国际象棋最短的棋局：
    brd.move_piece_to_coordinate(players[0].pawns[6], (6, 3))
    brd.dump(file=sys.stdout)
    print('[白棋]兵G4', file=sys.stdout)
    print(file=sys.stdout)
    brd.move_piece_to_coordinate(players[1].pawns[4], (4, 4))
    brd.dump(file=sys.stdout)
    print('[黑棋]兵E5', file=sys.stdout)
    print(file=sys.stdout)
    brd.move_piece_to_coordinate(players[0].pawns[5], (5, 2))
    brd.dump(file=sys.stdout)
    print('[白棋]兵F3', file=sys.stdout)
    print(file=sys.stdout)
    brd.move_piece_to_coordinate(players[1].queen, (7, 3))
    brd.dump(file=sys.stdout)
    print('[黑棋]后H4 ++', file=sys.stdout)


if '__main__' == __name__ :
    main()
