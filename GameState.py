class Q3_GameState:
	def __init__(self):
		self.ServerMessageSequence = None
		self.ReliableAcknowledge = None
		self.ReliableSequence = 0
		self.ServerCommandSequence = None
		self.ClientNum = None
		self.ChecksumFeed = None

		self.ServerCommands = []
		self.SnapShot = ""
		self.SnapShots = []
		self.NewSnapShots = None
		self.ConfigStrings = []

		self.EntityBaseLines = None
		self.ParseEntities = None
