import os
import yaml
import fnmatch

def load_prompts(prompt_path: str) -> dict:
    """
    Read all prompts from an existing folder and return the dict with available prompts
    the key is the filename without extensions
    """
    results = {}
    files = os.listdir(prompt_path)
    for file in files:
        if os.path.isfile(os.path.join(prompt_path, file)) and fnmatch.fnmatch(file, '*.y*ml'):
            with open(os.path.join(prompt_path, file), 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            assistant_name = content[ "assistant_name" ]
            results[assistant_name] = content
    return results
