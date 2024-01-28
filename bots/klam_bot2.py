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
        self.counter = 0
        self.sniperpositions = self.mostpath(7, True, self.map.width*self.map.height)
        self.bomberpositions = self.mostpath(3, True, self.map.width*self.map.height)
        self.sunpositions = self.mostpath(7, False, self.map.width*self.map.height)
        self.placedsun = []
        self.attack = 0
        self.solarzero = 0
        
    def play_turn(self, rc: RobotController):
        #if rc.can_send_debris(1, 45):
        #    rc.send_debris(1, 45)
        self.build_towers(rc)
        self.towers_attack(rc)

    def build_towers(self, rc: RobotController):
        locations = self.sniperpositions.index(max(self.sniperpositions))
        locationb = self.bomberpositions.index(max(self.bomberpositions))
        locationsun = self.sunpositions.index(min(self.sunpositions))
        print(self.counter)
        if(self.counter ==0 and self.solarzero < len(self.placedsun)):
            print("HIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            x = self.indextorow(self.placedsun[len(self.placedsun)-1])
            y = self.indextocol(self.placedsun[len(self.placedsun)-1])
            towertosell = rc.sense_towers_within_radius_squared(rc.get_ally_team(), x, y, 0)[0]
            rc.sell_tower(towertosell)
            self.placedsun.pop(len(self.placedsun)-1)
            if (rc.can_build_tower(TowerType.GUNSHIP, x, y)):
                rc.build_tower(TowerType.GUNSHIP, x, y)
        else:
            if((len(rc.get_debris(rc.get_ally_team()))!=0
                and rc.get_debris(rc.get_ally_team())[0].progress < self.map.path_length/3
                and min(self.sunpositions)==0)
                or self.attack==7):
                if (rc.can_build_tower(TowerType.SOLAR_FARM, self.indextorow(locationsun), self.indextocol(locationsun))):
                    rc.build_tower(TowerType.SOLAR_FARM, self.indextorow(locationsun), self.indextocol(locationsun))
                    self.bomberpositions[locationsun] = -1
                    self.sniperpositions[locationsun] = -1
                    self.sunpositions[locationsun] = 2305
                    self.placedsun.append(locationsun)
                    self.attack = 0
                    self.counter -= 1
                    if(min(self.sunpositions)==0):
                        self.solarzero += 1
            else:
                if(max(self.bomberpositions)*6>max(self.sniperpositions)):
                    if (rc.can_build_tower(TowerType.BOMBER, self.indextorow(locationb), self.indextocol(locationb))):
                        rc.build_tower(TowerType.BOMBER, self.indextorow(locationb), self.indextocol(locationb))
                        self.bomberpositions[locationb] = -1
                        self.sniperpositions[locationb] = -1
                        self.sunpositions[locationb] = 2305
                        self.attack += 1
                        self.counter -= 1
                else:
                    if (rc.can_build_tower(TowerType.GUNSHIP, self.indextorow(locations), self.indextocol(locations))):
                        rc.build_tower(TowerType.GUNSHIP, self.indextorow(locations), self.indextocol(locations))
                        self.sniperpositions[locations] = -1
                        self.bomberpositions[locations] = -1
                        self.sunpositions[locations] = 2305
                        self.attack += 1
                        self.counter -= 1
                
    def indextorow(self, index:int):
        return index//self.map.width
    def indextocol(self, index:int):
        return index%self.map.width

    def mostpath(self, radius: int, is_max: bool, numreturn: int):
        path = []
        self.counter = 0
        for location in range(self.map.width *self.map.height):
            row = self.indextorow(location)
            col = self.indextocol(location)
            if(self.map.is_space(row, col)):
                numberpath = 0
                for a in range(2*radius):
                    for b in range(2*radius):
                        if (math.dist([a-radius,b-radius], [0, 0])< radius) and row+a-radius>=0 and col+b-radius>=0:
                            if self.map.is_path(row+a-radius,col+b-radius):
                                numberpath = numberpath + 1
                path.append(numberpath)
                self.counter +=1
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
        return path
            

    
    def towers_attack(self, rc: RobotController):
        #Random
        towers = rc.get_towers(rc.get_ally_team())
        for tower in towers:
            if tower.type == TowerType.GUNSHIP:
                rc.auto_snipe(tower.id, SnipePriority.FIRST)
            elif tower.type == TowerType.BOMBER:
                rc.auto_bomb(tower.id)

