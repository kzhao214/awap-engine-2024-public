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
        self.sniperpositions = self.mostpath(7, True, self.map.width*self.map.height)
        self.bomberpositions = self.mostpath(3, True, self.map.width*self.map.height)
        self.sunpositions = self.mostpath(7, False, self.map.width*self.map.height)

    def play_turn(self, rc: RobotController):
        self.build_towers(rc)
        self.towers_attack(rc)

    def build_towers(self, rc: RobotController):
        locations = self.sniperpositions.index(max(self.sniperpositions))
        locationb = self.bomberpositions.index(max(self.bomberpositions))
        print(max(self.sniperpositions))
        print(max(self.bomberpositions))
        if(max(self.bomberpositions)*6>max(self.sniperpositions)):
            if (rc.can_build_tower(TowerType.BOMBER, self.indextorow(locationb), self.indextocol(locationb))):
                rc.build_tower(TowerType.BOMBER, self.indextorow(locationb), self.indextocol(locationb))
                self.bomberpositions[locationb] = -1
                self.sniperpositions[locationb] = -1
        else:
            if (rc.can_build_tower(TowerType.GUNSHIP, self.indextorow(locations), self.indextocol(locations))):
                rc.build_tower(TowerType.GUNSHIP, self.indextorow(locations), self.indextocol(locations))
                self.sniperpositions[locations] = -1
                self.bomberpositions[locations] = -1
                
    def indextorow(self, index:int):
        return index//self.map.width
    def indextocol(self, index:int):
        return index%self.map.width

    def mostpath(self, radius: int, is_max: bool, numreturn: int):
        path = []
        for location in range(self.map.width *self.map.height):
            row = self.indextorow(location)
            col = self.indextocol(location)
            if(self.map.is_space(row, col)):
                numberpath = 0
                for a in range(2*radius):
                    for b in range(2*radius):
                        if math.dist([a-8,b-8], [0, 0])< 8:
                            if self.map.is_path(row+a-8,col+b-8):
                                numberpath = numberpath + 1
                path.append(numberpath)
            else:
                if is_max:
                    path.append(-1)
                else:
                    path.append(48*48+1)
        """returningstuff = []
        for i in range(numreturn):
            if is_max:
                returningstuff.append(path.index(max(path)))
                path.pop(path.index(max(path)))
            else:
                returningstuff.append(path.index(min(path)))
                path.pop(path.index(min(path)))
        print(returningstuff)
        """
        print(max(path))
        return path
            

    
    def towers_attack(self, rc: RobotController):
        #Random
        towers = rc.get_towers(rc.get_ally_team())
        for tower in towers:
            if tower.type == TowerType.GUNSHIP:
                rc.auto_snipe(tower.id, SnipePriority.FIRST)
            elif tower.type == TowerType.BOMBER:
                rc.auto_bomb(tower.id)

