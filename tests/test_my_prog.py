# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
# pylint: disable=missing-docstring,invalid-name,protected-access
"""
Unit tests for :py:module:`my_prog`.
"""

import sys

import mock
import pytest

from py_prod_bootstrap import my_prog


MOCK_PATH_EXPANDED_MAIN = '.'.join([
    my_prog.__name__,
    my_prog._expanded_main.__name__
])


@mock.patch(MOCK_PATH_EXPANDED_MAIN)
def test_main_ok(_):
    # given
    expected_log_level = 'test_log_level'
    expected_cmd = 'test_cmd'
    sys.argv = [
        'test_expanded_main',
        my_prog.CLI_ARG_LOG_LEVEL, expected_log_level,
        my_prog.CLI_ARG_CMD, expected_cmd
    ]
    # when
    my_prog.main()
    # then
    # pylint: disable=no-member
    my_prog._expanded_main.assert_called_once_with(
        log_level=expected_log_level, cmd=expected_cmd)


MOCK_PATH_MY_PROG_RUN_CMD = '.'.join([my_prog.__name__, my_prog._run_cmd.__name__])


@mock.patch(MOCK_PATH_MY_PROG_RUN_CMD)
def test__expanded_main_ok(_):
    # given
    cmd = 'test_cmd'
    # when
    my_prog._expanded_main(my_prog.DEFAULT_LOG_LEVEL, cmd)
    # then
    # pylint: disable=no-member
    my_prog._run_cmd.assert_called_once_with(cmd)


@pytest.mark.parametrize('cmd_arg', [None, '', ' '])
def test__run_cmd_nok_invalid_cmd(cmd_arg: str):
    # given/when/then
    with pytest.raises(ValueError):
        # given
        my_prog._run_cmd(cmd_arg)


MOCK_PATH_RUN_SUBPROCESS = '.'.join([my_prog.__name__, my_prog._run_subprocess.__name__])


def test__run_cmd_nok_proc_raises_exception(mocker):
    # given
    message = 'TEST'
    exception = RuntimeError(message)
    with mocker.patch(MOCK_PATH_RUN_SUBPROCESS, side_effect=exception):
        with pytest.raises(RuntimeError) as ex:
            # when
            my_prog._run_cmd('test')
            # then
            assert ex.message == message


MOCK_PATH_LOG_BYTES = '.'.join([my_prog.__name__, my_prog._log_bytes.__name__])


@pytest.mark.parametrize('return_code', [0, 1, -1])
def test__run_cmd_ok(mocker, return_code: int):
    # given
    cmd = 'my_test_cmd'
    stdout = b'TEST_STDOUT'
    stderr = b'TEST_STDERR'
    #
    with mocker.patch(MOCK_PATH_RUN_SUBPROCESS,
                      return_value=(return_code, stdout, stderr)):
        with mocker.patch(MOCK_PATH_LOG_BYTES):
            # when
            result = my_prog._run_cmd(cmd)
            # then
            assert result == return_code
            # pylint: disable=no-member
            my_prog._log_bytes.assert_any_call(stderr, mocker.ANY)
            my_prog._log_bytes.assert_any_call(stdout, mocker.ANY)
            my_prog._run_subprocess.assert_called_once_with(cmd)
