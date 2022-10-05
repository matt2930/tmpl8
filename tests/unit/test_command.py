import os
import pytest

from typing import Any, Optional
from unittest.mock import patch
from dataclasses import dataclass
from tmpl8.command import ArgInfo, ArgType, Command


TEST_FILES_DIR = 'tests/test_files'


class TestCommand:

    @dataclass
    class Fixture:
        expected_new_command: list
        expected_arg_info: list
        expected_command_output: str
        command: Optional[Command] = None
        actual_error: Optional[Any] = None
        expected_error: Optional[Any] = None

    @dataclass
    class Params:
        command_list: list
        expected_new_command: list
        expected_arg_info: list
        expected_command_output: str
        expected_error: Any = None

    @pytest.fixture(
        ids=['normal', 'no input command', 'command with dir'],
        params=[
            Params(
                command_list=['kubectl', 'get', 'pods', '-o', 'wide'],
                expected_new_command=['kubectl', 'get', 'pods', '-o', 'wide'],
                expected_arg_info=[
                    ArgInfo(arg='kubectl', arg_type=ArgType.ARG),
                    ArgInfo(arg='get', arg_type=ArgType.ARG),
                    ArgInfo(arg='pods', arg_type=ArgType.ARG),
                    ArgInfo(arg='-o', arg_type=ArgType.ARG),
                    ArgInfo(arg='wide', arg_type=ArgType.ARG)
                ],
                expected_command_output='test'
            ),
            Params(
                command_list=[],
                expected_new_command=[],
                expected_arg_info=[],
                expected_command_output='',
                expected_error=ValueError
            ),
            Params(
                command_list=['ls', TEST_FILES_DIR],
                expected_new_command=['ls', TEST_FILES_DIR],
                expected_arg_info=[
                    ArgInfo(arg='ls', arg_type=ArgType.ARG),
                    ArgInfo(
                        arg=TEST_FILES_DIR,
                        arg_type=ArgType.DIR,
                        path=os.path.abspath(TEST_FILES_DIR),
                        files={
                            os.path.abspath(f'{TEST_FILES_DIR}/test_template.txt'),
                            os.path.abspath(f'{TEST_FILES_DIR}/test_data.json'),
                            os.path.abspath(f'{TEST_FILES_DIR}/test_data.yml'),
                            os.path.abspath(f'{TEST_FILES_DIR}/test_invalid_data'),
                        }
                    )
                ],
                expected_command_output='hello'
            )
        ]
    )
    def setup(self, request) -> Fixture:

        if request.param.expected_error:
            with pytest.raises(Exception) as e:
                command = Command(request.param.command_list)

            return self.Fixture(
                expected_new_command=request.param.expected_new_command,
                expected_arg_info=request.param.expected_arg_info,
                expected_command_output=request.param.expected_command_output,
                expected_error=request.param.expected_error,
                actual_error=e
            )

        command = Command(request.param.command_list)
        command.generateCommand()

        return self.Fixture(
            command=command,
            expected_new_command=request.param.expected_new_command,
            expected_arg_info=request.param.expected_arg_info,
            expected_command_output=request.param.expected_command_output,
            expected_error=request.param.expected_error
        )

    def test_raised_exception(self, setup: Fixture):
        if setup.actual_error:
            assert setup.actual_error.type == setup.expected_error

    def test_get_command_info(self, setup: Fixture):
        if setup.command:
            print(setup.command.arg_info)
            print(setup.expected_arg_info)
            assert setup.command.arg_info == setup.expected_arg_info

    def test_generate_command(self, setup: Fixture):
        if setup.command:
            assert setup.command.new_command == setup.expected_new_command

    @patch('tmpl8.command.subprocess', autospec=True)
    def test_run_command(self, mock_subprocess, setup: Fixture):
        if setup.command:
            mock_subprocess.run.return_value = setup.expected_command_output
            assert setup.command.runCommand() == setup.expected_command_output
            mock_subprocess.run.assert_called_once_with(
                setup.command.new_command,
                capture_output=True,
                text=True
            )
