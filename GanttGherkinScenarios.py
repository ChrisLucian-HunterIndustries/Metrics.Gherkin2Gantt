from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

import Reports.GanttFromGherkin.GanttFromGherkinScenariosParsers as gantt_parsers
import Reports.GanttFromGherkin.GanttFromGherkinScenariosReport as gantt_report
from Constants.PathConstants import PathConstants


def save_images_of_gantt_charts_for_gherkin(gantt_datum):
    end_date = datetime.today().date() - timedelta(days=1)
    start_date = end_date - relativedelta(months=3)
    save_images_of_gantt_charts(gantt_datum, start_date, end_date)


def save_images_of_gantt_charts(gantt_data, start_date, end_date):
    for gantt_data in gantt_data:
        repo = gantt_data[0]
        project = gantt_data[1]

        file_path_suffix = " features by time"

        gantt_parsers.get_feature_and_scenario_history(repo, project, file_path_suffix, start_date, end_date)
        scenarios = gantt_parsers.get_scenario_history(PathConstants.Results + repo.project_name + file_path_suffix,
                                                       start_date, end_date)
        if scenarios.__len__() > 0:
            latest_scenarios = scenarios[-1][2]
            features_added_by_date = gantt_parsers.get_features_added_by_date(scenarios, latest_scenarios)
            if features_added_by_date.__len__() > 0:
                gantt_report.save_gantt_chart_image_for_scenarios(project, features_added_by_date, latest_scenarios,
                                                                  datetime.combine(end_date, datetime.max.time()))
        else:
            print("No Scenarios")
