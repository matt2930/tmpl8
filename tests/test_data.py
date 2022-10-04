from argparse import ArgumentTypeError
from json import JSONDecodeError
import pytest
import tempfile

from tmpl8.data import validateFile


@pytest.mark.parametrize(
    "extension, data, expected_data",
    [
        (".json", '{"test": 1}', {'test': 1}),
        (".yml", 'test:\n  - "a"', {'test': ['a']}),
        (".yml", '{"test": 1}', ArgumentTypeError),
        (".yaml", '{"test": 1}', {'test': 1}),
        (".txt", 'test\n  - "a"', JSONDecodeError)
    ]
)
def test_validate_file(extension, data, expected_data):

    tf = tempfile.NamedTemporaryFile(suffix=extension)
    tf.write(data.encode('utf-8'))
    tf.seek(0)

    if expected_data == ArgumentTypeError:
        tf.close()
        with pytest.raises(Exception) as error:
            actual_data = validateFile(tf.name)

        assert error.type == expected_data

    elif expected_data == JSONDecodeError:
        with pytest.raises(Exception) as error:
            actual_data = validateFile(tf.name)

        tf.close()
        assert error.type == JSONDecodeError

    else:
        actual_data = validateFile(tf.name)
        tf.close()
        assert actual_data == expected_data
