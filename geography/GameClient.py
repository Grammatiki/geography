import socket
import pickle
#from server.Landmark import Landmark

class GameClient:
    def __init__(self):
        self.HOST = 'localhost'    # The remote host
        self.PORT = 8387           # The same port as used by the server
        
        
    def getLandmarks(self, keyword):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.send('getLandmarks,%s' % keyword)
        data = self.recv_end(s)
        data = self._splitData(data)
        return data
    
    def addScore(self, score):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.send('addScore,%s' % score)
        data = s.recv(4096)
        data = self._splitData(data)
        s.close()
        return data
    
    def startMultiplayer(self, name):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.send('startMultiplayerGame%s' % name)
        s.recv(1024)
        
                
    
    def _splitData(self, data):
        pkl, data = data.split('@')
        if pkl == 'yes':
            data = pickle.loads(data)
        return data
    

    def recv_end(self, the_socket):
        End='$'
        total_data=[];data=''
        while True:
            data=the_socket.recv(8192)
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
        return ''.join(total_data)



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
