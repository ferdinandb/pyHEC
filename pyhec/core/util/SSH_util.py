"""
Helper functions for the job submission module
"""

import paramiko
import time
import base64
import os
from tqdm import tqdm


class ConnectSSH:
    """
    Higher-level wrapper for Paramiko dealing with all the SSH-related tasks. This
    includes file transfer via SFTP and job submission.

    See Paramiko’s documentation http://docs.paramiko.org/en/stable/index.html
    """

    def __init__(self, hostname, username, password, host_key_dir=None):
        """
        Create new SSH connection to the remote server.

        :param hostname: remote server name or IP address
        :param username: username for authentication
        :param password: password for authentication
        :param host_key_dir: Location of the known_hosts file
        """
        self.ssh_client = paramiko.SSHClient()

        if host_key_dir is None:
            # Don't check the known_hosts and blindly accept the remote host key
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        elif os.path.isfile(os.path.join(host_key_dir, 'known_hosts')):
            # Load the known_hosts and reject the connection if no matching key was found
            self.ssh_client.load_host_keys(os.path.join(host_key_dir, 'known_hosts'))
            self.ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())
        else:
            raise FileNotFoundError()

        self.ssh_client.connect(hostname, 22, username, password)
        self.ssh_transport = self.ssh_client.get_transport()
        print(f'Connected to {username}@{hostname}')


    def sftp_upload(self, local_file, remote_file, upload_desc='Uploading file'):
        """
        Uploads a local file to the remote server via SFTP.

        :param local_file: path and filename of the local file to copy
        :param remote_file: path and filename of the remote destination
        :param upload_desc: description next to the progress bar
        """
        sftp = self.ssh_client.open_sftp()
        with TqdmWrap(unit='b', unit_scale=True, desc=upload_desc) as pbar:
            sftp.put(local_file, remote_file, callback=pbar.view_pbar)
        sftp.close()


    def find_remote_dir(self, env_var) -> str:
        """
        Uses the SSH session to find the absolute path of an environment variable.

        :param env_var: environment variable without leading $
        :return: absolute path represented by the environment variable
        """
        # Start a new interactive shell session
        session = self.ssh_transport.open_session()
        session.get_pty()
        session.invoke_shell()

        # Helper function to fetch the shell output
        def ret_output():
            time.sleep(1)  # Wait for the content to be loaded
            while session.recv_ready():  # Retry until content is ready
                time.sleep(1)
                return str(session.recv(1000), 'utf-8')

        # Disregard the server's welcome message and clear stdout
        _ = ret_output()

        # Echo the absolute path in the interactive shell session (the interactive shell
        # session is necessary to get all user-specific environment variables)
        cmd = f'echo ${env_var}'
        session.send(f'{cmd}\n')
        # Get the output and return the line following the initial echo command
        output = ret_output().splitlines()
        return_next_line = False
        for line in output:
            if return_next_line:
                return line
            if line == cmd:
                return_next_line = True
        # Worst case: no path found
        ValueError(f'Unable to find path for ${env_var}')


    def __del__(self):
        """Close the SSH connection when the object gets destroyed."""
        self.ssh_client.close()


def update_known_hosts(host_key_file, hostname, hostkey_str, keytype='ssh-rsa'):
    """
    Adds a new hostname to the list of known hosts.

    Unix command:
    nmap <hostname> --script ssh-hostkey --script-args ssh_hostkey=full
    """
    host_keys = paramiko.hostkeys.HostKeys(host_key_file)
    host_keys.add(hostname, keytype, paramiko.RSAKey(data=base64.b64decode(hostkey_str)))
    host_keys.save(host_key_file)


class TqdmWrap(tqdm):
    """
    Higher-level wrapper instance of tqdm.
    """
    def view_pbar(self, a, b):
        """
        Displays a progress bar to visualize the transfer status. See Paramiko’s
        documentation http://docs.paramiko.org/en/stable/api/sftp.html

        :param a: already transferred bytes
        :param b: total bytes to be transferred
        """
        if self.total is None:
            self.total = int(b)

        # Update incremental progress
        self.update(int(a - self.n))
