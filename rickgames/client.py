import socket
import json

def attack(sock, playerId, targetId):
    message = json.dumps({
        'requestType' : 'attack',
        'targetId': targetId,
        'playerId': playerId
    })
    sendMsg(sock, message)

def getInfo(sock):
    message = json.dumps({
        'requestType' : 'playerData'
    })
    data = sendMsg(sock, message)
    return json.loads(data)

def sendMsg(sock, message):
    print('sending "%s"' % message)
    sock.sendall(bytes(message, 'UTF-8'))

    data = sock.recv(2048)
    result = data.decode("utf-8")
    print('received "%s"' % result)

    return result

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    info = getInfo(sock)
    for key in info.keys():
        attack(sock, int(key), 0)
finally:
    sock.close()