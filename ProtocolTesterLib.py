import subprocess
import time

timestamp = str(int(time.time()))

not_file_uri_schemes = ["dccp"]

protocol_ports = {"srm": "8443", "gsidcap": "22128"}

class ProtocolTesterLib:

    def __init__(self):
        self.client = ""
        self.local_file = ""
        self.remote_file = ""
        self.protocol = ""
        self.port = ""
        self.host = ""
        self.extra_arguments = ""
        self.timestamp = ""
        self.remote_directory = ""


        self.process = None
        self.command = ""
        self.output = ""
        self.error = ""
        self.returncode = None
        self.host_string = ""

        self.ProtocolError = "Protocol isn't implemented !"
        self.HostError = "Host isn't implemented !"

    def set_client(self, client):
        self.client = client

    def set_protocol(self, protocol, port=-1):
        self.protocol = protocol
        if port < 0:
            self.port = protocol_ports[protocol]
        else:
            self.port = port

    def _set_local_file(self, local_file):
        self.local_file = local_file if self.client in not_file_uri_schemes else "file://" + local_file

    def _set_remote_file(self, remote_file):
        self.remote_file = remote_file

    def _set_remote_directory(self, remote_directory):
        self.remote_directory = remote_directory

    def set_host(self, host):
        self.host = host

    def set_extra_arguments(self, extra_arguments):
        self.extra_arguments = extra_arguments

    def copy_local_file(self, local_file, remote_file, add_timestamp=True):

        if self.protocol:
            self._set_local_file(local_file)
        else:
            raise NotImplementedError(self.ProtocolError)

        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string()

        if add_timestamp:
            self.timestamp = str(int(time.time()))

        self.command = self.client + " " + self.extra_arguments + " " + self.local_file + " " + self.host_string + self.remote_file + self.timestamp
        self._execute_command(self.command)

    def remove_remote_file(self, remote_file):
        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string()
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_file
        self._execute_command(self.command)


    def create_remote_directory(self, remote_directory):
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string()
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory
        self._execute_command(self.command)

    def _create_host_string(self):

        if not self.protocol:
            raise NotImplementedError(self.ProtocolError)

        if not self.host:
            raise NotImplementedError(self.HostError)

        host_string = self.protocol + "://" + self.host + ":" + self.port

        return host_string

    def _execute_command(self, command):
        print "Executing: ", command
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output, self.error = self.process.communicate()
        self.returncode = self.process.returncode
        print "OUTPUT:", self.output

    def output_should_be(self, expected_output):
        if expected_output != self.output:
            raise AssertionError("Expected output: " + expected_output + " but got output: " + self.output)

    def error_should_be(self, expected_error):
        if expected_error != self.error:
            raise AssertionError("Expected error: " + expected_error + " but got error: " + self.error)


