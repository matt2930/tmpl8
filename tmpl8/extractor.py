import glob
import os

class CommandExtractor:
    arg_info: dict = {}

    def __init__(self, command: list):
        self.command = command
        self._extractFiles()

    def _extractFiles(self) -> set:
        for i, arg in enumerate(self.command):
            for path in glob.glob(arg):
                path = os.path.realpath(path)

                if os.path.isfile(path):
                    self.arg_info[path] = {
                        'type': 'file',
                        'ind': i,
                        'files': {os.path.abspath(path)}
                    }

                elif os.path.isdir(path):
                    dir_files = set()

                    # glob will recurse directories for us, and listdir will get files in parent directory
                    files = glob.glob(os.path.join(path, '**/*')) + [os.path.join(path, f) for f in os.listdir(path)]

                    for file in files:
                        if os.path.isfile(os.path.join(path, file)):
                            dir_files.add(os.path.realpath(os.path.expanduser(file)))

                    self.arg_info[path] = {
                        'type': 'dir',
                        'ind': i,
                        'files': dir_files
                    }
