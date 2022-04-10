import socket
import binascii
import calculateChecksum as calChk
import incrementSequence as iSeq
import struct
import time

srcIP = "192.168.1.80"
dstIP = "8.8.8.8"
numberOfPings = 5


# https://www.binarytides.com/raw-socket-programming-in-python-linux/
# tell kernel not to put in headers, since we are providing it, when using IPPROTO_RAW this is not necessary
# s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

rawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
rawSocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)



ICMPseqNum = b'\x00\x00'

count = 0
while count < numberOfPings:
	#-----
	# IPv4 section

	ip_header16bit1 = b'\x45\x00' # Version, IHL, Type of Service 
	ip_header16bit2 = b'\x00\x1c' # Total Length

	ip_header16bit3 = b'\xab\xcd' # Identification 
	ip_header16bit4 = b'\x00\x00' # Flags, Fragment Offset

	ip_header16bit5 = b'\x40\x01' # TTL, Protocol 
	ip_header16bit6 = b'\x00\x00' # Header Checksum

	ip_header32bit1 = socket.inet_aton(srcIP) # Source Address
	ip_header32bit2 = socket.inet_aton(dstIP) # Destination Address

	ip_header16bit7 = ip_header32bit1[:2]
	ip_header16bit8 = ip_header32bit1[-2:]

	ip_header16bit9 = ip_header32bit2[:2]
	ip_header16bit10 = ip_header32bit2[-2:]


	chunks=[ip_header16bit1, ip_header16bit2, ip_header16bit3, ip_header16bit4, ip_header16bit5, ip_header16bit6, ip_header16bit7, ip_header16bit8, ip_header16bit9, ip_header16bit10]

	IPcalculatedChecksum = calChk.calculateCheckSum(chunks)
	IPcalculatedChecksum = '\\' + 'x{}'.format(IPcalculatedChecksum[2:][:2]) + '\\' + 'x{}'.format(IPcalculatedChecksum[2:][2:])

	# https://stackoverflow.com/questions/33257875/python-string-to-bytes-conversion-double-backslash-issue
	reformatedIPcalculatedChecksum = bytes(IPcalculatedChecksum, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')
	 

	#-----
	# ICMP section

	icmpHeader1 = b'\x08\x00' # ICMPtype | code
	icmpHeader2 = b'\x00\x00' # Checksum

	''' RFC792 = The checksum is the 16-bit ones's complement of the one's
		     complement sum of the ICMP message starting with the ICMP Type.
	      	     For computing the checksum , the checksum field should be zero.
	      	     This checksum may be replaced in the future.'''

	icmpHeader3 = b'\x12\x34' # Identifier
	icmpHeader4 = iSeq.hexIncrement(ICMPseqNum)
	ICMPseqNum=icmpHeader4

	
	#print("Calculated ICMP Seq number: {}".format(icmpHeader4))
	
	#print("ICMP Section:\n")

	chunks=[icmpHeader1, icmpHeader2, icmpHeader3, icmpHeader4]
	ICMPcalculatedChecksum = calChk.calculateCheckSum(chunks)
	ICMPcalculatedChecksum = '\\' + 'x{}'.format(ICMPcalculatedChecksum[2:][:2]) + '\\' + 'x{}'.format(ICMPcalculatedChecksum[2:][2:])

	# https://stackoverflow.com/questions/33257875/python-string-to-bytes-conversion-double-backslash-issue
	reformatedICMPcalculatedChecksum = bytes(ICMPcalculatedChecksum, "UTF-8").decode('unicode-escape').encode('ISO-8859-1')


	#-----
	# Build and send packet

	packet = struct.pack("!2s2s2s2s2s2s2s2s2s2s2s2s2s2s", ip_header16bit1, ip_header16bit2, ip_header16bit3, ip_header16bit4, 
						ip_header16bit5, reformatedIPcalculatedChecksum, ip_header16bit7, ip_header16bit8, ip_header16bit9, 
						ip_header16bit10, icmpHeader1, reformatedICMPcalculatedChecksum, icmpHeader3, icmpHeader4)

	#print(packet)

	rawSocket.sendto(packet, (dstIP, 0))
	print("Ping Sent...")
	
	count+=1
	time.sleep(1)

rawSocket.close()