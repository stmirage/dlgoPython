from dlgo.gamemodels.point import Point



def is_point_an_eye(board, point, color):
    '''
Что мы считаем глазом?
для отладки - глаз это пустая точка у которой все соседние по горизонтали-вертикали
и минимум 3 из 4х диагональных с дружественными камнями
для глаз на краю доски все диагональные камни должны быть дружественными
'''

    if board.get(point) is not None:
        return False # Глаз это пустая точка
    
    for neighbor in point.neighbors: # Все соседние точки по горизонтали-вертикали должны быть своими
        if board.is_on_grid(neighbor):
            neighbor.color = board.get(neighbor)
            if neighbor.color!=color:
                return False 

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]

    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
            return off_board_corners + friendly_corners == 4 # на углах и сторонах все углы должны быть дружественными
    return friendly_corners >= 3 # Минимум три угла дружественные