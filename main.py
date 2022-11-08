from DemoParser import Q3_DemoParser

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

parser = Q3_DemoParser("/home/lotzy/Desktop/pyquake/test.dm_68")
while((state:= parser.nextFrame())):
	if(state.PacketType == parser.Q3_DEMOPARSER_SVC_GAMESTATE):
		config = parser.currentGameState.ConfigStrings
		for k in range(len(config)):
			v = config[k]
			if(k == 0 or k == 1 or k >= 544 and k < 608):
					config[k] = createKeyValue(config[k])
		try:
			print("GameVersion: "+config[20])
		except:
			pass

		print("CurrentPlayerNum: "+str(parser.currentGameState.ClientNum))
		print("PlayerOfDemo:")
		try:
			print(config[544+parser.currentGameState.ClientNum])
		except:
			pass
		print("ConfigStrings:")
		print(config)

	elif(state.PacketType == parser.Q3_DEMOPARSER_SVC_SERVERCOMMAND):
		print("ServerCommand received:")
		print(state.Packet)
	elif(state.PacketType == parser.Q3_DEMOPARSER_SVC_SNAPSHOT):
		print("Snapshot received (ServerTime: "+str(state.Packet.ServerTime)+")")
		print(state.Packet)