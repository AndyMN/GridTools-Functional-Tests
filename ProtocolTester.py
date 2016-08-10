import subprocess
import time

timestamp = str(int(time.time()))

not_file_uri_schemes = ["dccp"]

protocol_ports = {"srm": "8443", "gsidcap": "22128"}

class ProtocolTester:

    def __init__(self):
        self.client = ""
        self.local_file = ""
        self.remote_file = ""
        self.protocol = ""
        self.port = ""
        self.host = ""

        self.process = None
        self.command = ""
        self.output = ""
        self.error = ""
        self.returncode = None

    def _set_client(self, client):
        self.client = client

    def _set_protocol(self, protocol):
        self.protocol = protocol

    def _set_port(self, protocol):
        self.port = protocol_ports[self.protocol]

    def _set_local_file(self, local_file):
        self.local_file = local_file if self.client in not_file_uri_schemes else "file://" + local_file

    def _set_remote_file(self, remote_file):
        self.remote_file = remote_file

    def _set_host(self, host):
        self.host = host

    def _create_command(self):
        self.command = self.client + " " + self.local_file + " " + self.protocol + "://" + self.host + ":" + self.port + self.remote_file + timestamp

    def copy_file(self, client, host, protocol, local_file, remote_file):

        self._set_client(client)
        self._set_protocol(protocol)
        self._set_local_file(local_file)
        self._set_remote_file(remote_file)
        self._set_port(protocol)
        self._set_host(host)

        self._create_command()
        self._execute_command(self.command)

    def _execute_command(self, command):

        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output, self.error = self.process.communicate()
        self.process.wait()
        self.returncode = self.process.returncode
