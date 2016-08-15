import subprocess
import time

timestamp = str(int(time.time()))

not_file_uri_schemes = ["dccp"]

protocol_ports = {"srm": "8443", "gsidcap": "22128", "gsiftp": "2811", "http": "2288", "dcap": "22125"}

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

    def copy_local_file(self, local_file, remote_file, add_timestamp=False):

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

    def copy_remote_file(self, remote_file, local_file):

        if self.protocol:
            self._set_local_file(local_file)
        else:
            raise NotImplementedError(self.ProtocolError)

        if self.client == "srmcp":
            if " -streams_num " not in self.extra_arguments:
                self.extra_arguments += " -streams_num=1 "

        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string()

        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_file + " " + self.local_file
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


    def remove_remote_directory(self, remote_directory):
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
        print "ERROR: ", self.error
        print "RETURN CODE: ", self.returncode


    def error_should_contain(self, expected_error):
        errorstream = "STDOUT: " + self.output + " STDERR: " + self.error

        if expected_error not in errorstream:
            raise AssertionError("Expected error: " + expected_error + " but got: " + errorstream)

    def command_should_execute_successfully(self):
        client_executed_successfully = True
        if self.client == "srmcp":
            if "ERROR" in self.error:
                client_executed_successfully = False
        elif self.client == "dccp":
            if "error" in self.error:
                client_executed_successfully = False
        elif self.client == "arccp":
            if "ERROR" in self.error:
                client_executed_successfully = False

        if self.returncode >= 1:
            raise AssertionError("Process didn't execute sucessfully. Return code: " + str(self.returncode))

        if not client_executed_successfully:
            raise AssertionError("Process didn't execute command properly. \n STDERR: " + self.error + "\n STDOUT: " + self.output)


