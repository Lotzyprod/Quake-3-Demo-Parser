class Q3_ServerCommand:
		def __init__(self, cmd, seq):
			self.Command = ""
			self.Message = ""
			self.parseCmd(cmd)
			self.SequenceNumber = seq

		def parseCmd(self,cmd):
			property = ['Command', 'Message']
			propertyNum = 0

			for i in range(len(cmd)):
				val = ord(cmd[i])
				if val == 34:
					if(propertyNum == 0):
						self.Command = self.Command[0: -1]
						propertyNum+=1
				elif val == 10:
					property[propertyNum] += "\\n"

				elif val ==13:
					property[propertyNum] += "\\r"

				elif val ==9:
					property[propertyNum] += "\\t"
				elif(val >= 32 and val <= 126):
					property[propertyNum] += cmd[i]