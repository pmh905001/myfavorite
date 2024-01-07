import json
from unittest import mock

import pytest

from toutiao.dbimporter import DBImporter


def test_locate_position_last_id_is_none():
    result = DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], None)
    assert result == [('file0.txt', -1, -1), ('file1.txt', -1, -1), ('file2.txt', -1, -1)]


def test_locate_position_line1():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter([json.dumps({'data': [{'id': '1'}, {'id': '2'}, {'id': '3'}]})])
        )
        result = DBImporter()._locate_position(['file1.txt', 'file2.txt', 'file3.txt'], '2')
        assert result[0] == ('file3.txt', 0, 1)


def test_locate_position_line2():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter([
                json.dumps({'data': [{'id': 'number'}, {'id': 'number'}, {'id': 'number'}]}),
                json.dumps({'data': [{'id': 'number'}, {'id': '2'}, {'id': 'number'}]})
            ])
        )
        result = DBImporter()._locate_position(['file1.txt', 'file2.txt', 'file3.txt'], '2')
        assert result[0] == ('file3.txt', 1, 1)


def test_locate_position_file2():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            side_effect=[
                iter([
                    json.dumps({'data': [{'id': 'file2_line0_number0'}, {'id': 'file2_line0_number1'},
                                         {'id': 'file2_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file2_line1_number0'}, {'id': 'file2_line1_number1'},
                                         {'id': 'file2_line1_number2'}]})
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file1_line0_number0'}, {'id': 'file1_line0_number1'},
                                         {'id': 'file1_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line1_number0'}, {'id': '2'}, {'id': 'file1_line1_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line2_number0'}, {'id': 'file1_line2_number1'},
                                         {'id': 'file1_line2_number2'}]}),
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file0_line0_number0'}, {'id': 'file0_line0_number1'},
                                         {'id': 'file0_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file0_line1_number0'}, {'id': 'file0_line1_number1'},
                                         {'id': 'file0_line1_number2'}]})
                ]),
            ]

        )
        result = DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], '2')
        assert result == [('file1.txt', 1, 1), ('file2.txt', -1, -1)]


def test_locate_position_ignore_first_line_first_data():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            side_effect=[
                iter([
                    json.dumps({'data': [{'id': 'file2_line0_number0'}, {'id': 'file2_line0_number1'},
                                         {'id': 'file2_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file2_line1_number0'}, {'id': 'file2_line1_number1'},
                                         {'id': 'file2_line1_number2'}]})
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file1_line0_number0'}, {'id': 'file1_line0_number1'},
                                         {'id': 'file1_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line1_number0'}, {'id': 'file1_line1_number1'},
                                         {'id': 'file1_line1_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line2_number0'}, {'id': 'file1_line2_number1'},
                                         {'id': 'file1_line2_number2'}]}),
                ]),
                iter([
                    json.dumps({'data': [{'id': '2'}, {'id': 'file0_line0_number1'},
                                         {'id': 'file0_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file0_line1_number0'}, {'id': 'file0_line1_number1'},
                                         {'id': 'file0_line1_number2'}]})
                ]),

            ]

        )
        result = DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], '2')
        assert result == [('file1.txt', -1, -1), ('file2.txt', -1, -1)]


def test_locate_position_not_ignore_first_line_if_not_first_data():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            side_effect=[
                iter([
                    json.dumps({'data': [{'id': 'file2_line0_number0'}, {'id': 'file2_line0_number1'},
                                         {'id': 'file2_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file2_line1_number0'}, {'id': 'file2_line1_number1'},
                                         {'id': 'file2_line1_number2'}]})
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file1_line0_number0'}, {'id': 'file1_line0_number1'},
                                         {'id': 'file1_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line1_number0'}, {'id': 'file1_line1_number1'},
                                         {'id': 'file1_line1_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line2_number0'}, {'id': 'file1_line2_number1'},
                                         {'id': 'file1_line2_number2'}]}),
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file0_line0_number0'}, {'id': '2'}, {'id': 'file0_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file0_line1_number0'}, {'id': 'file0_line1_number1'},
                                         {'id': 'file0_line1_number2'}]})
                ]),

            ]

        )
        result = DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], '2')
        assert result == [('file0.txt', 0, 1), ('file1.txt', -1, -1), ('file2.txt', -1, -1)]


def test_locate_position_not_ignore_if_not_first_line_first_data():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            side_effect=[
                iter([
                    json.dumps({'data': [{'id': 'file2_line0_number0'}, {'id': 'file2_line0_number1'},
                                         {'id': 'file2_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file2_line1_number0'}, {'id': 'file2_line1_number1'},
                                         {'id': 'file2_line1_number2'}]})
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file1_line0_number0'}, {'id': 'file1_line0_number1'},
                                         {'id': 'file1_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line1_number0'}, {'id': 'file1_line1_number1'},
                                         {'id': 'file1_line1_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line2_number0'}, {'id': 'file1_line2_number1'},
                                         {'id': 'file1_line2_number2'}]}),
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file0_line0_number0'}, {'id': 'file0_line0_number1'},
                                         {'id': 'file0_line0_number2'}]}),
                    json.dumps({'data': [{'id': '2'}, {'id': 'file0_line1_number1'}, {'id': 'file0_line1_number2'}]})
                ]),

            ]

        )
        result = DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], '2')
        assert result == [('file0.txt', 1, 0), ('file1.txt', -1, -1), ('file2.txt', -1, -1)]


def test_locate_position_not_found():
    with mock.patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            side_effect=[
                iter([
                    json.dumps({'data': [{'id': 'file2_line0_number0'}, {'id': 'file2_line0_number1'},
                                         {'id': 'file2_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file2_line1_number0'}, {'id': 'file2_line1_number1'},
                                         {'id': 'file2_line1_number2'}]})
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file1_line0_number0'}, {'id': 'file1_line0_number1'},
                                         {'id': 'file1_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line1_number0'}, {'id': 'file1_line1_number1'},
                                         {'id': 'file1_line1_number2'}]}),
                    json.dumps({'data': [{'id': 'file1_line2_number0'}, {'id': 'file1_line2_number1'},
                                         {'id': 'file1_line2_number2'}]}),
                ]),
                iter([
                    json.dumps({'data': [{'id': 'file0_line0_number0'}, {'id': 'file0_line0_number1'},
                                         {'id': 'file0_line0_number2'}]}),
                    json.dumps({'data': [{'id': 'file0_line1_number0'}, {'id': 'file0_line1_number1'},
                                         {'id': 'file0_line1_number2'}]})
                ]),

            ]

        )
        with pytest.raises(FileNotFoundError):
            DBImporter()._locate_position(['file0.txt', 'file1.txt', 'file2.txt'], '2')
