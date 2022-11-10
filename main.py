from DemoParser import Q3_DemoParser
import json
def createKeyValue(configString):
	tmp = {}
	arr = configString.split("\\")
	for i in range(len(arr)-1):
		check = arr[i].strip()
		if(not check):
			continue

		tmp[arr[i]] = arr[i+1]
		i+=1
	return tmp

parser = Q3_DemoParser("/home/lotzy/Desktop/php_quake3_demoparser/cut_air+rg.dm_68")
pow_player =[]
s = 0
while((state:= parser.nextFrame())):
	#if(state.PacketType == parser.Q3_DEMOPARSER_SVC_GAMESTATE):
	print('iteration: '+str(s))
	if(state.PacketType == parser.Q3_DEMOPARSER_SVC_SNAPSHOT):
		for i in range(state.Packet.NumEntities):
			#if (parser.parseEntities[i].eType == 2):
			#	print(parser.parseEntities[i].number)
			print(parser.entityBaselines[i].eType)
		pow_player.append({
			'origin':state.Packet.Ps.Origin,
			'viewangles':[
				state.Packet.Ps.ViewAngles[0],
				state.Packet.Ps.ViewAngles[1],
				state.Packet.Ps.ViewAngles[2]
			]
			})
	s+=1


with open('pow_player.json', 'w') as pow_file:
    pow_file.write(json.dumps(pow_player))