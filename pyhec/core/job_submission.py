"""
Job submission module
---------------------
Higher-level wrapper to deploy the project onto the cluster.
Read more: https://pyhec.gitbook.io/pyhec/modules/job-submission
"""

from typing import Optional, Dict, Union
from os import PathLike

import subprocess
import shutil
import os
import pathlib
from pyhec.core.config import read_yaml
from pyhec.core.util.SSH_util import ConnectSSH


class JobSubmission:
    """
    Job submission core: higher-level wrapper to deploy the project onto the cluster.
    """

    ssh_client = None
    __settings = dict()

    # Local directories
    project_dir = parent_dir = None

    # Local file location (path and filename)
    conda_env_path = pip_req_path = archive_path = job_sub_path = None

    # pyHEC-specific directories
    module_dir = settings_dir = templates_dir = None

    # Remote working dir
    remote_dir = None

    # Naming conventions
    project_name = archive_name = None
    submission_script = 'submit_job.sh'
    environment_file = 'environment.yml'
    requirements_file = 'requirements.txt'


    def __init__(self, user_settings: Optional[Union[Dict, PathLike, str, None]] = None, **kwargs):
        """
        :param user_settings: Either a dictionary with key-value pairs or the path to YAML
            file containing all user-specific settings for the cluster (see docs for details)
        """
        # Define paths
        self.project_dir = os.getcwd()  # current working dir
        self.parent_dir = pathlib.Path(self.project_dir).parent  # location to save project archive
        self.module_dir = pathlib.Path(os.path.dirname(__file__)).parent  # pyHEC location to load template file
        self.settings_dir = os.path.join(self.module_dir, 'clustersettings')
        self.templates_dir = os.path.join(self.module_dir, 'submissiontemplates')

        # Define (local) file locations
        self.conda_env_path = os.path.join(self.project_dir, self.environment_file)  # Conda environment file
        self.pip_req_path = os.path.join(self.project_dir, self.requirements_file)  # Conda environment file
        self.project_name = f'project-{self.get_env_name().replace(" ", "")}'  # project name
        self.archive_name = f'{self.project_name}.zip'
        self.archive_path = os.path.join(self.parent_dir, self.archive_name)

        # Load user-specific settings from YAML file
        if user_settings is None:
            user_settings = dict()
        elif not isinstance(user_settings, dict):
            user_settings = read_yaml(user_settings)
        # Override the user settings with the keyword arguments and save as settings
        user_settings.update(kwargs)
        self.__settings = user_settings

        # Load general cluster settings and override with user settings (if applicable)
        cluster_settings = os.path.join(self.settings_dir, f'{self.get_conf("cluster_id")}.yml')
        if os.path.isfile(cluster_settings):
            self.__settings = read_yaml(cluster_settings)
            self.__settings.update(user_settings)


    def get_env_name(self, env_file: Optional[Union[PathLike, str, None]] = None) -> str:
        """
        Loads the Anaconda environment.yml file of the current project (or creates one
        first if there is none) and reads the environment name.

        :param env_file: Location of the Conda environment.yml file

        :return: Name of the current environment as string
        """
        self.conda_env_path = self.conda_env_path if env_file is None else env_file

        if os.path.isfile(self.conda_env_path) is False:
            self.export_condaenv(self.conda_env_path)

        env = read_yaml(self.conda_env_path)
        return env['name']


    def export_condaenv(self, env_file: Optional[Union[PathLike, str, None]] = None):
        """
        Saves the current Anaconda environment to a YAML file in the working dir. The YAML
        file will be used to setup the environment on the cluster.

        :param env_file: Location of the Conda environment.yml file. If no location is given,
            the default filename environment.yml is used
        """
        self.conda_env_path = self.conda_env_path if env_file is None else env_file
        subprocess.run(f'conda env export --no-builds --from-history > {self.conda_env_path}', shell=True)
        subprocess.run(f'pip freeze > requirements.txt {self.pip_req_path}', shell=True)

        # Remove ANSI escape characters in the last line of the YAML file
        with open(self.conda_env_path, 'r') as f:
            data = f.readlines()
        with open(self.conda_env_path, 'w') as f:
            f.writelines(data[:-1])


    def generate_submission_script(self, project_dir: Optional[Union[PathLike, str]] = None):
        """
        Copies the submission script for the corresponding cluster in the project directory.

        :param project_dir: location of the current working/project dir

        :return: full path of the job submission script
        """
        template_file = os.path.join(self.templates_dir, f'{self.get_conf("cluster_id")}.sh')
        if not os.path.isfile(template_file):
            raise ValueError(f'No template file for cluster {self.get_conf("cluster_id")} found. '
                             f'Check the cluster_id or create your own submission file.')

        self.job_sub_path = self.project_dir if project_dir is None else project_dir
        self.job_sub_path = os.path.join(self.job_sub_path, self.submission_script)

        shutil.copy(template_file, self.job_sub_path)
        return self.job_sub_path


    def zip_project(self, project_dir: Optional[Union[PathLike, str]] = None,
                    output_file: Optional[Union[PathLike, str]] = None) -> str:
        """
        Creates a ZIP file ENV_NAME.zip containing all project files. This file will be
        transferred to the cluster when deploying the project.

        :param project_dir: location of the current working/project dir
        :param output_file: path and filename of where to save the ZIP file

        :return: full path of the ZIP file
        """
        self.archive_path = self.archive_path if output_file is None else output_file
        self.project_dir = self.project_dir if project_dir is None else project_dir
        shutil.make_archive(self.archive_path[:-4], 'zip', self.project_dir)
        return self.archive_path


    def transfer_project(self, local_archive: Optional[Union[PathLike, str]] = None,
                         remote_dir: Optional[Union[PathLike, str]] = None) -> Union[str, PathLike]:
        """"
        Transfers an archived project to the cluster via SFTP and unpacks the archive.

        :param local_archive: local location of the project archive (including filename)
        :param remote_dir: remote location to upload the archive to (without filename)

        :return the remote path of the project
        """
        # Get active SSH channel
        ssh = self.__ssh_client()

        # Set local path
        self.archive_path = self.archive_path if local_archive is None else local_archive

        # Set remote path
        self.remote_dir = self.get_conf('remote_project_dir') if remote_dir is None else remote_dir
        # "Translate" environment variables as an absolute path (necessary for SFTP)
        if self.remote_dir.startswith('$'):
            self.remote_dir = ssh.find_remote_dir(self.remote_dir)

        # Check archive type (only ZIP!)
        self.archive_name = os.path.basename(self.archive_path)
        if self.archive_name[-4:] != '.zip':
            raise ValueError(f'file_name has to be a ZIP file: {self.archive_name}')

        print('Start transferring project archive to the cluster.')

        # Upload files and unpack the archive to the remote project dir
        ssh.sftp_upload(local_file=self.archive_path,
                        remote_file=os.path.join(self.remote_dir, self.archive_name),
                        upload_desc=self.archive_name)
        ssh.ssh_client.exec_command(f'cd {self.remote_dir} && '
                                    f'unzip -q -o -DD {self.archive_name} -d {self.archive_name[:-4]}')
        self.remote_dir = os.path.join(self.remote_dir, self.archive_name[:-4])
        self.remote_dir = self.remote_dir.replace('\\', '/')

        print(f'Success. Project uploaded and unpacked to {self.remote_dir}')
        return self.remote_dir


    def submit_job(self):
        print('coming soon...')


    def deploy_project(self):
        """
        Wraps together all necessary steps to run a Python project on the cluster. These steps
        include: export the current environment; generate all necessary job submission files;
        transfer a ZIP-compressed archive of the project to the cluster; and submit the project
        as-is to the job scheduler. This is the easiest way of using the cluster.
        """
        print('Start deploying project. This might take a while.')
        self.export_condaenv()
        self.generate_submission_script()
        self.zip_project()
        self.transfer_project()
        self.submit_job()
        print('Done. Project deployed and job submitted.')


    def get_conf(self, key: Union[str, int]) -> Union[str, int]:
        """
        Checks the provided user and general cluster settings and returns the defined
        option. If no setting was provided, asks for manual user input.

        :param key: key of the settings dictionary

        :return: value of the settings item
        """
        if key not in self.__settings:
            self.__settings[key] = input(f'*** Config item missing. Please input manually: {key}')
        return self.__settings[key]


    def __ssh_client(self):
        """
        Returns an active SSH connection.
        """
        # Only create new connection object if necessary
        if self.ssh_client is not None:
            return self.ssh_client

        # Establish a new connection
        host_key_dir = self.settings_dir if self.get_conf('check_hostkey') else None
        self.ssh_client = ConnectSSH(hostname=self.get_conf('hostname'),
                                     username=self.get_conf('username'),
                                     password=self.get_conf('password'),
                                     host_key_dir=host_key_dir)
        return self.ssh_client
