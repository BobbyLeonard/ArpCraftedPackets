import binascii

def hexidecimalAddition(x,y):
	vals=[x,y]
	#print("Now adding: {}".format(vals))
	hexVals=[]
	for val in vals:
		hexadecimal_representation = int(val, 16)
		#print(hexadecimal_representation)
		hexadecimal_string = hex(hexadecimal_representation)
		#print(hexadecimal_string)
		hexVals.append(hexadecimal_string)
	#print("hexidecimalAddition Completed, returning...")
	return hex(int(hexVals[0],16) + int(hexVals[1],16))




