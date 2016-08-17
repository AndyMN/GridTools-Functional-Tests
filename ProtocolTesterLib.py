import subprocess
import time
from UserDefinedVariables import *

timestamp = str(int(time.time()))

not_file_uri_schemes = ["dccp"]


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
            self.port = PROTOCOL_PORTS[protocol]
        else:
            self.port = port

    def _set_local_file(self, local_file):
        if self.client not in not_file_uri_schemes and "file://" not in local_file:
            self.local_file = "file://" + local_file
        else:
            self.local_file = local_file

    def _set_remote_file(self, remote_file):
        self.remote_file = remote_file

    def _set_remote_directory(self, remote_directory):
        self.remote_directory = remote_directory

    def set_host(self, host):
        self.host = host

    def set_extra_arguments(self, extra_arguments):
        self.extra_arguments = extra_arguments

    def get_remote_files_list(self, remote_directory):
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string()
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory

        self._execute_command(self.command)

        file_names_list = []

        if self.client == "srmls":
            file_names_dir = self.output.split("\n")
            for size_name in file_names_dir:
                file_name = size_name.split()
                if len(file_name) >= 2:
                    file_names_list.append(file_name[1])

        return file_names_list

    def get_space_tokens(self, base_dir, space_desc=None):
        self._set_remote_directory(base_dir)

        self.host_string = self._create_host_string()

        if self.client == "srm-get-space-tokens":
            if space_desc and "space_desc" not in self.extra_arguments:
                self.extra_arguments += " -space_desc=" + space_desc

        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory
        self._execute_command(self.command)



    def get_remote_directories_list(self, remote_directory):
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string()
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory

        self._execute_command(self.command)

        directories_list = []

        if self.client == "srmls":
            ls_names_dir = self.output.split("\n")
            for size_name in ls_names_dir:
                size_dir_split = size_name.split()
                if len(size_dir_split) >= 2:
                    dir_name = size_dir_split[1]
                    if dir_name[-1] == "/":
                        directories_list.append(dir_name)

        return directories_list

    def copy_local_file(self, local_file, remote_file):

        if self.protocol:
            self._set_local_file(local_file)
        else:
            raise NotImplementedError(self.ProtocolError)

        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string()

        self.command = self.client + " " + self.extra_arguments + " " + self.local_file + " " + self.host_string + self.remote_file
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

    def copy_remote_to_remote(self, remote_file1, remote_file2):

        self.local_file = remote_file1
        self.remote_file = remote_file2

        self.host_string = self._create_host_string()

        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.local_file + " " + self.host_string + self.remote_file
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

    def change_remote_permissions(self, remote_directory, perm_type=None, owner=None, group=None, other=None):
        if self.client == "srm-set-permissions":
            possible_types = ["ADD", "REMOVE", "CHANGE"]
            possible_permissions = ["NONE", "X", "W", "WR", "R", "RX", "RW", "RWX"]

            if perm_type and "type" not in self.extra_arguments:
                if perm_type in possible_types:
                    self.extra_arguments += " -type=" + perm_type
                else:
                    raise ValueError(perm_type + " not in list of possible types: " + possible_types)

            if owner and "owner" not in self.extra_arguments:
                if owner in possible_permissions:
                    self.extra_arguments += " -owner=" + owner
                else:
                    raise ValueError(owner + " not in list of possible permissions for owner: " + possible_permissions)

            if group and "group" not in self.extra_arguments:
                if group in possible_permissions:
                    self.extra_arguments += " -group=" + group
                else:
                    raise ValueError(group + " not in list of possible permissions for group: " + possible_permissions)

            if other and "other" not in self.extra_arguments:
                if other in possible_permissions:
                    self.extra_arguments += " -other=" + other
                else:
                    raise ValueError(other + " not in list of possible permissions for other: " + possible_permissions)

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
        elif expected_error == "":
            raise AssertionError("Expected no error but got: " + errorstream)

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


