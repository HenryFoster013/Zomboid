import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Tile():
    def __init__(self,position_start,position_end):
        self.position_start = position_start
        self.position_end = position_end
    
    def check_collision(self, pos_x, pos_y):
        return (pos_x >= self.position_start[0] and pos_x <= self.position_end[0]) and (pos_y >= self.position_start[1] and pos_y <= self.position_end[1])

class DiagonalTile():
    def __init__(self, _position_start, _position_end):
        self.position_start = _position_start
        self.position_end = _position_end
        self.thickness = 10
        self.gradient = -165/155
    
    def check_collision(self, pos_x, pos_y):
        m = self.gradient
        x = pos_x
        c = self.position_start[1]
        y = (m*(x - self.position_start[0]))+c 

        return (pos_x >= self.position_start[0] and pos_x <= self.position_end[0]) and (pos_y >= y - 45 and pos_y <= y + 60)
        

#ALL WALLS:
left_house_wall = Tile((806,105),(894,689))
middle_house_wall = Tile((863,610),(1323,690))
diagonal_house_wall = DiagonalTile((1321,649),(1486,494))
right_house_wall = Tile((1481,436),(1804,528))

walls = [left_house_wall,middle_house_wall,right_house_wall]
diagonal_walls = [diagonal_house_wall]
