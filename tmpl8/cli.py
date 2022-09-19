import argparse
import os

from tempfile import TemporaryDirectory
from tmpl8 import __version__
from tmpl8.command import Command
from tmpl8.template import templateFile

def main():
    parser = argparse.ArgumentParser(prog='tmpl8', description="tmpl8 wrapper for cli commands")
    parser.add_argument('command', help='command to run', nargs=argparse.REMAINDER)
    parser.add_argument('-v', '--version', action='version', version=__version__)

    args = parser.parse_args()

    if args.command == []:
        parser.print_help()
        parser.exit(status=1, message='error: missing command\n')

    command = Command(args.command)

    data = {}

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
        result = command.runNewCommand()
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
            exit(result.returncode)
