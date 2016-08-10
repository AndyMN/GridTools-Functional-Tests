from ProtocolTester import ProtocolTester


myProtocolTester = ProtocolTester()

client = "srmcp"
protocol = "srm"
local_file = "/scratch/jenkins/jenkins/workspace/robot-g2-tests/testfile"
remote_file = "/Users/kermit/testo"
host = "prometheus.desy.de"

myProtocolTester.copy_file(client=client, protocol=protocol, local_file=local_file, remote_file=remote_file, host=host)
print "OUTPUT: ", myProtocolTester.output
print "ERROR: ", myProtocolTester.error
print "RETURNCODE: ", myProtocolTester.returncode



