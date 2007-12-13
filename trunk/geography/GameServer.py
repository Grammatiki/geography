from twisted.internet.protocol import Protocol, ClientCreator, Factory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class PingResponder(Protocol):
    buf = ''
    def dataReceived(self, data):
        self.buf += data
        if self.buf == 'PING':
            print 'PONGED!'
            self.transport.write('PONG')
            self.transport.loseConnection()

class PingSender(Protocol):
    def __init__(self):
        self.buf = ''
        
    def connectionMade(self):
        self.transport.write('PING')
        
    def dataReceived(self, data):
        self.buf += data
    def connectionLost(self, reason):
        print "PONGED WITH: " +self.buf

def client():
    ps = PingSender
    cc = ClientCreator(reactor, ps)
    def dontDelay():
        cc.connectTCP('sabeto', 4321)
    lc = LoopingCall(dontDelay)
    lc.start(0.5)


def server():
    pf = Factory()
    pf.protocol = PingResponder
    svr = reactor.listenTCP(4321, pf)

import sys
if sys.argv[1] == 'client':
    client()
else:
    server()

reactor.run()