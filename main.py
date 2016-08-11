from ProtocolTesterLib import ProtocolTesterLib


myProtocolTester = ProtocolTesterLib()

client = "srmcp"
protocol = "srm"
local_file = "/scratch/jenkins/jenkins/workspace/robot-g2-tests/testfile"
remote_file = "/Users/kermit/testo"
host = "prometheus.desy.de"



myProtocolTester.set_client(client)
myProtocolTester.set_host(host)
myProtocolTester.set_protocol(protocol=protocol)

myProtocolTester.copy_local_file(local_file=local_file, remote_file=remote_file)
print "OUTPUT: ", myProtocolTester.output
print "ERROR: ", myProtocolTester.error
print "RETURNCODE: ", myProtocolTester.returncode

myProtocolTester.remove_remote_file(remote_file=remote_file)
print "OUTPUT: ", myProtocolTester.output
print "ERROR: ", myProtocolTester.error
print "RETURNCODE: ", myProtocolTester.returncode



