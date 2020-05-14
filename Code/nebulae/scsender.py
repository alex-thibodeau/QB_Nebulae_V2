# Courtesy of hecanjob/pippi.pd
import sys
import os
sys.path.insert(0, '/home/alarm/QB_Nebulae_V2/Code/nebulae/lib')

import socket
import scosc

class ScSend():
    values = { }
    serverhost = 'localhost'
    serverport = 3000
    serverip = None
    recvport = 3001
    socket = None
    timeout = 2
    connected = False

    def __init__(self):
        self.connect()

    def quit(self) :
            os.system('killall sclang jackd scsynth');
            sys.exit()

    def connect(self):
        print 'connecting to sc'
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
            self.connected = True
            self.serverip = socket.gethostbyname(self.serverhost)
            print 'Sending to SC on port ' + str(self.serverip) + " : " + str(self.serverport)

        except:
            print 'Connection failed - open SC'
            quit();


    def _send(self, bin):
        try:
            self.socket.sendto(bin, (self.serverip, self.serverport))
        except:
            print 'Could not send to SC. send_ failed'
            quit();

    def send(self, what, value):
        try:
            if what in self.values and self.values[what] == value :
                    return 

            self.values[what]=value
            oscmessage = scosc.OSC.OSCMessage()
            oscmessage.setAddress("/neb/"+what)
            oscmessage.append(value)
            self._send(oscmessage.getBinary())
        except:
            print 'Could not send to SC. Did you open a connection?'
            quit();

    def close(self):
        print 'Closing connection to SC'
        self.socket.close()
        self.connected = False

    def is_connected(self):
        return self.connected
