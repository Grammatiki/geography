import socket
import pickle
#from server.Landmark import Landmark

class GameClient:
    def __init__(self):
        self.HOST = 'localhost'    # The remote host
        self.PORT = 8387           # The same port as used by the server
        
        
    def getLandmarks(self, difficulty):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.send('getLandmarks,%s' % difficulty)
        data = self.s.recv(8129)
        data = self._splitData(data)
        return data
    
    def addScore(self, score):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.send('addScore,%s' % score)
        data = self.s.recv(8129)
        data = self._splitData(data)
        self.s.close()
        return data
    
    def startMultiplayer(self, name):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.send('startMultiplayerGame%s' % name)
        self.s.recv(1024)
        
                
    
    def _splitData(self, data):
        pkl, data = data.split('@')
        if pkl == 'yes':
            data = pickle.loads(data)
        return data



"""class GameClient():
    def __init__(self):
        pass
        
    def getLandmarks(self, difficulty):
        #create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #now connect to the web server on port 80 
        # - the normal http port
        self.s.connect(("localhost", 8387))
        self.s.send('getLandmarks')
        landmarks =  self.s.recv(8192)
        print landmarks
        #landmarks = pickle.loads(landmarks)
        #return landmarks
   """     
        
        


"""class GameClient(object):
    def __init__(self):
        self.scores = None
        self.data = None
        self.factory = ReconnectingPBClientFactory()

    def connect(self):        
        reactor.connectTCP("localhost", 8387, self.factory)
        print dir(self.factory)
        #return self.factory.getRootObject().addCallback(self._connected)

    def _connected(self, rootObj):
        print rootObj
        self.data = rootObj

    def getLandmarks(self, difficulty):
        if self.data == None:
            self.data = self.factory.data
        return self.data.callRemote('getLandmarks', difficulty).addCallback(
            self._gotLandMarks)
    
    def _gotLandMarks(self, landmarks):
        self.landmarks = landmarks
        print "Got landmarks", landmarks
        
    def getScores(self):
        print "Getting scores..."
        return self.data.callRemote('getScores').addCallback(
            self._gotScores)
    
    def _gotScores(self, scores):
        self.listOfScores = scores
        print "Got scores:", scores
        
    def addScore(self, score):
        return self.data.callRemote('addScore', score)

    def _catchFailure(self, failure):
        print "Error:", failure.getErrorMessage()"""

if __name__ == '__main__':
    g = GameClient()
    g.getLandmarks('easy')

#t = GameClient()
#t.getInfo()
#reactor.run()
