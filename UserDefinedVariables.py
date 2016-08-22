import os

PROTOCOL_PORTS = {"srm": os.environ.get('SRM_PORT'), "gsidcap": os.environ.get('GSIDCAP_PORT'), "gsiftp": os.environ.get('GSIFTP_PORT'), "http": os.environ.get('HTTP_PORT'), "dcap": os.environ.get('DCAP_PORT')}


#HOST = "prometheus.desy.de"
#HOST = "reference-2-13.desy.de"
HOST = os.environ.get('DFTS_SUT')

LOCAL_DIR = "/scratch/jenkins/jenkins/workspace/robot-g2-tests/"
LOCAL_FILE = LOCAL_DIR + "testfile"

#REMOTE_DIR = "/Users/kermit/"
#REMOTE_DIR = "/data/g2/"
REMOTE_DIR = os.environ.get('REMOTE_DIR')
REMOTE_FILE = REMOTE_DIR + "testo"
