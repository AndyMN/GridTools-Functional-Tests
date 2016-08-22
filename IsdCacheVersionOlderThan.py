import sys
import subprocess
import os


def get_versions(version_string):

    version_splits = version_string.split(".")

    major_version = version_splits[0]
    minor_version = version_splits[1]

    return int(major_version), int(minor_version)



version_compare = str(sys.argv[1])

major_version_compare, minor_version_compare = get_versions(version_compare)



# Find dCache version of system under test
process = subprocess.Popen("curl -D- -s http://" + os.environ.get('DFTS_SUT') + ":" + os.environ.get('HTTP_PORT') + "/ |grep Serv", shell=True, stdout=subprocess.PIPE)

output, error = process.communicate()

system_version = ""
slash_before_version = output.find("/")
if slash_before_version > 0:
    dash_after_version = output.find("-")
    if dash_after_version > 0:
        system_version = output[slash_before_version + 1:dash_after_version]
    else:
        system_version = output[slash_before_version + 1:]
else:
    system_version = "2.10"


major_version_system, minor_version_system = get_versions(system_version)


if major_version_system < major_version_compare:
    print "true"
elif major_version_system > major_version_compare:
    print "false"
elif major_version_system == major_version_compare and minor_version_system < minor_version_compare:
    print "true"
else:
    print "false"




