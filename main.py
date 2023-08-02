#!/usr/bin/env python3
import os
from shutil import rmtree
from typing import Optional
from configparser import ConfigParser
import argparse
import subprocess

class BitBackup():
    def __init__(self, config_path: str | None, backup_dir: str):
        """
        Initialize BitBackup

        Args:
            config_path (str)         : The configuration file to be loaded.
            backup_dir (str)          : The backup directory to store successful cloned repositories.
        """
        self.backup_dir = backup_dir
        self.tmp_dir = f"{self.backup_dir}.new"
        if not config_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_path = f"{script_dir}/config.ini"
        else:
            self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.workspaces = self.config.sections()

        if not os.path.exists(self.backup_dir):
            os.mkdir(self.backup_dir)

        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)


    def __del__(self):
        if os.path.exists(self.tmp_dir):
            rmtree(self.tmp_dir)


    def clone_repo(self, workspace: str, repo: str) -> bool:
        """
        Clones a repository from bitbucket using the git binary.

        Args:
            workspace (str): The workspace the repo exists under.
            repo (str)     : The repository to clone.

        Returns:
            bool: If the command ran successful with returncode 0.
        """
        repo_url = f"git@bitbucket.org:{workspace}/{repo}.git"
        clone_dir = f"{self.tmp_dir}/{repo}"
        ssh_key = f"./keys/{self.config[workspace]['ssh_key']}"
        cmd = ['git', 'clone', repo_url, clone_dir]
        r = subprocess.run(cmd, env={
            'GIT_SSH_COMMAND': f'ssh -i {ssh_key} -o StrictHostKeyChecking=no'
            }, check=True, capture_output=True)
        if r.returncode != 0:
            print(f"NonZero Return - {r.returncode} on clone of {repo_url}")
            return False
        print(f"Succesfully cloned {repo_url}")
        return True


    def replace_old(self, repo: str | None = None):
        """
        Deletes old backup directory and renames the temporary directory to old.

        Args:
            repo (str, optional): If exists, it will only target specific repository.

        Returns:
            None
        """
        if repo:
            print(f"Removing backup dir: {self.backup_dir}/{repo}")
            rmtree(f"{self.backup_dir}/{repo}")
            print(f"Renaming {self.tmp_dir} to {self.backup_dir}")
            os.rename(f"{self.tmp_dir}/{repo}",f"{self.backup_dir}")
        else:
            print(f"Removing backup dir: {self.backup_dir}")
            rmtree(self.backup_dir)
            print(f"Renaming {self.tmp_dir} to {self.backup_dir}")
            os.rename(self.tmp_dir, self.backup_dir)


    def all(self) -> bool:
        """
        Loop through all of the config and clone every repository.
        Note: This will not delete anything on its own.

        Args:
            None

        Returns:
            bool: Indicates that none of the clone commands had a nonzero return code.
        """
        success = True
        for workspace in self.workspaces:
            for repo in self.config[workspace]['repos'].split(','):
                if not self.clone_repo(workspace, repo):
                    success = False
        return success



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='bitbucket-backup',
                    description='This script will read a config.ini file and clone all repos.')
    parser.add_argument('-c', '--config', help="Path to config.ini used by program. See config-example.ini.")
    parser.add_argument('-b', '--backup-dir', default="./backups", required=True, help="Root directory where backups are finally stored.")
    args = parser.parse_args()

    bb = BitBackup(config_path=args.config, backup_dir=args.backup_dir)
    if bb.all():
        bb.replace_old()

