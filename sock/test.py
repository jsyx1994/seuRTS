import xml.etree.ElementTree as ET
import json
'''
playersss = []
tree = ET.parse('bases8x8.xml')
root = tree.getroot()
terrain = root.find('terrain').text

players = []
loadedPlayers = tree.findall('players/rts.Player')
for player in loadedPlayers:
    players.append(player.attrib)
units = []
loadedUnits = tree.findall('units/rts.units.Unit')
for unit in loadedUnits:
    units.append(unit.attrib)
print(units)
print()
# sunits = [dict([a, int(x)] for a, x in b.items()) for b in units]

for b in units:
    for a, x in b.items():
        try:
            b[a] = int(x)
        except ValueError:
            b[a] = x
print(units)
'''

# x = '{"time":4,"pgs":{"width":8,"height":8,"terrain":"0000000000000000000000000000000000000000000000000000000000000000","players":[{"ID":0, "resources":5},{"ID":1, "resources":5}],"units":[{"type":"Resource", "ID":0, "player":-1, "x":0, "y":0, "resources":20, "hitpoints":1},{"type":"Resource", "ID":1, "player":-1, "x":7, "y":7, "resources":20, "hitpoints":1},{"type":"Base", "ID":2, "player":0, "x":2, "y":1, "resources":0, "hitpoints":10},{"type":"Base", "ID":3, "player":1, "x":5, "y":6, "resources":0, "hitpoints":10}]},"actions":[{"ID":2, "time":0, "action":{"type":4, "parameter":0, "unitType":"Worker"}},{"ID":3, "time":0, "action":{"type":4, "parameter":3, "unitType":"Worker"}}]}'
# msg = json.loads(x)['actions']
# print(msg)
# y = 'hhhh  '
# y = y + json.dumps(msg)
# print (y)


# x = {   'time': 0, 
#         'pgs': {
#                 'width': 8, 
#                 'height': 8, 
#                 'terrain': '0000000000000000000000000000000000000000000000000000000000000000', 
#                 'players': [{'ID': 0, 'resources': 5}, 
#                             {'ID': 1, 'resources': 5}], 
#                 'units':   [{'type': 'Resource', 'ID': 0, 'player': -1, 'x': 0, 'y': 0, 'resources': 20, 'hitpoints': 1}, 
#                             {'type': 'Resource', 'ID': 1, 'player': -1, 'x': 7, 'y': 7, 'resources': 20, 'hitpoints': 1}, 
#                             {'type': 'Base', 'ID': 2, 'player': 0, 'x': 2, 'y': 1, 'resources': 0, 'hitpoints': 10}, 
#                             {'type': 'Base', 'ID': 3, 'player': 1, 'x': 5, 'y': 6, 'resources': 0, 'hitpoints': 10}]
#                 }, 
#         'actions': []
#     }
# print(x['pgs']['width'])
x = {}
x.update()