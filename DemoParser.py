from Message import Q3_Message
from GameState import Q3_GameState
from ServerCommand import Q3_ServerCommand
from Snapshot import Q3_Snapshot
from PlayerState import Q3_PlayerState
from EntityState import Q3_EntityState
from ParserState import Q3_ParserState
from struct import unpack,pack

class Q3_DemoParser:
	# some parts converted from source code of quake3 (id software)
	Q3_DEMOPARSER_STATE_PARSING = 1
	Q3_DEMOPARSER_STATE_FINISHED = 2
	Q3_DEMOPARSER_STATE_ERROR = 3

	Q3_DEMOPARSER_GENTITYNUM_BITS = 10

	Q3_DEMOPARSER_MAX_RELIABLE_COMMANDS = 64
	Q3_DEMOPARSER_MAX_CONFIGSTRINGS = 1024
	Q3_DEMOPARSER_MAX_GAMESTATE_CHARS = 16000

	Q3_DEMOPARSER_MAX_GENTITIES = (1 << 10)

	Q3_DEMOPARSER_SVC_NOP = 1
	Q3_DEMOPARSER_SVC_GAMESTATE = 2
	Q3_DEMOPARSER_SVC_CONFIGSTRING = 3
	Q3_DEMOPARSER_SVC_BASELINE = 4
	Q3_DEMOPARSER_SVC_SERVERCOMMAND = 5
	Q3_DEMOPARSER_SVC_DOWNLOAD = 6 # skipped in demo messages...
	Q3_DEMOPARSER_SVC_SNAPSHOT = 7
	Q3_DEMOPARSER_SVC_EOF = 8
	def __init__(self, filename):
		self.cycle = None
		self.configStrings = []
		self.parseEntitiesNum = 0
		self.packetLoop = []
		self.gameStates = []
		self.ErrorString = None
		self.c = 0
		self.snap = Q3_Snapshot()
		self.estates = []
		self.entityBaselines = []
		for i in range(1024):
			self.entityBaselines.append(Q3_EntityState())

		self.parseEntities = []
		for i in range(2048):
			self.parseEntities.append(Q3_EntityState())

		self.snapshots = []
		for i in range(32):
			self.snapshots.append(Q3_Snapshot())

		self.fileHandler = open(filename, "rb")
		#if(!file_exists(filename))
		#	throwException("can't open demofile filename...");

		self.currentGameState = Q3_GameState()

		self.state = Q3_DemoParser.Q3_DEMOPARSER_STATE_PARSING

	def nextFrame(self):
		self.c +=1
		self.estates.append([])
		print('parser interation: '+str(self.c))
		if(not self.packetLoop):
			self.packetLoop = self.readDemoMessage()

		if isinstance(self.packetLoop, list):
			for i in range(len(self.packetLoop)):
				packet = self.packetLoop[i]
				del self.packetLoop[i]
				return Q3_ParserState(packet[0], packet[1])

		if(self.state == Q3_DemoParser.Q3_DEMOPARSER_STATE_ERROR or self.state == Q3_DemoParser.Q3_DEMOPARSER_STATE_FINISHED):
			return False

	def readDemoMessage(self):
		self.currentGameState.ServerMessageSequence = self.readIntegerFromStream()

		if(self.currentGameState.ServerMessageSequence == False):
			self.state = Q3_DemoParser.Q3_DEMOPARSER_STATE_FINISHED
			return None

		msg = Q3_Message(Q3_Message.Q3_MAX_MSGLEN)
		msg.CurSize = self.readIntegerFromStream()

		if(msg.CurSize > msg.MaxSize):
			print("Read successfully finished")
			self.state = Q3_DemoParser.Q3_DEMOPARSER_STATE_FINISHED
			return None

		if(not (data:= self.fileHandler.read(msg.CurSize))):
			print("readDemoMessage(): demo file was truncated! (self.cycle)")
			quit()
		msg.setData(data)
		msg.ReadCount = 0

		return self.parseServerMessage(msg)

	def parseServerMessage(self, msg):

		self.currentGameState.ReliableAcknowledge = msg.ReadLong()
		if(self.currentGameState.ReliableAcknowledge < self.currentGameState.ReliableSequence - Q3_DemoParser.Q3_DEMOPARSER_MAX_RELIABLE_COMMANDS):
			self.currentGameState.ReliableAcknowledge = self.currentGameState.ReliableSequence

		ret = []
		while(True):
			if(msg.ReadCount > msg.CurSize):
				print("parseServerMessage(): read past end of server message. (self.cycle)")
				quit()
			cmd = msg.ReadByte()
			if(cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_EOF):
				break
			if cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_NOP:
				ret.append([None,Q3_DemoParser.Q3_DEMOPARSER_SVC_NOP])
			elif cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_GAMESTATE:
				ret.append([self.parseGameState(msg),Q3_DemoParser.Q3_DEMOPARSER_SVC_GAMESTATE])
			elif cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_SERVERCOMMAND:
				if(tmp := self.parseServerCommand(msg)):
					ret.append([tmp, Q3_DemoParser.Q3_DEMOPARSER_SVC_SERVERCOMMAND])
			elif cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_SNAPSHOT:
				ret.append([self.parseSnapShot(msg),Q3_DemoParser.Q3_DEMOPARSER_SVC_SNAPSHOT])
			elif cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_DOWNLOAD:
				ret.append([None,Q3_DemoParser.Q3_DEMOPARSER_SVC_DOWNLOAD])
			else:
				print("illegible server message. (self.cycle)")	
				quit()
		return ret

	def parseServerCommand(self,msg):
		seq = msg.ReadLong()
		cmd = msg.ReadString()

		if(self.currentGameState.ServerCommandSequence >= seq):
			return None # we have already stored ...

		self.currentGameState.ServerCommandSequence = seq
		return Q3_ServerCommand(cmd, seq)

	def parseSnapShot(self,msg):
		newSnap = Q3_Snapshot()
		oldSnap = None

		newSnap.ServerCommandNum = self.currentGameState.ServerCommandSequence
		newSnap.ServerTime = msg.ReadLong()
		newSnap.MessageNum = self.currentGameState.ServerMessageSequence

		deltaNum = msg.ReadByte()
		if(not deltaNum):
			newSnap.DeltaNum = -1
		else:
			newSnap.DeltaNum = newSnap.MessageNum - deltaNum

		newSnap.SnapFlags = msg.ReadByte()

		if(newSnap.DeltaNum <= 0):
			newSnap.Valid = True
			oldSnap = None
		else:
			#oldSnap = &self.snapshots[newSnap.DeltaNum & 31]
			oldSnap = self.snapshots[newSnap.DeltaNum & 31]
			if(not oldSnap.Valid):
				pass
				# printing "Delta from invalid frame (not supposed to happen!)"
			elif(oldSnap.MessageNum != newSnap.DeltaNum):
				pass
				# printing "Delta parseEntitiesNum too old."
			elif(self.parseEntitiesNum - oldSnap.ParseEntitiesNum > 2048-128):
				pass
				# printing "Delta parseEntitiesNum too old."
			else:
				newSnap.Valid = True

		len = msg.ReadByte()
		if(len > 32):
			print("Invalid size for areamask.")
			quit()

		newSnap.Areamask = msg.ReadData(len)

		if(not oldSnap):
			msg,oldSnap,newSnap.Ps = self.readDeltaPlayerstate( msg, oldSnap, newSnap.Ps )
			oldSnap = None
		else:
			msg, oldSnap.Ps, newSnap.Ps = self.readDeltaPlayerstate( msg, oldSnap.Ps, newSnap.Ps )
		
		msg, oldSnap, newSnap = self.readPacketEntities(msg, oldSnap, newSnap)
		#print(oldSnap.number)
		#print(newSnap.number)
		# if not valid, dump the entire thing now that it has
		# been properly read
		if(not newSnap.Valid):
			return

		oldMessageNum = self.snap.MessageNum + 1

		if(newSnap.MessageNum - oldMessageNum >= 32):
			oldMessageNum = newSnap.MessageNum - 31

		while(oldMessageNum < newSnap.MessageNum):
			self.snapshots[oldMessageNum & 31].Valid = False
			oldMessageNum+=1

		self.snap = newSnap
		self.snap.Ping = 999

		self.snapshots[self.snap.MessageNum & 31] = self.snap
		return newSnap

	def parseGameState(self, msg):
		gameDataLen = 0
		self.gameStates.append(self.currentGameState)
		self.currentGameState = Q3_GameState();

		self.currentGameState.ServerCommandSequence = msg.ReadLong()

		while(True):
			cmd = msg.ReadByte()

			if(cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_EOF):
				break

			if(cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_CONFIGSTRING):
				configStringNum = msg.ReadShort()
				if(configStringNum < 0 or configStringNum >= Q3_DemoParser.Q3_DEMOPARSER_MAX_CONFIGSTRINGS):
					print("parseGameState(): configstrings > MAX_CONFIGSTRINGS! (self.cycle)")
					quit()

				configString = msg.ReadBigString()

				self.currentGameState.ConfigStrings.append(configString)

				if( (gameDataLen + 1 + len(configString)) > Q3_DemoParser.Q3_DEMOPARSER_MAX_GAMESTATE_CHARS):
					# quake3 allow max 16000 gameState data because his char array in c struct is only Q3_DEMOPARSER_MAX_GAMESTATE_CHARS bytes (gameState_t.stringData)
					print("parseGameState(): gameStateData > Q3_DEMOPARSER_MAX_GAMESTATE_CHARS! (self.cycle)")
					quit()

				gameDataLen += len(configString) + 1 # for quake3 max gamestate chars check...

			elif(cmd == Q3_DemoParser.Q3_DEMOPARSER_SVC_BASELINE):
				newNum = msg.ReadBits(Q3_DemoParser.Q3_DEMOPARSER_GENTITYNUM_BITS)
				if(newNum < 0 or newNum >= Q3_DemoParser.Q3_DEMOPARSER_MAX_GENTITIES):
					print("parseGameState(): baseline entities out of range! (self.cycle)")
					quit()

				nullState = Q3_EntityState()
				es = self.entityBaselines[newNum]
				msg, nullstate, es = self.parseDeltaEntity(msg, nullState, es, newNum)

			else:
				print("parseGameState(): bad gamestate command byte. (self.cycle)")
				quit()
		self.currentGameState.ClientNum = msg.ReadLong()
		self.currentGameState.ChecksumFeed = msg.ReadLong()

		return True
	def parseDeltaEntity(self, msg, fr, to, number):
		# throw all into >> /dev/null
		if(number < 0 or number >= Q3_DemoParser.Q3_DEMOPARSER_MAX_GENTITIES):
			print("Bad delta entity number: number (self.cycle)")
			quit()
		# check for remove
		if(msg.ReadBits(1) == 1):
			to = Q3_EntityState()
			to.number = Q3_DemoParser.Q3_DEMOPARSER_MAX_GENTITIES-1
			self.estates[self.c-1].append(to)
			print('________________')
			print(to.number)
			print(to.pos.trBase)
			print('________________')
			return msg,to,fr

		# check for no delta
		if(msg.ReadBits(1) == 0):
			to = fr
			to.number = number
			self.estates[self.c-1].append(to)
			print('________________')
			print(to.number)
			print(to.pos.trBase)
			print('________________')
			return msg,to,fr

		lc = msg.ReadByte()
		to.number = number

		for i in range(lc):
			if(msg.ReadBits(1) == 0):
				exec("to."+Q3_EntityState.NetFields[i][0]+" = fr."+Q3_EntityState.NetFields[i][0])
			else:
				if(Q3_EntityState.NetFields[i][1] == 0):
					if(msg.ReadBits(1) == 1):
						if(msg.ReadBits(1) == 0):
							# integral float
							trunc = msg.ReadBits(13) # FLOAT_IN_BITS (QUAKE3)
							# bias to allow equal parts positive and negative
							trunc -= (1<<(13-1))
							exec("to."+Q3_EntityState.NetFields[i][0]+" = float(trunc)")
						else:
							exec("to."+Q3_EntityState.NetFields[i][0]+" = unpack('f',pack('I',msg.ReadBits(32)))[0]") # full floating point value (QUAKE3)
			
				else:
					if(msg.ReadBits(1) == 0):
						exec("to."+Q3_EntityState.NetFields[i][0]+" = float(0)")
					else:
						exec("to."+Q3_EntityState.NetFields[i][0]+" = float(msg.ReadBits("+str(Q3_EntityState.NetFields[i][1])+"))") # full floating point value (QUAKE3)

		for i in range(lc,len(Q3_EntityState.NetFields)):
			exec("to."+Q3_EntityState.NetFields[i][0]+" = fr."+Q3_EntityState.NetFields[i][0])
		self.estates[self.c-1].append(to)
		print('________________')
		print(to.number)
		print(to.pos.trBase)
		print('________________')
		return msg,fr,to

	def readDeltaPlayerstate(self, msg, oldPs, newPs ):
		if(oldPs == None):
			oldPs = Q3_PlayerState()

		lc = msg.ReadByte()
		for i in range(lc):
			if(not msg.ReadBits(1)):
				# no changes... copy from delta playerstate...
				# magic and dirty ;)
				exec("newPs."+Q3_PlayerState.NetFields[i][0]+" = oldPs."+Q3_PlayerState.NetFields[i][0])
			else:
				if(Q3_PlayerState.NetFields[i][1] == 0):
					if(msg.ReadBits(1) == 0):
						# integral float
						trunc = int(msg.ReadBits(13))

						# bias to allow equal parts positive and negative
						trunc -= (1<<(13-1))

						# magic and dirty ;)
						exec("newPs."+Q3_PlayerState.NetFields[i][0]+" = float(trunc)")
					else:
						# full floating point value
						# magic and dirty ;)
						exec("newPs."+Q3_PlayerState.NetFields[i][0]+" = unpack('f',pack('I',msg.ReadBits(32)))[0]")
				else:
					# magic and dirty ;)
					exec("newPs."+Q3_PlayerState.NetFields[i][0]+" = int(msg.ReadBits("+str(Q3_PlayerState.NetFields[i][1])+"))")

		for i in range(lc,len(Q3_PlayerState.NetFields)):
			# magic and dirty ;)
			exec("newPs."+Q3_PlayerState.NetFields[i][0]+" = oldPs."+Q3_PlayerState.NetFields[i][0])

		if(msg.ReadBits(1)):
			# parse stats array
			if(msg.ReadBits(1)):
				bits = msg.ReadShort();
				for i in range(16):
					if(bits & (1<<i)):
						newPs.Stats.append(msg.ReadShort())

			# parse persistant array
			if(msg.ReadBits(1)):
				bits = msg.ReadShort()
				for i in range(16):
					if(bits & (1<<i)):
						newPs.Persistant.append(msg.ReadShort())

			# parse ammo array
			if(msg.ReadBits(1)):
				bits = msg.ReadShort()
				for i in range(16):
					if(bits & (1<<i)):
						newPs.Ammo.append(msg.ReadShort())

			# parse powerups array
			if(msg.ReadBits(1)):
				bits = msg.ReadShort()
				for i in range(16):
					if(bits & (1<<i)):
						newPs.Powerups[i] = msg.ReadShort()
		return msg,oldPs, newPs

	def readPacketEntities(self, msg, oldSnap, newSnap):
		newSnap.ParseEntitiesNum = self.parseEntitiesNum
		newSnap.NumEntities = 0

		oldindex = 0
		oldstate = None
		oldnum = 0

		if(oldSnap == None):
			oldnum = 99999
		else:
			if(oldindex >= oldSnap.NumEntities):
				oldnum = 99999
			else:
				oldstate = self.parseEntities[(oldSnap.ParseEntitiesNum + oldindex) & (2048-1)]
				oldnum = oldstate.number

		while(True):
			newnum = int(msg.ReadBits(10))

			if( newnum == (Q3_DemoParser.Q3_DEMOPARSER_MAX_GENTITIES-1)):
				break

			if(msg.ReadCount > msg.CurSize):
				print("end of message")
				quit()
			while(oldnum < newnum):

				msg, newSnap, oldstate = self.deltaEntity(msg, newSnap, oldnum, oldstate, True)
				oldindex+=1

				if(oldindex >= oldSnap.NumEntities):
					oldnum = 99999
				else:
					oldstate = self.parseEntities[(oldSnap.ParseEntitiesNum + oldindex) & (2048-1)]
					oldnum = oldstate.number

			if(oldnum == newnum):
				msg, newSnap, oldstate = self.deltaEntity(msg, newSnap, newnum, oldstate, False)
				oldindex+=1

				if(oldindex >= oldSnap.NumEntities):
					oldnum = 99999
				else:
					oldstate = self.parseEntities[(oldSnap.ParseEntitiesNum + oldindex) & (2048-1)]
					oldnum = oldstate.number
				continue

			if(oldnum > newnum):
				# delta from baseline

				msg, newSnap, self.entityBaselines[newnum] = self.deltaEntity(msg, newSnap, newnum, self.entityBaselines[newnum], False)
				#print(self.entityBaselines[newnum].origin)
				continue

		# any remaining entities in the old frame are copied over
		while( oldnum != 99999 ):
			# one or more entities from the old packet are unchanged
			msg, newSnap, oldState = self.deltaEntity(msg, newSnap, oldnum, oldstate, True)

			oldindex+=1

			if(oldindex >= oldSnap.NumEntities):
				oldnum = 99999
			else:
				oldstate = self.parseEntities[(oldSnap.ParseEntitiesNum + oldindex) & (2048-1)]
				oldnum = oldstate.number
		return msg, oldSnap, newSnap

	def deltaEntity(self, msg, frame, newnum, oldstate, unchanged):
		state = self.parseEntities[ self.parseEntitiesNum & (2048-1)]

		if(unchanged):
			state = oldstate
		else:
			msg, oldstate, state = self.parseDeltaEntity(msg, oldstate, state, newnum)

		if(state.number == (Q3_DemoParser.Q3_DEMOPARSER_MAX_GENTITIES-1)):
			return msg, frame, oldstate # entity was delta removed

		self.parseEntitiesNum+=1
		frame.NumEntities+=1
		return msg, frame, oldstate

	def readIntegerFromStream(self):
		data = self.fileHandler.read(4)
		return int.from_bytes(data, "little")
