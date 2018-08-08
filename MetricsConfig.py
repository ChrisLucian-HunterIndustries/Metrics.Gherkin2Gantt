import json
from pathlib import Path

metrics_config_script_path = Path(__file__).parent.__str__()
json1_file = open(metrics_config_script_path + '/config.json')
json1_str = json1_file.read()
metrics_config = json.loads(json1_str)


def get_metrics_config():
    return metrics_config
