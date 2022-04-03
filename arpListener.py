import socket
from datetime import timezone
import datetime

import decodeResponse as dc

logFile='arpCaptured.log'

def writeLogs(stringToWrite):
	with open(logFile,'a+') as f: 
		f.write(stringToWrite) 


setProtocol = 0x0806
ETH_FRAME_LEN = 1514  
interface = 'wlp2s0'

try:
	with socket.socket(socket.PF_PACKET, socket.SOCK_RAW, setProtocol) as rawSocket:
		rawSocket.bind((interface, setProtocol))
		while True:
			data = rawSocket.recv(ETH_FRAME_LEN)
			if not data:
		  		break
			d=dc.unpackResponse(data)
			outstring = str(datetime.datetime.now(timezone.utc))
			outstring=outstring+" --- "
			#print("UTC Timestamp {}".format(datetime.datetime.now(timezone.utc)))
			for key,item in d.items():
				#print(key, item)
				outstring=outstring+'{}={}, '.format(key, item)
			print(outstring[:-2])
			writeLogs(outstring[:-2] + '\n') 
			

except Exception as e:
	print(e)
