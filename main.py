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
data =[]
while((state:= parser.nextFrame())):
	#if(state.PacketType == parser.Q3_DEMOPARSER_SVC_GAMESTATE):
		#config = parser.currentGameState.ConfigStrings
		#for k in range(len(config)):
		#	v = config[k]
		#	if(k == 0 or k == 1 or k >= 544 and k < 608):
		#		config[k] = createKeyValue(config[k])
		#try:
		#	print("GameVersion: "+config[20])
		#except:
		#	pass
#
		#print("CurrentPlayerNum: "+str(parser.currentGameState.ClientNum))
		#print("PlayerOfDemo:")
		#try:
		#	print(config[544+parser.currentGameState.ClientNum])
		#except:
		#	pass
		#print("ConfigStrings:")
		#print(parser.currentGameState.SnapShots)

#	elif(state.PacketType == parser.Q3_DEMOPARSER_SVC_SERVERCOMMAND):
#		print("ServerCommand received:")
#		print(state.Packet)
	if(state.PacketType == parser.Q3_DEMOPARSER_SVC_SNAPSHOT):
		#print(state.Packet.Ps.Stats)
		#print(state.Packet.Ps.ViewAngles)
		#print(state.Packet.MessageNum)

		data.append({'origin':state.Packet.Ps.Origin,'viewangles':[state.Packet.Ps.ViewAngles[0],state.Packet.Ps.ViewAngles[1]]})
		#print(state.Packet.Ps.Velocity)
		#print(state.Packet.Ps.DeltaAngles)
		#parseEntities
		#ents = parser.entityBaselines
		#for i in range(len(ents)):
		#	if ents[i].number!=0 and ents[i].pos.trBase!=[0,0,0]:
#
#				print(ents[i].number)
#				print(ents[i].pos.trBase)

	#print('____')


with open('convert.txt', 'w') as convert_file:
     convert_file.write(json.dumps(data))
data2 = [] 
i = 0
print(parser.estates)
for val in parser.estates:
	data2.append([])
	d = {}
	for val2 in val:
		d[val2.number] = {'origin':val2.pos.trBase,'viewangles':[val2.apos.trBase[0],val2.apos.trBase[1]]}
	data2[i].append(d)
	i+=1
with open('convert2.txt', 'w') as convert_file:
     convert_file.write(json.dumps(data2))