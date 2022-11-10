from PlayerState import Q3_PlayerState
from EntityState import Q3_EntityState

class Q3_Snapshot:
	def __init__(self):
		self.Ps = Q3_PlayerState() # complete information about the current player at this time
		self.Valid = None			# cleared if delta parsing was invalid
		self.SnapFlags = None		# rate delayed and dropped commands
		self.ServerTime = None		# server time the message is valid for (in msec)

		self.MessageNum = 0		# copied from netchan->incoming_sequence
		self.DeltaNum = None		# messageNum the delta is from
		self.Ping = None			# time from when cmdNum-1 was sent to time packet was reeceived
		self.Areamask = None		# portalarea visibility bits (MAX_MAP_AREA_BYTES)

		self.CmdNum = None			# the next cmdNum the server is expecting				

		self.NumEntities = None			# all of the entities that need to be presented
		self.ParseEntitiesNum = None		# at the time of this snapshot

		self.ServerCommandNum = None		# execute all commands up to this before
										# making the snapshot current
