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
        pass


class DiagonalTile():
    def __init__(self,position_start,position_end):
        self.position_start = position_start
        self.position_end = position_end
        self.gradient = (self.position_end(0) - self.position_start(0))/(self.position_end(1)-self.position_start(1))

    def get_start_pos(self):
        return self.position_start
    
    def get_end_pos(self):
        return self.position_end
    
    def check_collision(self, player_pos):
        pass
