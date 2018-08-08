import os
import subprocess

import git

from Secrets import get_git_credential


class RollbackableRepo(object):
    def __init__(self, project_name, master_branch, url= None):
        self.master_branch = master_branch
        if url is None:
            self.repo_url = get_git_credential(project_name)
        else:
            self.repo_url = url
        self.project_name = project_name
        self.repo = None

    def get_repo_and_update(self, repo_directory, rollback_date=None):
        project_path = repo_directory + self.project_name
        print("Trying to check out " + self.repo_url)
        if not os.path.exists(project_path):
            repo = git.Repo.clone_from(self.repo_url, project_path, branch=self.master_branch)
        else:
            repo = git.Repo(project_path)
            repo.git.stash('-u')
            repo.git.checkout(self.master_branch)
        if not repo.active_branch.__str__() == self.master_branch:
            repo.git.fetch("--all")
        repo.git.pull(force=True)
        repo.git.checkout(self.master_branch, force=True)
        repo.git.reset("--hard")
        repo.git.checkout(self.master_branch)
        repo.git.checkout(".")
        if rollback_date is not None:
            parameter = "git rev-list -n 1 --before=\"" + rollback_date + "\" " + self.master_branch
            command = "git checkout " + parameter
            try:
                commit_hash = repo.git.execute(parameter)
                command = "git checkout " + commit_hash
                repo.git.execute(command)
            finally:
                pass
        self.repo = repo
        return repo
