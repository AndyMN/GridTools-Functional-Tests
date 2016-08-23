import subprocess
from UserDefinedVariables import *

not_file_uri_schemes = ["dccp"]    # Protocols that don't use the file:// part


class ProtocolTesterLib:
    """
    Library for client and protocol testing (Test Suite).

    In this library you will find all of the keywords needed to be able to write basic protocol and client tests.

    """

    def __init__(self):
        self.client = ""
        self.local_file = ""
        self.remote_file = ""

        self.protocol1 = ""
        self.port1 = ""
        self.host1 = ""

        self.protocol2 = ""
        self.port2 = ""
        self.host2 = ""

        self.extra_arguments = ""
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
        """
        Sets the client that we are using. (Ex: srmcp, dccp, srmrm, arccp, etc.).

        :param client: Client used to perform the command.

        :return: /

        """
        self.client = client

    def set_protocol(self, protocol1, port1=-1, protocol2=None, port2=-1):
        """
        Sets the protocol(s) and port(s) for the source(s)/destination(s) PROTOCOL://HOST:PORT (Ex: srm://prometheus.desy.de:8443).

        Only set protocol2 and port2 if you are doing things like: srmcp srm://prometheus.desy.de:8443/ http://reference-2-13.desy.de:2880.

        :param protocol1: Protocol for the first remote source/destination.

        :param port1: Port for the first protocol of the first remote source/destination (If not set, will take value from env variables set in Jenkins).

        :param protocol2: Protocol for the second remote source/destination.

        :param port2: Port for the second protocol of the second source/destination.

        :return: /
        """
        self.protocol1 = protocol1
        if port1 < 0:
            self.port1 = PROTOCOL_PORTS[protocol1]
        else:
            self.port1 = port1

        if protocol2:
            self.protocol2 = protocol2
            if port2 < 0:
                self.port2 = PROTOCOL_PORTS[protocol2]
            else:
                self.port2 = port2

    def _set_local_file(self, local_file):
        """
        Private function that sets the local file URI.

        When doing something with a local file it will preface the filename with the file:// prefix if the client needs.
        this and when it isn't already present.

        :param local_file: Absolute path to the file (Optionally can prefix it with file:// if needed).

        :return: /

        """
        if self.client not in not_file_uri_schemes and "file://" not in local_file:
            self.local_file = "file://" + local_file
        else:
            self.local_file = local_file

    def _set_remote_file(self, remote_file):
        """
        Private function that sets the path of the file on the remote source/destination.

        Doesn't do anything special at the moment but is implemented for possible future special cases.

        :param remote_file: Absolute path to file on remote source/destination.

        :return: /
        """
        self.remote_file = remote_file

    def _set_remote_directory(self, remote_directory):
        """
        Private function that sets the path of the directory on the remote source/destination/.


        Doesn't do anything special at the moment but is implemented for possible future special cases.

        :param remote_directory: Absolute path to directory on remote source/destination.

        :return: /
        """
        self.remote_directory = remote_directory

    def set_host(self, host1, host2=None):
        """
        Sets the remote host(s) (Ex: prometheus.desy.de, reference-2-13.desy.de, etc.).

        Only set host2 if you are doing stuff that requires two remote sources/destinations (Ex: srmcp srm://prometheus.desy.de:8443/ http://reference-2-13.desy.de:2880).

        :param host1: SUT of first dCache machine.

        :param host2: SUT of second dCache machine (optional).

        :return: /
        """
        self.host1 = host1

        if host2:
            self.host2 = host2

    def set_extra_arguments(self, extra_arguments):
        """
        Sets extra tags that would be needed in the command call. (Ex: srmcp -retry_num=0 local_file remote_file, -retry_num=0 would have to be passed).

        :param extra_arguments: Space seperated string of extra tags needed in the command line call (Ex: "-retry_num=0 -2").

        :return: /

        """
        self.extra_arguments = extra_arguments

    def get_remote_files_list(self, remote_directory):
        """
        Gets the list of files (no directories) in the remote directory.

        For every ls client, you can implement a way to distill just the file names.

        :param remote_directory: Absolute path to directory on remote source/destination

        :return: A list of names of the files in the remote directory.

        """
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory

        self._execute_command(self.command)

        file_names_list = []

        if self.client == "srmls":
            file_names_dir = self.output.split("\n")
            for size_name in file_names_dir:
                size_name_split = size_name.split()
                if len(size_name_split) >= 2:
                    file_name = size_name_split[1]
                    if file_name[-1] != "/":
                        file_names_list.append(file_name)

        return file_names_list

    def get_space_tokens(self, space_desc):
        """
        Gets the space reservation tokens on the remote host.

        :param space_desc: Space reservation description. This gets set when reserving space.

        :return: /
        """

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)

        specific_arguments = " "

        if self.client == "srm-get-space-tokens":
            if space_desc and "space_desc" not in self.extra_arguments:
                specific_arguments += " -space_desc=" + space_desc

        self.command = self.client + " " + self.extra_arguments + specific_arguments + self.host_string + "/"
        self._execute_command(self.command)

    def reserve_space(self, space_desc, guaranteed_size="2", retention_policy="REPLICA"):
        """
        Reserves space on the remote host.

        :param space_desc: Space reservation description.

        :param guaranteed_size: Guaranteed size of the reserved space (Bytes).

        :param retention_policy: Retention policy can be set to REPLICA, OUTPUT or CUSTODIAL.

        :return: String of the space token (Ex: Output: Space token=42, returns "42").

        """

        specific_arguments = " "

        if self.client == "srm-reserve-space":
            if space_desc and "space_desc" not in self.extra_arguments:
                specific_arguments += " -space_desc=" + space_desc
            if guaranteed_size and "guaranteed_size" not in self.extra_arguments:
                specific_arguments += " -guaranteed_size=" + guaranteed_size
            if retention_policy and "retention_policy" not in self.extra_arguments:
                specific_arguments += " -retention_policy=" + retention_policy

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)

        self.command = self.client + " " + self.extra_arguments + specific_arguments + self.host_string + "/"
        self._execute_command(self.command)

        space_token = -1

        if "Space token" in self.output:
            equal_sign_index = self.output.find("=")
            space_token = self.output[equal_sign_index + 1:]

        return space_token

    def release_space(self, space_token):
        """
        Releases space that was previously reserved on the remote host.

        :param space_token: Space token obtained after reserving space.

        :return: /
        """

        specific_arguments = " "

        if self.client == "srm-release-space":
            if space_token and "space_token" not in self.extra_arguments:
                specific_arguments += " -space_token=" + space_token

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + specific_arguments + self.host_string + "/"
        self._execute_command(self.command)



    def get_remote_directories_list(self, remote_directory):
        """
        Gets the list of directories in a remote directory.

        For every ls client, you can implement a way to distill just the directories.

        :param remote_directory: Directory of the remote host where we want to search for directories in.

        :return: List of names of the directories in the remote directory.

        """
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
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
        """
        Copies a local file to a remote destination.

        :param local_file: Absolute path to the file on the local machine

        :param remote_file: Absolute path to the file on the remote host

        :return: /

        """
        if self.protocol1:
            self._set_local_file(local_file)
        else:
            raise NotImplementedError(self.ProtocolError)

        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)

        self.command = self.client + " " + self.extra_arguments + " " + self.local_file + " " + self.host_string + self.remote_file
        self._execute_command(self.command)

    def copy_remote_file(self, remote_file, local_file):
        """
        Copies a file from a remote source to the local machine

        :param remote_file:  Absolute path of the remote file

        :param local_file: Absolute path of the local destination

        :return: /

        """
        if self.protocol1:
            self._set_local_file(local_file)
        else:
            raise NotImplementedError(self.ProtocolError)

        specific_arguments = " "

        if self.client == "srmcp":
            if " -streams_num " not in self.extra_arguments:
                specific_arguments += " -streams_num=1 "

        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)

        self.command = self.client + " " + self.extra_arguments + specific_arguments + self.host_string + self.remote_file + " " + self.local_file
        self._execute_command(self.command)

    def copy_remote_to_remote(self, remote_file1, remote_file2):
        """
        Copies from one remote source to a remote destination

        :param remote_file1: Absolute path of the remote file

        :param remote_file2: Absolute path of the remote destination

        :return: /

        """
        self.local_file = remote_file1
        self.remote_file = remote_file2

        host_string1 = self._create_host_string(self.protocol1, self.port1, self.host1)
        host_string2 = self._create_host_string(self.protocol2, self.port2, self.host2)

        self.command = self.client + " " + self.extra_arguments + " " + host_string1 + self.local_file + " " + host_string2 + self.remote_file
        self._execute_command(self.command)

    def remove_remote_file(self, remote_file):
        """
        Delete a remote file

        :param remote_file: Absolute path of the file on the remote host

        :return: /

        """
        self._set_remote_file(remote_file)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_file
        self._execute_command(self.command)


    def create_remote_directory(self, remote_directory):
        """
        Create a directory on a remote host

        :param remote_directory: Absolute path of the directory on the remote host

        :return: /

        """
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory
        self._execute_command(self.command)


    def remove_remote_directory(self, remote_directory):
        """
        Remove a directory on a remote host

        :param remote_directory: Absolute path of the directory on the remote host

        :return: /

        """
        self._set_remote_directory(remote_directory)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory
        self._execute_command(self.command)

    def change_remote_permissions(self, remote_directory, perm_type=None, owner=None, group=None, other=None):
        """
        Change the permissions of a remote directory

        :param remote_directory: Absolute path of the directory on the remote host

        :param perm_type: Permissions Type

        :param owner: Config for Owner (X, W, WR, R, RX, RW, RWX)

        :param group: Config for Group (X, W, WR, R, RX, RW, RWX)

        :param other: Config for Other (X, W, WR, R, RX, RW, RWX)

        :return: /

        """
        specific_arguments = " "

        if self.client == "srm-set-permissions":
            possible_types = ["ADD", "REMOVE", "CHANGE"]
            possible_permissions = ["NONE", "X", "W", "WR", "R", "RX", "RW", "RWX"]

            if perm_type and "type" not in self.extra_arguments:
                if perm_type in possible_types:
                    specific_arguments += " -type=" + perm_type
                else:
                    raise ValueError(perm_type + " not in list of possible types: " + possible_types)

            if owner and "owner" not in self.extra_arguments:
                if owner in possible_permissions:
                    specific_arguments += " -owner=" + owner
                else:
                    raise ValueError(owner + " not in list of possible permissions for owner: " + possible_permissions)

            if group and "group" not in self.extra_arguments:
                if group in possible_permissions:
                    specific_arguments += " -group=" + group
                else:
                    raise ValueError(group + " not in list of possible permissions for group: " + possible_permissions)

            if other and "other" not in self.extra_arguments:
                if other in possible_permissions:
                    specific_arguments += " -other=" + other
                else:
                    raise ValueError(other + " not in list of possible permissions for other: " + possible_permissions)

        self._set_remote_directory(remote_directory)
        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)
        self.command = self.client + " " + self.extra_arguments + specific_arguments + self.host_string + self.remote_directory
        self._execute_command(self.command)

    def perform_arbitrary_command_on_remote_dir(self, remote_dir):
        """
        Perform arbitrary command line call using just the SET CLIENT, SET PROTOCOL, SET HOST and SET REMOTE DIR functions.
        Console command=  Client + " " + Extra_arguments + " " + Protocol + Host + Port + Remote_Dir


        :param remote_dir: Absolute path of the remote directory

        :return: /
        """
        self._set_remote_directory(remote_dir)

        self.host_string = self._create_host_string(self.protocol1, self.port1, self.host1)

        self.command = self.client + " " + self.extra_arguments + " " + self.host_string + self.remote_directory
        self._execute_command(self.command)


    def _create_host_string(self, protocol, port, host):
        """
        Creates the host string by combining protocol, host and port:
        Host string= Protocol + Host + Port
        :param protocol: Protocol to use for talking to remote
        :param port: Port that the protocol uses
        :param host: Remote hostname
        :return: /
        """
        if not protocol:
            raise NotImplementedError(self.ProtocolError)

        if not host:
            raise NotImplementedError(self.HostError)

        host_string = protocol + "://" + host + ":" + port

        return host_string

    def _execute_command(self, command):
        """
        Execute the command in a shell.
        :param command: Command to enter in a shell
        :return: /
        """
        print "Executing: ", command
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output, self.error = self.process.communicate()
        self.returncode = self.process.returncode
        print "OUTPUT:", self.output
        print "ERROR: ", self.error
        print "RETURN CODE: ", self.returncode


    def error_should_contain(self, expected_error):
        """
        Checks the error output for the expected error.

        Throws assertion error if it's wrong.

        :param expected_error: Error to check if it's contained in the error output

        :return: /

        """
        errorstream = "STDOUT: " + self.output + " STDERR: " + self.error

        if expected_error not in errorstream:
            raise AssertionError("Expected error: " + expected_error + " but got: " + errorstream)
        elif expected_error == "":
            raise AssertionError("Expected no error but got: " + errorstream)

    def command_should_execute_successfully(self):
        """
        Checks if the command executed successfully

        Throws assertion error if something went wrong.

        :return:
        """
        client_executed_successfully = True

        if "error" in self.error or "ERROR" in self.error:
            client_executed_successfully = False

        if self.returncode >= 1 or not client_executed_successfully:
            raise AssertionError("Process didn't execute command properly. \n Return Code: " + str(self.returncode) +"\n STDERR: " + self.error + "\n STDOUT: " + self.output)


