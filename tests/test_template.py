import pytest
import tempfile

from tmpl8.template import templateFile


@pytest.mark.parametrize(
    "test_input, data, expected",
    [
        ('hello: {{ test }}', {'test': 'world'}, 'hello: world'),
        ('hello: {{ test }}', {}, 'hello: ')

    ]

)
def test_template_file(test_input, data, expected):
    with tempfile.NamedTemporaryFile() as tf:

        tf.write(test_input.encode('utf-8'))
        tf.seek(0)

        output = templateFile(tf.name, f'{tf.name}.out', data=data)

        with open(output) as f:
            content = f.read()

        assert content == expected
