#-*-coding:utf8;-*-


# TODO: 兵的走法必须结合棋盘实际情况才能给出：只能前进不能后退、直走斜吃、可以吃过路兵、首次可以走两格
# TODO: 王車易位必须结合棋盘实际情况才能给出：王和車不能移动动过、被将军时不能借助易位躲闪、易位时王途经的路线不能受敌人攻击
class ChessWithAnalyticGeometry:
    """通过解析几何学原理对国际象棋王、后、車、馬、象的最大活动范围进行计算"""

    def __init__(self):
        self.__width = 8
        self.__height = 8

    # “車”的正十字形最大活动范围：
    def rook_move_range(self, x, y):
        assert (0 <= x < self.__width)
        assert (0 <= y < self.__height)
        return set((i, y) for i in range(self.__width)) ^ set((x, j) for j in range(self.__height))

    # “馬”的最大活动范围：
    def knight_move_range(self, x, y):
        """“馬”的最大活动范围
        # 从起点坐标 (x,y) 出发, 最多可以到达 8 个位置, 然后排除其中超出棋盘边界的格子即可
        # 示意图：
        #
        # 　(x-1,y+2)↖　↗(x+1,y+2)
        # (x-2,y+1)↖　｜　↗(x+2,y+1)
        #          　—馬—
        # (x-2,y-1)↙　｜　↘(x+2,y-1)
        # 　(x-1,y-2)↙　↘(x+1,y-2)
        #
        # 棋子走法：先直走一格再斜走一格，国际象棋不考虑蹩马腿的情况
        """
        assert (0 <= x < self.__width)
        assert (0 <= y < self.__height)
        destinations = {
            (x - 2, y + 1), (x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1),
            (x - 2, y - 1), (x - 1, y - 2), (x + 1, y - 2), (x + 2, y - 1),
        }
        # 剔除超出棋盘边界的点：
        return {(i, j) for (i, j) in destinations if (0 <= i < self.__width) and (0 <= j < self.__height)}

    # 国际象棋的“王”的最大活动范围
    def king_move_range(self, x, y):
        """国际象棋的“王”可以直走或斜走1格，暂时不考虑“王车易位”特殊情况
        # 示意图：
        # ↖↑↗
        # ←♔→
        # ↙↓↘
        """
        # 以王为中心划出 3*3 的 9 格正方形：
        box = range_by_distance(1, x, y)
        # 裁剪掉超出棋盘边界的部分：
        return {(i, j) for (i, j) in box if ((0 <= i < self.__width) and (0 <= j < self.__height))}

    # 国际象棋的“后”的最大活动范围
    def queen_move_range(self, x, y):
        """国际象棋的“后”可以直走斜走任意格，同时具备車和象的功能
        """
        assert (0 <= x < self.__width)
        assert (0 <= y < self.__height)
        return self.rook_move_range(x, y) | self.bishop_move_range(x, y)

    # 国际象棋的“象”的最大活动范围
    def bishop_move_range(self, x, y):
        """国际象棋的“象”可以斜走任意格
        # 对应的线性方程为：
        # y-y0 = k(x-x0)
        # 斜率 k = ±1
        # y-y0 = ±(x-x0)
        """
        assert (0 <= x < self.__width)
        assert (0 <= y < self.__height)
        return {(i, j) for i in range(self.__width) for j in range(self.__height) if abs(y - j) == abs(x - i)}


# 找出所有到中心坐标点 (x0, y0) 距离为 distance 的点, distance>=1
def range_by_distance(distance, x0, y0):
    d = int(distance)
    assert (d > 0)
    return {(x0 + x, y0 + y) for x in range(-d, d + 1) for y in range(-d, d + 1) if (abs(x) == d or abs(y) == d)}


# 以下为模块自测试代码
def main():
    global __name__
    print('模块名：', __name__)


if '__main__' == __name__ :
    main()
