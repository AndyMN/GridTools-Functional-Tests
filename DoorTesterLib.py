import socket


class DoorTesterLib:

    def __init__(self, host):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.host = host

    def test_protocol_door(self, protocol, port):
        print "Testing port, not protocol ! Protocol is just an added string !"
        try:
            self.socket.connect((self.host, int(port)))
            print "Protocol: ", protocol
            print "Port: ", str(port)
        except self.socket.error as e:
            print "Protocol: ", protocol
            print e
