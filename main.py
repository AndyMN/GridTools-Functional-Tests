import subprocess
import time

timey = time.time()
print int(timey)

command = "srmcp file:///scratch/jenkins/jenkins/workspace/robot-g2-tests/testfile srm://prometheus.desy.de:8443/Users/kermit/testfile" + str(timey)


proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output, err = proc.communicate()
proc.wait()
print proc.returncode
print "OUTPUT: ", output
print "ERROR: ", err


