import argparse
from tempfile import TemporaryDirectory

from tmpl8 import __version__
from tmpl8.extractor import CommandExtractor
from tmpl8.template import templateFile

def main():
    parser = argparse.ArgumentParser(prog='tmpl8', description="tmpl8 wrapper for cli commands")
    parser.add_argument('command', help='command to run', nargs=argparse.REMAINDER)
    parser.add_argument('-v', '--version', action='version', version=__version__)

    args = parser.parse_args()

    if args.command == []:
        parser.print_help()
        parser.exit(status=1, message='error: missing command\n')

    command = CommandExtractor(args.command)

    print(command.arg_info)

    with TemporaryDirectory() as td:
        for arg, info in command.arg_info.items():
            for file in info['files']:
                out_file = templateFile(file, td, {})
                if out_file:
                    print(out_file)
