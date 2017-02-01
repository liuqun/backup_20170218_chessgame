# -*-encoding:utf8;-*-


class GameService:
    """游戏"""

    def __init__(self, player_id_list, player_name_list=None):
        """invite all players into game

        # Arguments:
        # player_id_list -- 玩家 ID 列表，用一组纯数字表示。
        #                   每位玩家有且仅有一个不重复的 ID 编号，比赛开始后不允许更改。
        #                   约定所有玩家按照 ID 大小决定走棋先后顺序, ID 最小的玩家先走
        # player_name -- 玩家名字一般用字符串表示。允许两名玩家重名，因为内部只通过玩家 ID 编号进行区分
        """
        assert player_id_list
        assert(len(list(player_id_list)) >= 1)
        self.__players = dict(zip(player_id_list, player_name_list))
        self.__loop_order = sorted(self.__players.keys()) # 记录多名玩家走棋循环次序
        self.__turn = 0  # self.__loop_order[self.__turn] 指向当前轮到走棋的这名玩家的 ID

    def total_players(self):
        return len(self.__players)

    def get_current_player_id(self):
        return self.__loop_order[self.__turn]

    def end_this_turn(self):
        self.__turn = (self.__turn + 1) % self.total_players()


# 以下为模块自测试代码
def main():
    global __name__
    print('模块名：', __name__)

    class Player:
        def __init__(self, name):
            self.__name = str(name)
            self.rooks = [None]*2
            self.knights = [None]*2
            self.bishops = [None]*2
            self.guards = [None]*2
            self.general = None
            self.cannons = [None]*2
            self.pawns = [None]*5

        def name(self):
            return str(self.__name) # 不允许改名, 如果需要改名只能去创建另一个新的 Player 对象

    red = Player('红棋')
    black = Player('黑棋')
    RED_PLAYER_ID = 1
    BLACK_PLAYER_ID = 2
    svc = GameService([RED_PLAYER_ID, BLACK_PLAYER_ID], [red.name(), black.name()])
    print('%(total)d 位棋手已经就位' % {'total': svc.total_players()})

    from game import GameBoard
    brd = GameBoard(9, 10)
    black.rooks[0] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, "車", (0, 9))
    black.rooks[1] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, "車", (8, 9))
    black.knights[0] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, "马", (1, 9))
    black.knights[1] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, "马", (7, 9))
    black.bishops[0] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '象', (2, 9))
    black.bishops[1] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '象', (6, 9))
    black.guards[0] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '士', (3, 9))
    black.guards[1] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '士', (5, 9))
    black.general = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '將', (4, 9))
    black.cannons[0] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '砲', (1, 7))
    black.cannons[1] = brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '砲', (7, 7))
    black.pawns = [brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '卒', (0, 6)),
                   brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '卒', (2, 6)),
                   brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '卒', (4, 6)),
                   brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '卒', (6, 6)),
                   brd.make_id_for_new_chess_piece(BLACK_PLAYER_ID, '卒', (8, 6))]
    red.rooks[0] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, "俥", (0, 0))
    red.rooks[1] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, "俥", (8, 0))
    red.knights[0] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, "馬", (1, 0))
    red.knights[1] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, "馬", (7, 0))
    red.bishops[0] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '相', (2, 0))
    red.bishops[1] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '相', (6, 0))
    red.guards[0] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '仕', (3, 0))
    red.guards[1] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '仕', (5, 0))
    red.general = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '帥', (4, 0))
    red.cannons[0] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '炮', (1, 2))
    red.cannons[1] = brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '炮', (7, 2))
    red.pawns = [brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '兵', (0, 3)),
                 brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '兵', (2, 3)),
                 brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '兵', (4, 3)),
                 brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '兵', (6, 3)),
                 brd.make_id_for_new_chess_piece(RED_PLAYER_ID, '兵', (8, 3))]
    import sys
    brd.dump(sys.stdout)
    print()

    PLAYER_TABLE = {BLACK_PLAYER_ID: black, RED_PLAYER_ID: red}

    i = svc.get_current_player_id()
    player = PLAYER_TABLE[i]
    piece_selected = player.cannons[0]
    brd.movePieceToCoordinate(piece_selected, (4, 2))
    print('[%(player_name)s]炮八平五：' % {'player_name': player.name()})
    brd.dump(sys.stdout)
    print()
    svc.end_this_turn()

    i = svc.get_current_player_id()
    player = PLAYER_TABLE[i]
    piece_selected = player.knights[0]
    brd.movePieceToCoordinate(piece_selected, (2, 7))
    print('黑棋马2进3：')
    brd.dump(sys.stdout)
    print()
    svc.end_this_turn()

    i = svc.get_current_player_id()
    player = PLAYER_TABLE[i]
    brd.movePieceToCoordinate(player.cannons[0], (4, 6))
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
    svc.end_this_turn()

    i = svc.get_current_player_id()
    player = PLAYER_TABLE[i]
    brd.movePieceToCoordinate(player.knights[0], (4, 6))
    print('黑棋马3进5(吃炮)：')
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
    svc.end_this_turn()


if '__main__' == __name__ :
    main()
