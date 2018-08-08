from MetricsConfig import get_metrics_config

config = get_metrics_config()

selected_theme = config["selected_theme"]
theme = config["themes"][selected_theme]
theme_colors = theme["colors"]
outcome_colors = theme_colors["outcomes"]


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


frame = hex_to_rgb(theme_colors["frame"])
background = hex_to_rgb(theme_colors["background"])
frame_highlight = hex_to_rgb(theme_colors["frame_highlight"])

text = hex_to_rgb(theme_colors["text"])
highlighted_text = hex_to_rgb(theme_colors["highlighted_text"])

success_failed = hex_to_rgb(outcome_colors["failed"])
success_passed = hex_to_rgb(outcome_colors["passed"])
success_unknown = hex_to_rgb(outcome_colors["unknown"])
success_cancelled = hex_to_rgb(outcome_colors["cancelled"])

svg_report_color = [100, 100, 100]
svg_report_color_increment = 40
svg_report_color_index = 0


def color_as_svg_rgb(color_tripple):
    return 'rgb({},{},{})'.format(color_tripple[0], color_tripple[1], color_tripple[2])


def generate_next_svg_report_color():
    global svg_report_color, svg_report_color_index, svg_report_color_increment
    svg_report_color[svg_report_color_index] = (svg_report_color[
                                                    svg_report_color_index] + svg_report_color_increment) % 255
    svg_report_color_index = (svg_report_color_index + 1) % 3
    return color_as_svg_rgb(svg_report_color)
