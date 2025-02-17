import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Tile():
    def __init__(self,position_start,position_end):
        self.position_start = position_start
        self.position_end = position_end

    def get_start_pos(self):
        return self.position_start
    
    def get_end_pos(self):
        return self.position_end
    
    def check_collision(self, player_pos):
        if (player_pos[0] >= self.position_start[0] and player_pos[0] <= self.position_end[0]) and (player_pos[1] >= self.position_start[1] and player_pos[1] <= self.position_end[1]):
            return True
        else:
            return False

class DiagonalTile():
    def __init__(self,position_start,position_end,thickness):
        self.position_start = position_start
        self.position_end = position_end
        self.thickness = thickness
        self.gradient = (self.position_end(0) - self.position_start(0))/(self.position_end(1)-self.position_start(1))

    def get_start_pos(self):
        return self.position_start
    
    def get_end_pos(self):
        return self.position_end
    
    def check_collision(self, player_pos):
        m = self.gradient
        x = player_pos[0]
        c = self.position_start[0]
        y = (m*x)+c 

        if (player_pos[0] >= self.position_start[0] and player_pos[0] <= self.position_end[0]) and (player_pos[1] >= y and player_pos[1] <= y + 10):
            return True
        else:
            return False
        

#ALL WALLS:
left_house_wall = Tile((826,105),(864,689))
middle_house_wall = Tile((863,656),(1323,690))
diagonal_house_wall = DiagonalTile((1321,649),(1486,494))
right_house_wall = Tile((1481,496),(1804,528))

walls = ["left_house_wall","middle_house_wall","right_house_wall"]
diagonal_walls = ["diagonal_house_wall"]
