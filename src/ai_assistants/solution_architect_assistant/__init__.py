import autogen

from autogen import ConversableAgent


def load_config_file(file_path: str):
    '''
    Load the autogen models configuration file
    '''

    config_list = autogen.config_list_from_json(
        env_or_file =file_path
    )

    return config_list


def termination_msg(x):
    '''
    Define the termination message
    '''
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()