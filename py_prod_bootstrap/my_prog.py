# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
"""
.. py:currentmodule:: my_prog.py

Runs a shell command.
"""

import logging
import os
import subprocess
import typing

LOGGER = logging.getLogger(__name__)

STDOUT_LOG_LEVEL = logging.INFO
STDERR_LOG_LEVEL = logging.ERROR


def main(cmd: str) -> int:
    """
    :param str cmd: Which shell command to run.
    :rtype: int
    :returns: The return code on the shell command exectution.
    """
    LOGGER.info('Running %s(%s)', __name__, locals())
    actual_cmd = cmd.strip() if cmd else cmd
    # validate input
    if not actual_cmd:
        raise ValueError('The argument {} needs to be given. '
                         'Got: {}'.format(locals(), actual_cmd))
    # call it
    ret_code, stdout, stderr = _run_cmd(actual_cmd)
    #
    _log_bytes(stdout, STDOUT_LOG_LEVEL)
    _log_bytes(stderr, STDERR_LOG_LEVEL)
    #
    if ret_code != 0:
        LOGGER.warning('Command [%s] did not succeed (return code %d), '
                       'check logs', actual_cmd, ret_code)
    #
    return ret_code


# pylint: disable=broad-except
def _run_cmd(cmd: str) -> typing.Tuple[int, bytes, bytes]:
    try:
        proc = subprocess.Popen(cmd.split(' '),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except Exception as ex:
        LOGGER.fatal('Could not execute [%s]. Exception: %s', cmd, ex)
        raise ex
    try:
        stdout, stderr = proc.communicate()
    except Exception as ex:
        LOGGER.fatal('Could not retrieve outputs for [%s]. Exception: %s',
                     cmd, ex)
    return proc.returncode, stdout, stderr


def _log_bytes(output: bytes, log_level: int) -> None:
    for line in output.decode('utf-8').split(os.linesep):
        LOGGER.log(log_level, line)
