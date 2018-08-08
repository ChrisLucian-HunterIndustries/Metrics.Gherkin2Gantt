import keyring

from MetricsConfig import get_metrics_config

config = get_metrics_config()

SERVICE_NAME = ""

def get_git_credential(key_name):
    password = keyring.get_password('git credentials', key_name)
    if password is None:
        raise ValueError("\n\nGit Credentials not set for :'{}'\nRun a script with the following to store this information to the keyring: \n\nimport keyring\nkeyring.set_password('git credentials', '{}',<GIT URL>)".format(key_name,key_name))
    return password

