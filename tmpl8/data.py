import argparse
import json
import os
import yaml


def validateJsonData(value):
    data = json.loads(value)
    return data


def validateYamlData(value):
    data = yaml.safe_load(value)
    return data


def validateFile(value):
    try:
        with open(value, 'r') as f:
            data = ''.join(f.readlines())
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f'no file: {value}')

    if os.path.splitext(value)[1] in ('.yml', '.yaml'):
        return validateYamlData(data)

    return validateJsonData(data)
