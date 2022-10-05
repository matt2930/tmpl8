import argparse
import os

from tempfile import TemporaryDirectory
from tmpl8 import __version__
from tmpl8.command import Command
from tmpl8.data import validateJsonData, validateFile
from tmpl8.template import templateFile


def main():
    parser = argparse.ArgumentParser(
        prog='tmpl8',
        description="tmpl8 wrapper for cli commands"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=__version__
    )
    command_group = parser.add_argument_group('command')
    command_group.add_argument(
        'command',
        help='command to run',
        nargs=1,
        default=[]
    )
    command_group.add_argument(
        'args',
        nargs=argparse.REMAINDER,
        help=argparse.SUPPRESS
    )

    data_group = parser.add_argument_group('data', 'data used when templating')
    data_group.add_argument(
        '-d', '--data',
        help=(
            'json data for templating.'
            'Overwrites data from file if -f/--file is specified'
        ),
        type=validateJsonData
    )
    data_group.add_argument(
        '-f', '--file',
        help='file with data to use for templating',
        type=validateFile
    )

    args = parser.parse_args()

    error_message = 'error:'

    if args.command == []:
        error_message = f'{error_message} missing command'

    if not args.data and not args.file:
        error_message = f'{error_message} missing data'

    if error_message != 'error:':
        parser.print_help()
        parser.exit(status=1, message=f'{error_message}\n')

    command = Command(args.command + args.args)

    args.data = args.data or {}
    args.file = args.file or {}

    data = {**args.file, **args.data}

    with TemporaryDirectory() as td:
        for arg_info in command.arg_info:
            dir = td
            if arg_info.arg_type == 'dir':
                dir = os.path.join(td, os.path.basename(arg_info.path))
                os.mkdir(dir)
            for file in arg_info.files:
                arg_info.template_dir = dir
                arg_info.template_files.append(templateFile(file, dir, data))

        command.generateCommand()
        result = command.runCommand()

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
            exit(result.returncode)
