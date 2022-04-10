import hexAdder as hA
import binascii

def hexIncrement(x):
	variables=[]
	hexOne = b'\x00\x01'
	
	variables.append(x)
	variables.append(hexOne)

	chunksBinascii=[]

	for item in variables:
		hexVariable = binascii.hexlify(item)
		chunksBinascii.append(hexVariable)

	
	x=chunksBinascii[0]
	y=chunksBinascii[1]

	incremented=hA.hexidecimalAddition(x, y)
	
	#print("After summing, the final value is : {}".format(incremented))
	
	if len(incremented[2:]) == 1:
		reformattedIncremented = '\\' + 'x00' + '\\' + 'x0{}'.format(incremented[2:])
		reformattedIncremented = bytes(reformattedIncremented, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')
		#print(reformattedIncremented)
		return reformattedIncremented
	
	elif len(incremented[2:]) == 2:
		reformattedIncremented = '\\' + 'x00' + '\\' + 'x{}'.format(incremented[2:])
		reformattedIncremented = bytes(reformattedIncremented, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')
		#print(reformattedIncremented)
		return reformattedIncremented
	
	elif len(incremented[2:]) == 3:
		reformattedIncremented = '\\' + 'x0{}'.format(incremented[2:][0]) + '\\' + 'x{}'.format(incremented[2:][1:])
		reformattedIncremented = bytes(reformattedIncremented, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')
		#print(reformattedIncremented)
		return reformattedIncremented

	elif len(incremented[2:]) == 4:
		reformattedIncremented = '\\' + 'x{}'.format(incremented[2:][:2]) + '\\' + 'x{}'.format(incremented[2:][2:])
		#print(reformattedIncremented)
		reformattedIncremented = bytes(reformattedIncremented, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')
		#print(reformattedIncremented)
		return reformattedIncremented
	



