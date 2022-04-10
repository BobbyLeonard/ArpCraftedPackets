import binascii
import hexAdder as hA


def calculateCheckSum(chunks):
	finalX=binascii.hexlify(b'\x00\x00')

	chunksBinascii=[]

	for item in chunks:
		hexVariable = binascii.hexlify(item)
		chunksBinascii.append(hexVariable)

	#print(chunksBinascii)

	for item in chunksBinascii:
		x=finalX
		y=item
		finalX=hA.hexidecimalAddition(x, y)
		#print("Current FinalX value: {}".format(finalX))
		

	
	#print("After summing, the final value is : {}".format(finalX))


	if len(finalX[2:]) > 4:
		#print("Too big need to carry over")
		baseAnswer=hex(int(finalX[-4:], 16))
		carryOver=hex(int(finalX[2:-4], 16))
		#print("Base Answer: {}".format(baseAnswer))
		#print("Carry Over: {}".format(carryOver))
		finalAnswerWithCarry=hex(int(baseAnswer, 16) + int(carryOver, 16))
		#print("Final Answer with carry: {}".format(finalAnswerWithCarry))

		onesComplement = binascii.hexlify(b'\xff\xff')
		onesComplement = hex(int(onesComplement, 16) - int(baseAnswer, 16))
		#print("onesComplement, wrong by +2 : {}".format(onesComplement))
		onesComplementCorrected = hex(int(onesComplement, 16) - int(carryOver, 16))
		#print("onesComplementCorrected (- carryOver) : {}".format(onesComplementCorrected))
		
		checkSumValue = onesComplementCorrected
		return checkSumValue

	else:
		checkSumValue = finalX
		onesComplement = binascii.hexlify(b'\xff\xff')
		onesComplement = hex(int(onesComplement, 16) - int(checkSumValue, 16))
		checkSumValue = onesComplement
		#print("checkSumValue in else section, no carries: {}".format(checkSumValue)) 	
		return checkSumValue
