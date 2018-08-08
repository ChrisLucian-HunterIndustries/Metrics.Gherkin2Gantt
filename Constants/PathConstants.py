from MetricsConfig import get_metrics_config


class PathConstants(object):
    config = get_metrics_config()
    paths_config = config["paths"]
    Repositories = paths_config["repositories"]
    Results = paths_config["results"]
