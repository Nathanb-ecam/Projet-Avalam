#produire une connexion TCP qui envoie du json

import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket.socket(IPv4, TCP)


try:
	s.connect(('localhost',3001)) 
	#envoi du json d'inscription
	data = {
	"matricules": ["18092"],
	"port": 8080,
	"name": " AI Bot "
}
	# boucle d'envoi 
	msg = json.dumps(data).encode('utf8')
	total = 0
	while total < len(msg):
		sent = s.send(msg[total:])
		total += sent
except Exception as e:
	print(e)
finally:
    s.close()