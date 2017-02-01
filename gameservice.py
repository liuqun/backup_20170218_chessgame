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


if '__main__' == __name__ :
    main()
