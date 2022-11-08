from Trajectory import Q3_Trajectory

class Q3_EntityState:
	def __init__(self):
		self.pos = Q3_Trajectory() # for calculating position
		self.apos = Q3_Trajectory() # for calculating angles

		self.origin = [0,0,0] # vec3_t
		self.origin2 = [0,0,0] # vec3_t

		self.angles = [0,0,0] # vec3_t
		self.angles2 = [0,0,0] # vec3_t
		
		self.number = 0			# entity index
		self.eType = None			# entityType_t
		self.eFlags = None
		
		self.time = None
		self.time2 = None

		self.otherEntityNum = None	# shotgun sources, etc
		self.otherEntityNum2 = None

		self.groundEntityNum = None	# -1 = in air

		self.constantLight = None	# r + (g<<8) + (b<<16) + (intensity<<24)
		self.loopSound = None		# constantly loop this sound

		self.modelindex = None
		self.modelindex2 = None
		self.clientNum = None		# 0 to (MAX_CLIENTS - 1], for players and corpses
		self.frame = None

		self.solid = None			# for client side prediction, trap_linkentity sets this properly

		self.event = None			# impulse events -- muzzle flashes, footsteps, etc
		self.eventParm = None

		# for players
		self.powerups = None		# bit flags
		self.weapon = None			# determines weapon and flash model, etc
		self.legsAnim = None		# mask off ANIM_TOGGLEBIT
		self.torsoAnim = None		# mask off ANIM_TOGGLEBIT

		self.generic1 = None

	# magic dont touch!!!
	# count of bits for every netField from enitityState_t (quake3)
	NetFields = [
		['pos.trTime', 32 ],
		['pos.trBase[0]', 0 ],
		['pos.trBase[1]', 0 ],
		['pos.trDelta[0]', 0 ],
		['pos.trDelta[1]', 0 ],
		['pos.trBase[2]', 0 ],
		['apos.trBase[1]', 0 ],
		['pos.trDelta[2]', 0 ],
		['apos.trBase[0]', 0 ],
		['event', 10 ],
		['angles2[1]', 0 ],
		['eType', 8 ],
		['torsoAnim', 8 ],
		['eventParm', 8 ],
		['legsAnim', 8 ],
		['groundEntityNum', 10 ],
		['pos.trType', 8 ],
		['eFlags', 19 ],
		['otherEntityNum', 10 ],
		['weapon', 8 ],
		['clientNum', 8 ],
		['angles[1]', 0 ],
		['pos.trDuration', 32 ],
		['apos.trType', 8 ],
		['origin[0]', 0 ],
		['origin[1]', 0 ],
		['origin[2]', 0 ],
		['solid', 24 ],
		['powerups', 16 ],
		['modelindex', 8 ],
		['otherEntityNum2', 10 ],
		['loopSound', 8 ],
		['generic1', 8 ],
		['origin2[2]', 0 ],
		['origin2[0]', 0 ],
		['origin2[1]', 0 ],
		['modelindex2', 8 ],
		['angles[0]', 0 ],
		['time', 32 ],
		['apos.trTime', 32 ],
		['apos.trDuration', 32 ],
		['apos.trBase[2]', 0 ],
		['apos.trDelta[0]', 0 ],
		['apos.trDelta[1]', 0 ],
		['apos.trDelta[2]', 0 ],
		['time2', 32 ],
		['angles[2]', 0 ],
		['angles2[0]', 0 ],
		['angles2[2]', 0 ],
		['constantLight', 32 ],
		['frame', 16 ]
	]
 
