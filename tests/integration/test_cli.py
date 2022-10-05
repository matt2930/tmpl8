import pytest
import sys

from dataclasses import dataclass
from io import StringIO
from typing import Optional
from unittest.mock import patch
from tmpl8.cli import main

TEST_FILES_DIR = 'tests/test_files'

USAGE = 'usage: tmpl8 [-h] [-v] [-d DATA] [-f FILE] command'


@dataclass
class SetupInput:
    command: list
    expected_stdout: str = ''
    expected_stderr: str = ''
    expected_error: Optional[SystemExit] = None


@dataclass
class SetupOutput:
    expected_stdout: str = ''
    actual_stdout: str = ''
    expected_stderr: str = ''
    actual_stderr: str = ''
    actual_error: Optional[SystemExit] = None
    expected_error: Optional[SystemExit] = None


@pytest.fixture(
    ids=[
        '-d flag',
        '-f flag',
        'no data',
        'invalid file',
        'invalid json file',
        'invalid json data'
    ],
    params=[
        # -d flag
        SetupInput(
            command=[
                'tmpl8',
                '-d',
                '{"test_var": "hello"}',
                'cat',
                f'{TEST_FILES_DIR}/test_template.txt'
            ],
            expected_stdout='hello\n'
        ),
        # -f flag
        SetupInput(
            command=f'tmpl8 -f {TEST_FILES_DIR}/test_data.json cat {TEST_FILES_DIR}/test_template.txt' \
                    .split(' '),
            expected_stdout='hello\n'
        ),
        # no data
        SetupInput(
            command='tmpl8 ls'.split(' '),
            expected_stderr='error: missing data\n',
            expected_error=SystemExit
        ),
        # invalid file
        SetupInput(
            command='tmpl8 -f test_invalid_data ls'.split(' '),
            expected_error=SystemExit,
            expected_stderr=f"""{USAGE}
tmpl8: error: argument -f/--file: no file: test_invalid_data
"""
        ),
        # invalid json file
        SetupInput(
            command=f'tmpl8 -f {TEST_FILES_DIR}/test_invalid_data ls'.split(' '),
            expected_error=SystemExit,
            expected_stderr=f"""{USAGE}
tmpl8: error: argument -f/--file: invalid validateFile value: '{TEST_FILES_DIR}/test_invalid_data'
"""
        ),
        # invalid json data
        SetupInput(
            command=[
                'tmpl8',
                '-d',
                '{"test":}',
                'ls'
            ],
            expected_error=SystemExit,
            expected_stderr=f"""{USAGE}
tmpl8: error: argument -d/--data: invalid validateJsonData value: '{{"test":}}'
"""
        )
    ]
)
def setup(request):

    with patch.object(sys, 'argv', request.param.command):
        with patch('sys.stderr', new=StringIO()) as mock_stderr, patch('sys.stdout', new=StringIO()) as mock_stdout:

            if request.param.expected_error:
                try:
                    main()
                except SystemExit as error:
                    return SetupOutput(
                        actual_stderr=mock_stderr.getvalue(),
                        expected_stderr=request.param.expected_stderr,
                        actual_error=error,
                        expected_error=request.param.expected_error
                    )

            main()
            return SetupOutput(
                actual_stdout=mock_stdout.getvalue(),
                expected_stdout=request.param.expected_stdout,
            )


def test(setup):
    if not setup.actual_error:
        assert setup.actual_stdout == setup.expected_stdout
    else:
        print(setup.actual_stderr)
        print(setup.expected_stderr)
        assert setup.actual_stderr == setup.expected_stderr
