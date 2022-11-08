class Q3_PlayerState:
	# magic dont touch!!!
	# count of bits for every netField from playerState_t (quake3)
	NetFields = [
		['CommandTime', 32 ],
		['Origin[0]', 0 ],
		['Origin[1]', 0 ],
		['BobCycle', 8 ],
		['Velocity[0]', 0 ],
		['Velocity[1]', 0 ],
		['ViewAngles[1]', 0 ],
		['ViewAngles[0]', 0 ],
		['WeaponTime', -16 ],
		['Origin[2]', 0 ],
		['Velocity[2]', 0 ],
		['LegsTimer', 8 ],
		['PmTime', -16 ],
		['EventSequence', 16 ],
		['TorsoAnim', 8 ],
		['MovementDir', 4 ],
		['Events[0]', 8 ],
		['LegsAnim', 8 ],
		['Events[1]', 8 ],
		['PmFlags', 16 ],
		['GroundEntityNum', 10 ],
		['Weaponstate', 4 ],
		['eFlags', 16 ],
		['ExternalEvent', 10 ],
		['Gravity', 16 ],
		['Speed', 16 ],
		['DeltaAngles[1]', 16 ],
		['ExternalEventParm', 8 ],
		['ViewHeight', -8 ],
		['DamageEvent', 8 ],
		['DamageYaw', 8 ],
		['DamagePitch', 8 ],
		['DamageCount', 8 ],
		['Generic1', 8 ],
		['PmType', 8 ],
		['DeltaAngles[0]', 16 ],
		['DeltaAngles[2]', 16 ],
		['TorsoTimer', 12 ],
		['EventParms[0]', 8 ],
		['EventParms[1]', 8 ],
		['ClientNum', 8 ],
		['Weapon', 5 ],
		['ViewAngles[2]', 0 ],
		['GrapplePoint[0]', 0 ],
		['GrapplePoint[1]', 0 ],
		['GrapplePoint[2]', 0 ],
		['JumpPadEnt', 10 ],
		['LoopSound', 16 ]
	]

	def __init__(self):
		self.CommandTime = None	# cmd->serverTime of last executed command
		self.PmType = None
		self.BobCycle = None		# for view bobbing and footstep generation
		self.PmFlags = None		# ducked, jump_held, etc
		self.PmTime = None

		self.Origin = [0,0,0] # vec3_t
		self.Velocity = [0,0,0] # vec3_t

		self.WeaponTime = None
		self.Gravity = None
		self.Speed = None
		self.DeltaAngles = [0,0,0]	# add to command angles to get view direction (length 3)
									# changed by spawns, rotating objects, and teleporters

		self.GroundEntityNum = None# ENTITYNUM_NONE = in air

		self.LegsTimer = None		# don't change low priority animations until this runs out
		self.LegsAnim = None		# mask off ANIM_TOGGLEBIT

		self.TorsoTimer = None		# don't change low priority animations until this runs out
		self.TorsoAnim = None		# mask off ANIM_TOGGLEBIT

		self.MovementDir = None	# a number 0 to 7 that represents the reletive angle
								# of movement to the view angle (axial and diagonals)
								# when at rest, the value will remain unchanged
								# used to twist the legs during strafing

		self.GrapplePoint = [0,0,0]	# location of grapple to pull towards if PMF_GRAPPLE_PULL (vec3_t)

		self.eFlags = None			# copied to entityState_t->eFlags

		self.EventSequence = None	# pmove generated events
		self.Events = [0,0,0]
		self.EventParms = [0,0,0]

		self.ExternalEvent = None	# events set on player from another source
		self.ExternalEventParm = None
		self.ExternalEventTime = None

		self.ClientNum = None		# ranges from 0 to MAX_CLIENTS-1
		self.Weapon = None			# copied to entityState_t->weapon
		self.Weaponstate = None

		self.ViewAngles = [0,0,0]		# for fixed views (vec3_t)
		self.ViewHeight = None

		# damage feedback
		self.DamageEvent = None	# when it changes, latch the other parms
		self.DamageYaw = None
		self.DamagePitch = None
		self.DamageCount = None

		self.Stats = []
		self.Persistant = []	# stats that aren't cleared on death
		self.Powerups = []	# level.time that the powerup runs out
		self.Ammo = []

		self.Generic1 = None
		self.LoopSound = None
		self.JumpPadEnt = None	# jumppad entity hit this frame

		# not communicated over the net at all
		self.Ping = None			# server to game info for scoreboard
		self.PmoveFrameCount = None	# FIXME: don't transmit over the network
		self.JumpPadFrame = None
		self.EntityEventSequence = None
		

		

		
