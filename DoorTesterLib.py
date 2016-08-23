import socket


class DoorTesterLib:
    """
    Library that tests if a port is open for a given host.

    Initialize this library in robot with a host (Ex: Library  DoorTesterLib.py   prometheus.desy.de)
    """

    def __init__(self, host="prometheus.desy.de"):
        """
        Will initialize an instance of the Door Tester for the given host.

        :param host: The remote dcache hostname (Ex: prometheus.desy.de, reference-2-13.desy.de, etc.)

        :return:
        """

        self.host = host

    def test_protocol_door(self, protocol, port):
        """
        Tries to connect to the given port.

        Throws a RuntimeError if it can't connect to the port.

        :param protocol: Protocol string, only used for output. Doesn't actually do anything.

        :param port: Port that should be open on the given host.

        :return: /
        """
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

