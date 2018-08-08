from Constants.PathConstants import PathConstants

def clone_and_update_aat_projects(repositories,rollback_date=None):
    for project_info in repositories:
        print("Getting from git: " + project_info.project_name)
        repo = project_info.get_repo_and_update(PathConstants.Repositories,rollback_date)
        commits_touching_path = list(repo.iter_commits(project_info.master_branch))
        print(project_info.project_name + ": " + commits_touching_path.__len__().__str__() + " commits\n")

