from src.player import Player
from src.map import Map
from src.robot_controller import RobotController
from src.game_constants import TowerType, Team, Tile, GameConstants, SnipePriority, get_debris_schedule
from src.debris import Debris
from src.tower import Tower
import math

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map
    
    def play_turn(self, rc: RobotController):
        self.build_towers(rc)
        #self.towers_attack(rc)

    def build_towers(self, rc: RobotController):
        location = self.mostpath(60, True, 1)[0]
        if (rc.can_build_tower(TowerType.GUNSHIP, self.indextorow(location), self.indextocol(self.indextocol(location)))):
            rc.build_tower(TowerType.GUNSHIP, self.indextorow(location), self.indextocol(self.indextocol(location)))
                
    def indextorow(self, index:int):
        return index//self.map.width
    def indextocol(self, index:int):
        return index%self.map.width

    def mostpath(self, radius: int, is_max: bool, numreturn: int):
        path = []
        for location in range(self.map.width *self.map.height):
            numberpath = 0
            row = self.indextorow(location)
            col = self.indextocol(location)
            for a in range(2*radius):
                for b in range(2*radius):
                    if math.dist([a-8,b-8], [0, 0])< 8:
                        if self.map.is_path(row+a-8,col+b-8):
                            numberpath = numberpath + 1
            path.append(numberpath)
        returningstuff = []
        for i in range(numreturn):
            if is_max:
                returningstuff.append(path.pop(path.index(max(path))))
            else:
                returningstuff.append(path.pop(path.index(min(path))))
        return returningstuff
            

    
    def towers_attack(self, rc: RobotController):
        #Random
        towers = rc.get_towers(rc.get_ally_team())
        for tower in towers:
            if tower.type == TowerType.GUNSHIP:
                rc.auto_snipe(tower.id, SnipePriority.FIRST)
            elif tower.type == TowerType.BOMBER:
                rc.auto_bomb(tower.id)

