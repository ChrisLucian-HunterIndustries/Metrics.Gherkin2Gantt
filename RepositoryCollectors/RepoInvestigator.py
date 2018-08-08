import os
import re
from functools import reduce
from os import listdir
from os.path import isfile, join

from Constants.PathConstants import PathConstants
from RepositoryCollectors.GherkinProject import GherkinProject


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_features_and_scenarios(feature_path,feature_files):
    result = ""
    total_scenarios = 0
    total_scenario_variations = 0

    for file in feature_files:
        with open(feature_path + file, 'r') as content_file:
            file_result = ""
            content = content_file.read()

            feature_descriptions = re.findall(
                    '(?:@.*?.*?\n)|(Feature:.*?)(?:Background:)|(Feature:.*?)(?:@)|(Feature:.*?)(?:Scenario:)|(Feature:.*?)(?:Scenario Outline:)', content,
                    re.DOTALL)

            file_result += reduce(lambda x, y: x + reduce(lambda z, f: z + f, y, ""), feature_descriptions, "")

            file_result += '\n'
            scenarios = re.findall(r'(?:@ignore.*?Feature:.*?Scenario.*)|(?:@ignore.*?Scenario.*?\n)|(Scenario.*?\n)', content, re.DOTALL)

            for scenario in scenarios:
                file_result += scenario
            file_result += '\n\n'

            total_scenarios += file_result.count("Scenario")
            total_scenario_variations += file_result.count("Scenario")
            examples = re.findall(r'Examples:.*\n.*?\n((.*\|\n)*)', content)

            if examples.__len__() > 0:
                count = 0
                for example in examples:
                    example_count = example[0].split('\n').__len__() - 2
                    if example_count > 0:
                        count += example_count
                total_scenario_variations += count

            result += file_result
    result_with_totals = "Total Scenarios: " + total_scenarios.__str__() + '\n'
    result_with_totals += "Total Scenarios & Variations: " + total_scenario_variations.__str__() + '\n\n' + result
    return result_with_totals


def extract_all_gherkin_features_and_scenarios(gherkin_projects):
    file_name_prefix="Tested Features "
    sub_path=""
    for gherkin_project in gherkin_projects:
        extract_gherkin_features_and_scenarios_for_project(gherkin_project, file_name_prefix, sub_path)


def extract_gherkin_features_and_scenarios_for_project(gherkin_project, file_name_prefix, sub_path):
    result = extract_gherkin_features_and_scenarios(gherkin_project)
    if result is None: return
    file_name = file_name_prefix + gherkin_project.project_name + ".txt"
    result_path = PathConstants.Results + sub_path
    data_file_name = result_path + file_name
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    with open(data_file_name, "w+") as text_file:
        text_file.write(gherkin_project.project_name + ' Automated Tests\n' + result)


def extract_gherkin_features_and_scenarios(gherkin_project):
    if not os.path.isdir(gherkin_project.project_file_path): return None
    files_in_features_folder = [f for f in listdir(gherkin_project.project_file_path) if
                                isfile(join(gherkin_project.project_file_path, f))]
    feature_files = list(filter(lambda x: x.endswith('.feature'), files_in_features_folder))
    result = get_features_and_scenarios(gherkin_project.project_file_path, feature_files)

    return result


