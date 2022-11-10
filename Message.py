from Decompressor import Q3_Huffman_Decompressor

class Q3_Message:
	def __init__(self,len):
		self.huffman = Q3_Huffman_Decompressor.create()
		self.MaxSize = len
		self.Data = ""
		self.CurSize = 0
		self.ReadCount = 0
		self.Bit = 0

	def setData(self,data):
		self.Data = data

	def ReadBits(self,bits):
		sgn = False
		value = 0;

		if(bits < 0):
			bits = -bits
			sgn = True

		nbits = 0
		if(bits&7):
			nbits = bits&7
			for i in range(nbits):
				res, self.Data, self.Bit = Q3_Huffman_Decompressor.GetBit(self.Data, self.Bit)
				value |= (res<<i)
			bits -= nbits
		
		if (bits):
			for i in range(0,bits,8):
				get,self.Data,self.Bit = self.huffman.OffsetReceive(self.Data, self.Bit)
				
				value |= (get<<(i+nbits))

		self.ReadCount = (self.Bit>>3)+1

		if ( sgn ):
			if ( value & ( 1 << ( bits - 1 ) ) ):
				value |= -1 ^ ( ( 1 << bits ) - 1 )
		return value

	def ReadBigString(self):
		maxLen = 8192
		curLen = 0
		data = ""

		for i in range(8192):
			byte = self.ReadByte()
			if(byte == -1 or byte == 0):
				break

			# translate all fmt spec to avoid crash bugs (c++)
			if(byte == '%'):
				byte = ord(".")

			data += chr(byte)

		return data

	def ReadString(self):
		maxLen = 1024
		curLen = 0
		data = ""

		for i in range(1024):
			byte = self.ReadByte()
			if(byte == -1 or byte == 0):
				break

			# translate all fmt spec to avoid crash bugs (c++)
			if(byte == '%'):
				byte = ord(".");

			# don't allow higher ascii values
			if(byte > 127):
				byte = ord(".")
			data += chr(byte)

		return data

	def ReadData(self,len):
		data = []
		for i in range(len):
			data.append(int(self.ReadByte()))
		return data

	def ReadLong(self):
		return self.Read(32)
	def ReadShort(self):
		return self.Read(16)
	def ReadByte(self):
		return self.Read(8)

	def Read(self,bits):
		c = self.ReadBits(bits)

		if(self.ReadCount > self.CurSize):
			c = -1

		return c