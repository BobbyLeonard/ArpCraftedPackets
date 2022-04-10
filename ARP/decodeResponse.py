import struct
import binascii

def addSemiColons(extractedField):
	extractedField=binascii.hexlify(extractedField).decode('UTF-8')
	returnItem = ':'.join(format(s, '02x') for s in bytes.fromhex(extractedField))
	return returnItem

def convertToIPaddr(extractedField):
	extractedField=binascii.hexlify(extractedField).decode('UTF-8')
	dottedFormat = '.'.join(format(s, '02x') for s in bytes.fromhex(extractedField))
	octetList=[]
	for octet in dottedFormat.split('.'):
		octetList.append(octet)
	returnItem=""	
	for octet in octetList:
		returnItem= returnItem + str(int(octet, 16)) + '.'
	return returnItem[:-1]

def unpackResponse(response):

	eth_hdr = struct.unpack("!6s6s2s", response[0:14])
	hw_type = struct.unpack("!2s", response[14:16]) 
	prot_type = struct.unpack("!2s", response[16:18])  
	hw_size = struct.unpack("!1s", response[18:19])
	prot_size = struct.unpack("!1s", response[19:20])
	op_code = struct.unpack("!2s", response[20:22])
	send_mac = struct.unpack("!6s", response[22:28])
	send_ip = struct.unpack("!4s", response[28:32])
	tgt_mac = struct.unpack("!6s", response[32:38])
	tgt_ip = struct.unpack("!4s", response[-4:])

	d=dict()

	d['dstMac']=addSemiColons(eth_hdr[0])
	d['srcMac']=addSemiColons(eth_hdr[1])
	d['proto']=addSemiColons(eth_hdr[2])
	d['hardwareType']=addSemiColons(hw_type[0])
	d['protoType']=addSemiColons(prot_type[0])
	d['hardwareSize']=addSemiColons(hw_size[0])
	d['protoSize']=addSemiColons(prot_size[0])
	d['opcode']=addSemiColons(op_code[0])
	d['senderMac']=addSemiColons(send_mac[0])
	d['senderIP']=convertToIPaddr(tgt_ip[0])
	d['targetMac']=addSemiColons(tgt_mac[0])
	d['targetIP']=convertToIPaddr(tgt_ip[0])

	return d


