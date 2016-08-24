from flask import Flask, jsonify, request, json, render_template, send_from_directory
import random
import socket
import threading
app = Flask(__name__)


lastMsg = 'no message yet'

def createPlayer(name):
    return {
        'name' : name,
        'attack' : random.randint(3,5),
        'defense' : random.randint(1,2),
        'health' : random.randint(15,20)
    }

ids = {
    0 : createPlayer('Bob'),
    1 : createPlayer('Tim'),
    2 : createPlayer('Sue'),
    3 : createPlayer('Joe'),
}

def startSocket():
    global lastMsg
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print ('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()


        try:
            print ('connection from', client_address)

            while True:
                msg = connection.recv(2048)
                if msg:
                    lastMsg = msg.decode("utf-8")
                    data = json.loads(lastMsg)
                    requestType = data['requestType']
                    if requestType == 'attack':
                        result = attack(data['playerId'], data['targetId'])
                    elif requestType == 'playerData':
                        result = json.dumps(ids)
                    else:
                        result = 'invalid request'
                    print('received "%s"' % lastMsg)
                    connection.sendall(bytes(result, 'UTF-8'))
                else:
                    break
        finally:
            connection.close()

@app.route('/attack/<int:playerId>/<int:targetId>')
def attack_web(playerId, targetId):
    global lastMsg
    msg = attack(playerId, targetId)
    lastMsg = msg
    return render_template('browse.html', msg=msg)

def attack(playerId, targetId):

    if (playerId == targetId):
        return "Players can't attack themselves"

    global ids
    player, target = ids[playerId]['name'], ids[targetId]['name']
    playerHp, targetHp = ids[playerId]['health'], ids[targetId]['health']

    if (playerHp <= 0):
        return "%s cannot attack... oh you know he ded." % player

    msg = "%s attacked %s" % (player, target)

    if (targetHp <= 0):
        return msg + ", but %s is already dead." % (target)
    attack, defense = ids[playerId]['attack'], ids[targetId]['defense']

    attack = random.randint(1,attack)
    defense = random.randint(0,defense)
    dmgDone = attack - defense
    result = targetHp - dmgDone
    ids[targetId]['health'] = result

    if attack <= 0:
        return msg + " and missed."

    if result <= 0:
        return msg + " for %d and %d was defended. %s died" % (attack, defense, target)
    return msg + " for %d and %d was defended" % (attack, defense)

@app.route('/info')
def info(playerId=None):
    playerId = request.args.get('player', None)
    if (playerId is None):
        msg = ids
    else:
        msg = ids[int(playerId)]

    return render_template('browse.html', msg=msg)

@app.route('/')
def lastMessage():
    return render_template('browse.html', msg=lastMsg)

@app.route('/<dir>/<imgName>')
def showImage(dir, imgName):
    return send_from_directory(dir, imgName)

if __name__ == '__main__':
    t = threading.Thread(target=startSocket)
    t.start()
    app.run(host='0.0.0.0', port=8082)