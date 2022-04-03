#!/usr/bin/python3

import socket
import struct
import time

setProtocol = 0x0806

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, setProtocol)

rawSocket.bind(("wlp2s0", setProtocol))


#ARP request:
#------------
dstMac = b'\xff\xff\xff\xff\xff\xff'
#dstMac = b'\xb8\x27\xeb\xc0\x5d\xae'
srcMac = b'\xd8\xf3\xbc\x6f\x94\xe9'
proto  = b'\x08\x06'
hardwareType = b'\x00\x01'
protoType = b'\x08\x00'
hardwareSize = b'\x06'
protoSize = b'\x04'
opcode = b'\x00\x01'
senderMac = srcMac
senderIP = b'\xc0\xa8\x01\x50'
targetMac = b'\x00\x00\x00\x00\x00\x00'
targetIP = b'\xc0\xa8\x01\x1e'
#padding = b'\x00\x00\x00\x00'


packet = struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s", dstMac, srcMac, proto, hardwareType, protoType, hardwareSize, protoSize, opcode, senderMac, senderIP, targetMac, targetIP)

print(packet)

rawSocket.send(packet)

time.sleep(1)
rawSocket.close()


