from dataclasses import dataclass, field
import glob
import os
import subprocess
import sys

@dataclass
class ArgInfo:
    arg: str
    arg_type: str
    path: str = ''
    files: set[str] = field(default_factory=set)
    template_files: list[str] = field(default_factory=list)
    template_dir: str = ''


class Command:
    arg_info: list[ArgInfo] = []
    new_command: list[str] = []

    def __init__(self, command: list[str]):
        self.command = command
        self._extractFiles()

    def _extractFiles(self) -> set[str]:
        for i, arg in enumerate(self.command):

            arg_to_path = glob.glob(os.path.expandvars(arg))

            if not arg_to_path:
                self.arg_info.append(
                    ArgInfo(
                        arg=arg,
                        arg_type='arg'
                    )
                )

            for path in arg_to_path:
                path = os.path.realpath(os.path.expanduser(path))

                if 'pycache' in arg:
                    self.arg_info.append(
                        ArgInfo(
                            arg=arg,
                            arg_type='ignore'
                        )
                    )
                    continue

                if os.path.isfile(path):
                    self.arg_info.append(
                        ArgInfo(
                            arg=arg,
                            arg_type='file',
                            path=path,
                            files= {os.path.abspath(path)}
                        )
                    )

                elif os.path.isdir(path):
                    dir_files = set()

                    for root, dir, files in os.walk(path):
                        if '.git' in root:
                            continue

                        for file in files:
                            file = os.path.join(root, file)

                            if os.path.isfile(file) and 'pycache' not in file and '.terraform' not in file:
                                dir_files.add(file)

                    self.arg_info.append(
                        ArgInfo(
                            arg=arg,
                            arg_type='dir',
                            path=path,
                            files=dir_files
                        )
                    )

    def generateCommand(self):
        for arg_info in self.arg_info:
            if arg_info.arg_type == 'dir':
                self.new_command.append(arg_info.template_dir)
            elif arg_info.arg_type == 'file':
                self.new_command.append(*arg_info.template_files)
            elif arg_info.arg_type == 'ignore':
                continue
            elif arg_info.arg_type == 'arg':
                self.new_command.append(arg_info.arg)


    def runNewCommand(self):
        try:
            result = subprocess.run(self.new_command, capture_output=True, text=True)
        except KeyboardInterrupt:
            print('--KeyboardInterrupt--', file=sys.stderr)
            exit(1)

        return result
