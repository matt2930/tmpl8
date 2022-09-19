import glob
import os

class CommandExtractor:
    files: dict = {}

    def __init__(self, command: list):
        self.command = command
        self._extractFiles()

    def _extractFiles(self) -> set:
        for i, arg in enumerate(self.command):
            for path in glob.glob(arg):
                if os.path.isfile(path):
                    self.files[path] = {'ind': i, 'files': os.path.abspath(path)}
                elif os.path.isdir(path):
                    dir_files = set()
                    for file in glob.glob(f'{path}/**/*'):
                        if os.path.isfile(file):
                            dir_files.add(os.path.abspath(file))
                    self.files[path] = {'ind': i, 'files': dir_files}
