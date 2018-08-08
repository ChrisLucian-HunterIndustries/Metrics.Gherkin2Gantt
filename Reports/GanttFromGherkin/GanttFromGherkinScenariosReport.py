import os
from datetime import datetime, timedelta
from functools import reduce
import textwrap
import Image
import ImageDraw
import ImageFont

from Constants import ReportColors
from Constants.PathConstants import PathConstants


def save_gantt_chart_image_for_scenarios(project, features_added_by_date, latest_scenarios,
                                         end_date=datetime.today() - timedelta(days=1)):
    width = 1200
    scenario_desciption_length = 580
    header_height = 60
    title_font_size = 25
    scenario_font_size = 16

    row_height_per_scenario = int(scenario_font_size * scenario_desciption_length * 0.005)

    the_scenarios = []
    for feature in features_added_by_date:
        the_scenarios.extend(feature[1])

    height = header_height + the_scenarios.__len__() * (row_height_per_scenario ) + title_font_size
    result_image = Image.new('RGB', (width, height), ReportColors.text)
    draw = ImageDraw.Draw(result_image)
    title_font = ImageFont.truetype("arial.ttf", title_font_size)

    scenario_font = ImageFont.truetype("arial.ttf", scenario_font_size)
    scenario_y_index = 0
    earliest_date = datetime.strptime(features_added_by_date[-1][0], "%Y-%m-%d")
    latest_date = end_date
    total_difference = latest_date - earliest_date
    previous_date = latest_date
    left = width

    draw.rectangle([(0, 0), (scenario_desciption_length, height)], fill=ReportColors.frame)

    draw.rectangle([(0, 0), (width, header_height)], fill=ReportColors.frame)
    draw.text((10, 10), project.project_name + " Completed Scenarios Over Time", font=title_font,
              fill=ReportColors.text)
    right = scenario_desciption_length
    complexity_line_left = width
    complexity_line_top = 0
    row_height = header_height
    for features_for_date in features_added_by_date:
        date = datetime.strptime(features_for_date[0], "%Y-%m-%d")
        diff = previous_date - date
        diff_total = latest_date - date
        diff_percentt = diff.days / total_difference.days

        complexity_line_right = complexity_line_left
        complexity_line_left = complexity_line_right - diff_percentt * (width - scenario_desciption_length)
        complexity_line_bottom = complexity_line_top + height * the_scenarios.__len__() / reduce(lambda x, y: x if x > y[2] else y[2], features_added_by_date, 0)
        complexity_line_top = complexity_line_bottom

        top = height
        for scenario in features_for_date[1]:
            scenario = textwrap.fill(scenario, scenario_desciption_length * 1/8)

            scenario_y_index += 1
            right = left - diff_percentt * (width - scenario_desciption_length)
            bottom = row_height + row_height_per_scenario * 0.1
            top = row_height + row_height_per_scenario * 0.9

            draw.text((10,bottom), scenario, font=scenario_font,
                      fill=ReportColors.text)
            draw.rectangle([(left, bottom), (right, top)], fill=ReportColors.frame_highlight)

            draw.line((scenario_desciption_length, row_height + row_height_per_scenario, width, row_height + row_height_per_scenario),
                      fill=ReportColors.background)
            previous_date = date
            row_height += row_height_per_scenario
        left = right

    left = width
    run_date = earliest_date.date()
    while latest_date.date() > run_date:
        friday = 4
        if run_date.weekday() == friday:
            draw.line((left, header_height, left, row_height), fill=ReportColors.success_passed)
        left -= ((width - scenario_desciption_length ) / total_difference.days)
        run_date = run_date + timedelta(days=1)

    draw.text((scenario_desciption_length + 10, row_height), earliest_date.date().__str__(),
              font=title_font, fill=ReportColors.success_cancelled)
    draw.text((width - 11 * 12, row_height), latest_date.date().__str__(), font=title_font,
              fill=ReportColors.success_cancelled)
    del draw
    directory = PathConstants.Results + "/GanttCharts/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = PathConstants.Results + "/GanttCharts/"
    result_image.save(directory + project.project_name + ".png")