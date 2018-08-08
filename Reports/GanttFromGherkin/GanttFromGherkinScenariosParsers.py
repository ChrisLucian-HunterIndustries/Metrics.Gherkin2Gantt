import os
import re
from datetime import datetime, timedelta
from os import listdir

from Constants.PathConstants import PathConstants
from RepositoryCollectors.RepoInvestigator import extract_gherkin_features_and_scenarios_for_project
from Utilities.FileUtilities import ensure_dir


def get_features_added_by_date(scenarios, latest_scenarios):
    scenarios.reverse()
    features_added_by_date = []
    current_list = []
    for earlier_scenario in scenarios:
        date = earlier_scenario[1]
        new_list = list(set(latest_scenarios) - set(earlier_scenario[2]))
        new_features = list(set(new_list) - set(current_list))
        if new_features.__len__() > 0:
            features_added_by_date.append([date, new_features, earlier_scenario[3]])
        current_list = new_list
    return features_added_by_date


def get_scenario_history(path, start_date, end_date):
    if not os.path.exists(path):
        print("No Gherkin History Found")
        return []

    ensure_dir(path)
    result_files = listdir(path)
    dates = []
    counts = []
    scenarios = []
    for file in result_files:
        with open(path + "/" + file, 'r') as content_file:
            file_result = ""

            content = content_file.read()
            feature_descriptions = re.findall(
                    '(?:,*)Total Scenarios & Variations:(.*)\n\n(?:.*)', content)
            total_feature_variants = int(feature_descriptions[0])
            file_dates = re.findall(
                    '(....-..-..)(?:.*)', file)
            date = file_dates[0]
            converted_date = datetime.strptime(date, "%Y-%m-%d").date()
            if start_date <= converted_date <= end_date:
                dates.append(converted_date)
                counts.append(total_feature_variants)

                scenario_search = re.findall(
                        r'(?:Scenarios.*?)|(?:@ignore.*?Feature:.*?Scenario.*)|(?:@ignore.*?Scenario.*?\n)|(Scenario.*?\n)',
                        content, re.DOTALL)
                scenario_search = list(
                    map(lambda scenario: scenario.replace("Scenario Outline: ", "").replace("Scenario: ", ""),
                        scenario_search))
                scenarios.append([file, date, scenario_search, total_feature_variants])
    return scenarios


def get_feature_and_scenario_history(repo, project, file_path_suffix, start_date, end_date):
    run_date = start_date
    while end_date >= run_date:
        weekend = [5, 6]
        if run_date.weekday() not in weekend:
            rollback_date = run_date.__str__() + " 00:00"
            file_name = rollback_date.replace(":", "") + " " + project.project_name + ".txt"
            name = PathConstants.Results + repo.project_name + " features by time/" + file_name
            if not os.path.isfile(name):
                print("Saving", name)
                worked = 0
                while worked < 10:
                    try:
                        repo.get_repo_and_update(PathConstants.Repositories, rollback_date)
                        extract_gherkin_features_and_scenarios_for_project(project, rollback_date.replace(":", "") + " ",
                                                                           repo.project_name + file_path_suffix + "/")
                        worked = 11
                    except:
                        worked += 1
                        print("Retry due to windows SSL cert error ",worked)
        run_date = run_date + timedelta(days=1)