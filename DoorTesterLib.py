import socket


class DoorTesterLib:

    def __init__(self, host):
        self.host = host

    def test_protocol_door(self, protocol, port):
        print "Testing port, not protocol ! Protocol is just an added string !"
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            test_socket.connect((self.host, int(port)))
            print "Protocol: ", protocol
            print "Port: ", str(port)
            test_socket.close()
        except:
            print "Protocol: ", protocol
            print "Port: ", str(port)
            print "Not open !"
            raise RuntimeError("Socket couldn't connect to Port: " + str(port))

