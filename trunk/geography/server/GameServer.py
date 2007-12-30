#from twisted.spread import pb
from GameData import GameData
from Landmark import Landmark
import socket
import pickle
import threading

class Request:
    def __init__(self, method, arguments):
        self.method = method
        self.arguments = arguments
        
class Player:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.score = 0
        

class GameServer:
    def __init__(self):
        HOST = ''                 # Symbolic name meaning the local host
        PORT = 8387               # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print 'listening'
        self.gameData = GameData()
        self.methods = {'getLandmarks':self.getLandmarks,
                        'addScore':self.addScore,
                        'startMultiplayerGame':self.startMultiplayerGame,
                        'addMultiplayerScore':self.addMultiplayerScore,
                    }
        self.player1 = None
        self.player2 = None
        
        while True:
            print 'while true'
            conn, addr = s.accept()
            print 'Connected by', addr
            request = conn.recv(1024)
            if not request: break
            methodString, argument = request.split(',')
            method = self.methods[methodString]
            method(argument, conn)
                
        
    def getLandmarks(self, difficulty, conn):        
        landmarks = self.gameData.getLandmarks(difficulty)
        landmarks = pickle.dumps(landmarks)
        data = 'yes@%s$' % landmarks
        print conn.sendall(data)
    
    def addScore(self, score, conn):
        self.gameData.addScore(score)
        scores = 'no@%s' % self.gameData.getScores()
        conn.send(scores)
    
    def startMultiplayerGame(self, player, conn):
        name, address = player.split('$')
        if self.player1 == None:
            self.player1 = Player(name, address)
            player2Server = Player2Server(self)
            player2Server.start()
            return '%s has joined the game, now waiting for a second player' % name
        if self.player2 == None:
            self.player2 = Player(name, address)
            
    def gotPlayer2(self):
        pass
            
    def addMultiplayerScore(self, score):
        pass
        
class Player2Server(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self._stopEvent = threading.Event()
        self.socket = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8388))
        self.socket.listen(1)
        self.server = server
    def run(self):
        while not self._stopEvent.isSet():
            conn, addr = self.socket.accept()
            print 'Connected by', addr
            request = conn.recv(1024)
            self.connection = request
            self.server.gotPlayer2(request)

"""class GameServer:
    def __init__(self):
        self.gameData = GameData()
        
    def start(self):
        #create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host, 
        # and a well-known port
        serversocket.bind(('', 8387))
        #become a server socket
        serversocket.listen(5)
        self.methods = {'getLandmarks':self.getLandmarks,}
        
        while True:
            #accept connections from outside
            (clientsocket, address) = serversocket.accept()
            print address
            request = serversocket.recv(1024)
            print request
            #method = self.methods[request]
            #data = method('easy')
            #print data
            #serversocket.send(data)

    def getLandmarks(self, difficulty):
        return self.gameData.getLandmarks(difficulty)"""

"""class GamePerspective(pb.Root):
    def __init__(self, gameData):
        self.gameData = gameData
        
    def remote_getScores(self):
        return self.gameData.getData()
    
    def remote_getLandmarks(self, difficulty):
        return self.gameData.getLandmarks(difficulty)
    
    def remote_addScore(self, score):
        self.gameData.addScore(score)"""

"""if __name__ == "__main__":
    #import sys
    #from twisted.internet import reactor
    #gameData = GameData()
    #gamePerspective = GamePerspective(gameData)
    #reactor.listenTCP(8387, pb.PBServerFactory(gamePerspective))
    #reactor.run()
    server = GameServer()
    server.start()"""
if __name__ == "__main__":
    g = GameServer()