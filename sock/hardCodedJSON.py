import json
import xml.etree.ElementTree as ET


class UnitType:
    def __init__(self):
        self.ID = 0
        self.cost = 1 
        self.hp = 1
        self.minDamage = 1
        self.maxDamage = 1 
        self.attackRange = 1
        self.produceTime = 10 
        self.moveTime = 10
        self.attackTime = 10 
        self.harvestTime = 10 
        self.returnTime = 10
        self.harvestAmount = 1 
        self.sightRadius = 4
        self.name = 'deafult'
        self.isResource = False 
        self.isStockpile = False 
        self.canHarvest = False 
        self.canMove = True
        self.canAttack = True
        self._produce = []
        self._producedBy = []

        
    def produces(self,ut):
        self._produce.append(ut.name)
        ut._producedBy.append(self.name)

    def producedBy(self,ut):
        ut._producedBy.append(ut.name)
        


    def toJSON(self):
        ID = self.ID; name = self.name; cost = self.cost; hp = self.hp 
        minDamage = self.minDamage; maxDamage = self.maxDamage; attackRange = self.attackRange
        produceTime = self.produceTime; moveTime = self.moveTime; attackTime = self.attackTime
        harvestTime = self.harvestTime; returnTime = self.returnTime
        harvestAmount = self.harvestAmount; sightRadius = self.sightRadius 
        isResource = str(self.isResource).casefold()
        isStockpile = str(self.isStockpile).casefold()
        canHarvest = str(self.canHarvest).casefold()
        canMove = str(self.canMove).casefold()
        canAttack= str(self.canAttack).casefold()
        msg = '{'
        msg = msg +'"ID":{}, "name":"{}", "cost":{}, "hp":{}, "minDamage":{}, "maxDamage":{}, "attackRange":{}, "produceTime":{}, "moveTime":{}, "attackTime":{}, "harvestTime":{}, "returnTime":{}, "harvestAmount":{}, "sightRadius":{}, "isResource":{}, "isStockpile":{}, "canHarvest":{}, "canMove":{}, "canAttack":{}, "produces":[' \
                     .format(ID, name, cost, hp, minDamage, maxDamage, attackRange, 
                             produceTime, moveTime, attackTime, harvestTime, returnTime, \
                            harvestAmount, sightRadius, isResource, isStockpile, \
                            canHarvest, canMove, canAttack)
        
        first = True
        for utName in self._produce:
            if first is False:
                msg = msg + ', '
            msg = msg + '"%s"'%utName
            first = False

        msg = msg +'], "producedBy":['
        first = True
        for utName in self._producedBy:
            if first is False:
                msg = msg + ', '
            msg = msg + '"%s"'%utName
            first = False
        msg = msg +']}'
        
        return msg
    
class UnitTypeTable:
    _unitTypes = []
    _moveConflictResolutionStrategy = 1 # default: 1, Non-deterministic: 2
    
    def __init__(self,json = None):
        self.jsonString = json
        # Resource
        resource = UnitType()
        resource.name = "Resource"
        resource.isResource = True
        resource.isStockpile = False
        resource.canHarvest = False
        resource.canMove = False
        resource.canAttack = False
        resource.sightRadius = 0
        self.addUnitType(resource)
      
                
        # BASE
        base = UnitType()
        base.name = "Base"
        base.cost = 10
        base.hp = 10
        base.isResource = False
        base.isStockpile = True
        base.canHarvest = False
        base.canMove = False
        base.canAttack = False
        base.sightRadius = 5
        # Only ORIGINAL VERSION
        base.produceTime = 250
        self.addUnitType(base)
        '''
        switch(version) {
            case VERSION_ORIGINAL: base.produceTime = 250;
                                   break;
            case VERSION_ORIGINAL_FINETUNED: base.produceTime = 200;
                                   break;
        }
        '''
        

        # BARRACKS
        barracks = UnitType()
        barracks.name = "Barracks"
        barracks.cost = 5
        barracks.hp = 4
        barracks.isResource = False
        barracks.isStockpile = False
        barracks.canHarvest = False
        barracks.canMove = False
        barracks.canAttack = False
        barracks.sightRadius = 3
        # Only ORIGINAL VERSION        
        barracks.produceTime = 200
        self.addUnitType(barracks)
        '''
        switch(version) {
            case VERSION_ORIGINAL: 
                barracks.produceTime = 200;
                break;
            case VERSION_ORIGINAL_FINETUNED: 
            case VERSION_NON_DETERMINISTIC:
                barracks.produceTime = 100;
                break;
        }
        '''
 
        
        # WORKER
        worker = UnitType()
        worker.name = "Worker"
        worker.cost = 1
        worker.hp = 1
        worker.attackRange = 1
        worker.produceTime = 50
        worker.moveTime = 10
        worker.attackTime = 5
        worker.harvestTime = 20
        worker.returnTime = 10
        worker.isResource = False
        worker.isStockpile = False
        worker.canHarvest = True
        worker.canMove = True
        worker.canAttack = True
        worker.sightRadius = 3
        # Only ORIGINAL VERSION
        worker.minDamage = worker.maxDamage = 1
        self.addUnitType(worker)   
        '''
        switch(version) {
            case VERSION_ORIGINAL:
            case VERSION_ORIGINAL_FINETUNED:
                worker.minDamage = worker.maxDamage = 1;
                break;
            case VERSION_NON_DETERMINISTIC:
                worker.minDamage = 0;
                worker.maxDamage = 2;
                break;
        }
        '''
        
        # LIGHT: 
        light = UnitType()
        light.name = "Light"
        light.cost = 2
        light.hp = 4
        light.attackRange = 1
        light.produceTime = 80
        light.moveTime = 8
        light.attackTime = 5
        light.isResource = False
        light.isStockpile = False
        light.canHarvest = False
        light.canMove = True
        light.canAttack = True
        light.sightRadius = 2
        # Only ORIGINAL VERSION
        light.minDamage = light.maxDamage = 2
        self.addUnitType(light)           
        '''
        switch(version) {
            case VERSION_ORIGINAL:
            case VERSION_ORIGINAL_FINETUNED:
                light.minDamage = light.maxDamage = 2
                break
            case VERSION_NON_DETERMINISTIC:
                light.minDamage = 1
                light.maxDamage = 3
                break
        '''


        # HEAVY: 
        heavy = UnitType()
        heavy.name = "Heavy"
        heavy.attackRange = 1
        heavy.produceTime = 120
        heavy.attackTime = 5
        heavy.isResource = False
        heavy.isStockpile = False
        heavy.canHarvest = False
        heavy.canMove = True
        heavy.canAttack = True
        heavy.sightRadius = 2
        # Only ORIGINAL VERSION
        heavy.minDamage = heavy.maxDamage = 4
        heavy.moveTime = 12
        heavy.hp = 4
        heavy.cost = 2
        self.addUnitType(heavy)           
        
        '''
        switch(version) {
            case VERSION_ORIGINAL:
            case VERSION_ORIGINAL_FINETUNED:
                heavy.minDamage = heavy.maxDamage = 4
                break
            case VERSION_NON_DETERMINISTIC:
                heavy.minDamage = 0
                heavy.maxDamage = 6
                break
        }
        
        switch(version) {
            case VERSION_ORIGINAL: 
                heavy.moveTime = 12
                heavy.hp = 4
                heavy.cost = 2
                break
            case VERSION_ORIGINAL_FINETUNED: 
            case VERSION_NON_DETERMINISTIC:
                heavy.moveTime = 10
                heavy.hp = 8
                heavy.cost = 3
                break
        }
        '''


        # RANGED: 
        ranged = UnitType()
        ranged.name = "Ranged"
        ranged.cost = 2
        ranged.hp = 1
        ranged.attackRange = 3
        ranged.produceTime = 100
        ranged.moveTime = 10
        ranged.attackTime = 5
        ranged.isResource = False
        ranged.isStockpile = False
        ranged.canHarvest = False
        ranged.canMove = True
        ranged.canAttack = True
        ranged.sightRadius = 3
        # Only ORIGINAL VERSION
        ranged.minDamage = ranged.maxDamage = 1
        self.addUnitType(ranged)     
        '''
        switch(version) {
            case VERSION_ORIGINAL:
            case VERSION_ORIGINAL_FINETUNED:
                ranged.minDamage = ranged.maxDamage = 1
                break
            case VERSION_NON_DETERMINISTIC:
                ranged.minDamage = 1
                ranged.maxDamage = 2
                break
        }
        '''

        
        base.produces(worker)  
        barracks.produces(light)
        barracks.produces(heavy) 
        barracks.produces(ranged)
        worker.produces(base)
        worker.produces(barracks)

    def fromJSON(self,json = None):
        pass

    def addUnitType(self,ut):
        ut.ID = len(self._unitTypes)
        self._unitTypes.append(ut)

    def toJSON(self):
        first = True
        msg = '{"moveConflictResolutionStrategy":%i,"unitTypes":['%(self._moveConflictResolutionStrategy)
        for ut in self._unitTypes:
            if first is False:
                msg = msg + ', '
            msg = msg + ut.toJSON()
            first = False
        msg = msg + ']}'
        return msg

class GameState:
    def __init__(self,pgs,utt):
        self.time = 0
        self.pgs = pgs
        self.utt = utt
        self.unitActions = []


    def toJSON(self):
        msg = '{'
        msg = msg + '"time":{},"pgs":'.format(self.time)
        msg = msg + self.pgs.toJSON()
        msg = msg + ',"actions":'
        msg = msg + json.dumps(self.unitActions) + '}'

        return msg
    
    def fromJSON(self,string):
        msg = json.load(string)["actions"]
        if len(self.unitActions) != len(msg):
            self.unitActions = msg
        else:
            for i in len(msg):
                self.unitActions[i].update(msg[i])
     

class PhysicalGameState:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.terrain = ''
        self.players = []
        self.units = []
    
    def load(self, fileName, utt):
        tree = ET.parse('fileName')
        root = tree.getroot()
        self.width = root.attrib.get('width')
        self.height = root.attrib.get('height')
        self.terrain = root.find('terrain').text

        players = [] 
        loadedPlayers = tree.findall('players/rts.Player')
        for player in loadedPlayers:
            players.append(player.attrib)

        self.players = [dict([a, int(x)] for a, x in b.items()) for b in players]

        units = []
        loadedUnits = tree.findall('units/rts.units.Unit')
        for unit in loadedUnits:
            units.append(unit.attrib)

        for b in units:
            for a, x in b.items():
                try:
                    b[a] = int(x)
                except ValueError:
                    b[a] = x
        self.units = units


    def toJSON(self):
        msg = '{'
        msg = msg + '"width":{},"height":{},"terrain":'.format(self.width, self.height)
        msg = msg + self.terrain + '",'
        msg = msg + '"players":' + str(self.players) + ',"units":' + str(self.units) + '}'
        return msg


class UnitAction:
    # The 'no-op' action
    TYPE_NONE = 0
    # Action of moving
    TYPE_MOVE = 1
    # Action of harvesting
    TYPE_HARVEST = 2
    # Action of return to base with resource
    TYPE_RETURN = 3
    # Action of produce a unit
    TYPE_PRODUCE = 4
    # Action of attacking a location
    TYPE_ATTACK_LOCATION = 5
    # Total number of action types
    NUMBER_OF_ACTION_TYPES = 6
    ActionName = ["wait", "move", "harvest", "return", "produce", "attack_location"]
    
	# Direction of 'standing still'
    DIRECTION_NONE = -1
    
    # Alias for directions
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    
    DIRECTION_NAMES = ["up", "right", "down", "left"]
 
	
    def __init__(self,type = TYPE_NONE, parameter = DIRECTION_NONE, x = 0, y =0):
        self.type = type
        self.parameter = parameter
        self.x = x
        self.y = y



if __name__ == "__main__":
    utt = UnitTypeTable()
    msg = utt.toJSON()
    print(msg)



