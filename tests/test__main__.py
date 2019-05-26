# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
# pylint: disable=missing-docstring,invalid-name,protected-access
"""
Unit tests for :py:module:`__main__`.
"""

import sys

import mock

from py_prod_bootstrap import __main__
from py_prod_bootstrap import my_prog

MOCK_PATH_EXPANDED_MAIN = '.'.join([
    __main__.__name__,
    __main__._expanded_main.__name__
])


@mock.patch(MOCK_PATH_EXPANDED_MAIN)
def test_main_ok(_):
    # given
    expected_log_level = 'test_log_level'
    expected_cmd = 'test_cmd'
    sys.argv = [
        'test_expanded_main',
        __main__.CLI_ARG_LOG_LEVEL, expected_log_level,
        __main__.CLI_ARG_CMD, expected_cmd
    ]
    # when
    __main__.main()
    # then
    # pylint: disable=no-member
    __main__._expanded_main.assert_called_once_with(
        log_level=expected_log_level, cmd=expected_cmd)


MOCK_PATH_MY_PROG_MAIN = '.'.join([my_prog.__name__, my_prog.main.__name__])


@mock.patch(MOCK_PATH_MY_PROG_MAIN)
def test__expanded_main_ok(_):
    # given
    cmd = 'test_cmd'
    # when
    __main__._expanded_main(__main__.DEFAULT_LOG_LEVEL, cmd)
    # then
    # pylint: disable=no-member
    my_prog.main.assert_called_once_with(cmd)
