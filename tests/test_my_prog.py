# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
# pylint: disable=missing-docstring,invalid-name,protected-access
"""
Unit tests for :py:module:`my_prog`.
"""

import pytest

from py_prod_bootstrap import my_prog


@pytest.mark.parametrize('cmd_arg', [None, '', ' '])
def test_main_nok_invalid_cmd(cmd_arg: str):
    # given/when/then
    with pytest.raises(ValueError):
        # given
        my_prog.main(cmd_arg)


MOCK_PATH_RUN_CMD = '.'.join([my_prog.__name__, my_prog._run_cmd.__name__])


def test_main_nok_proc_raises_exception(mocker):
    # given
    message = 'TEST'
    exception = RuntimeError(message)
    with mocker.patch(MOCK_PATH_RUN_CMD, side_effect=exception):
        with pytest.raises(RuntimeError) as ex:
            # when
            my_prog.main('test')
            # then
            assert ex.message == message


MOCK_PATH_LOG_BYTES = '.'.join([my_prog.__name__, my_prog._log_bytes.__name__])


@pytest.mark.parametrize('return_code', [0, 1, -1])
def test_main_ok(mocker, return_code: int):
    # given
    cmd = 'my_test_cmd'
    stdout = b'TEST_STDOUT'
    stderr = b'TEST_STDERR'
    #
    with mocker.patch(MOCK_PATH_RUN_CMD,
                      return_value=(return_code, stdout, stderr)):
        with mocker.patch(MOCK_PATH_LOG_BYTES):
            # when
            result = my_prog.main(cmd)
            # then
            assert result == return_code
            # pylint: disable=no-member
            my_prog._log_bytes.assert_any_call(stderr, mocker.ANY)
            my_prog._log_bytes.assert_any_call(stdout, mocker.ANY)
            my_prog._run_cmd.assert_called_once_with(cmd)
