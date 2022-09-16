import argparse
from tmpl8 import __version__

def main():
    parser = argparse.ArgumentParser(prog='tmpl8', description="tmpl8 wrapper for cli commands")
    parser.add_argument('command', help='command to run', nargs=argparse.REMAINDER)
    parser.add_argument('-v', action='version', version=__version__)

    args = parser.parse_args()
    print(args.command)
