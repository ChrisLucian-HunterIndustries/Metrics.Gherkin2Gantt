import GanttGherkinScenarios as ggs
from Constants.PathConstants import PathConstants
from MetricsConfig import get_metrics_config
from RepositoryCollectors.FeatureExtractor import clone_and_update_aat_projects
from RepositoryCollectors.GherkinProject import GherkinProject
from RepositoryCollectors.RollbackableRepo import RollbackableRepo
from RepositoryCollectors.RepoInvestigator import extract_all_gherkin_features_and_scenarios

config = get_metrics_config()

for project in config["projects"]:
    repo_gherkin_projects = list(map(lambda p: [RollbackableRepo(p["name"], p["branch"]), GherkinProject(project["name"],
                                                                                                         PathConstants.Repositories +
                                                                                                         p["name"] + "/" + p[
                                                                                                       "feature_file_path"])
                                                ], project["gherkin_repos"]))

    repositories = list(map(lambda p: p[0], repo_gherkin_projects))
    gherkin_projects = list(map(lambda p: p[1], repo_gherkin_projects))

    print("Clone and Update AAT Projects")
    clone_and_update_aat_projects(repositories)
    print("Extract all Gherkin Features and Scenarios")
    extract_all_gherkin_features_and_scenarios(gherkin_projects)
    print("Save images of Gantt charts for Gherkin Scenarios")
    ggs.save_images_of_gantt_charts_for_gherkin(repo_gherkin_projects)
