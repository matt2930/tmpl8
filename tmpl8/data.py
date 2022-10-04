import json
import os
import yaml

from argparse import ArgumentTypeError


def validateJsonData(data: str) -> dict:
    return json.loads(data)


def validateYamlData(data: str) -> dict:
    return yaml.safe_load(data)


def validateFile(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = ''.join(f.readlines())
    except FileNotFoundError:
        raise ArgumentTypeError(f'no file: {file_path}')

    if os.path.splitext(file_path)[1] in ('.yml', '.yaml'):
        return validateYamlData(data)

    return validateJsonData(data)
