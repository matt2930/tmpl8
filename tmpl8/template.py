import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader


def templateFile(input_path: str, output_path: str, data={}) -> Optional[str]:

    full_input_path = os.path.realpath(os.path.expanduser(input_path))
    input_file_dir = os.path.dirname(full_input_path)
    input_file_name = os.path.basename(full_input_path)
    environment = Environment(loader=FileSystemLoader(input_file_dir))

    template = environment.get_template(input_file_name)

    content = template.render(**data)

    full_output_path = os.path.realpath(os.path.expanduser(output_path))

    if os.path.isdir(full_output_path):
        full_output_path = f'{full_output_path}/{input_file_name}'

    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return full_output_path
