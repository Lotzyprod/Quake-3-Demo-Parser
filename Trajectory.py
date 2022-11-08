class Q3_Trajectory:
	def __init__(self):
		self.trBase = [0,0,0] # vec3_t
		self.trDelta = [0,0,0] # velocity, etc (vec3_t)
		self.trType = None
		self.trTime = None
		self.trDuration = None	# if non 0, trTime + trDuration = stop time