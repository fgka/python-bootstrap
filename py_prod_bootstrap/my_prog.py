# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
"""
.. py:currentmodule:: my_prog.py

Runs a shell command.
"""

import argparse
import logging
import os
import subprocess
import sys
import typing


STDOUT_LOG_LEVEL = logging.INFO
STDERR_LOG_LEVEL = logging.ERROR

LOGGER = logging.getLogger(__name__)
DEFAULT_LOG_LEVEL = logging.getLevelName(logging.INFO)
DEFAULT_LOG_FORMAT = (
    '%(asctime)s - %(name)s - %(levelname)s - '
    '%(filename)s:%(lineno)d - %(message)s'
)

CLI_ARG_LOG_LEVEL = '--log-level'
CLI_ARG_CMD = '--cmd'


def main() -> int:
    """
    Entry point to be called by :py:func:`__main__`.
    :rtype: int
    :returns: The resulting value from executing the desired command.
    """
    _set_root_logger()
    parser = _create_parser()
    args = parser.parse_args()
    #
    _expanded_main(**vars(args))


def _set_root_logger(
    log_level: int = DEFAULT_LOG_LEVEL, log_format: str = DEFAULT_LOG_FORMAT
) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(handler)


def _create_parser() -> argparse.ArgumentParser:
    # description
    result = argparse.ArgumentParser(
        description='Example executable entry point.'
    )
    # arguments
    result.add_argument(
        CLI_ARG_LOG_LEVEL,
        help='Defines the minimum log level.',
        default=DEFAULT_LOG_LEVEL,
    )
    result.add_argument(
        CLI_ARG_CMD, help='Which shell command to run.', required=True
    )
    #
    return result


def _expanded_main(log_level: str, cmd: str) -> int:
    """
    Just a wrapper that consumes system level settings, applies them, \
            and calls :py:func:`my_prog.main`.

    :param str log_level: Sets the log level to be used, including root logger.
    :param str cmd: Which command to be run by :py:func:`my_prog.main`.
    :rtype: int
    :returns: The return code on the shell command execution.
    """
    # set log level
    LOGGER.setLevel(log_level.upper())
    # set global level
    logging.getLogger().setLevel(LOGGER.level)
    #
    LOGGER.info(f'Running {__name__}({locals()})')
    # call actual logic
    return _run_cmd(cmd.strip())


def _run_cmd(cmd: str) -> int:
    """
    :param str cmd: Which shell command to run.
    :rtype: int
    :returns: The return code on the shell command execution.
    """
    LOGGER.info(f'Running {__name__}({locals()})')
    actual_cmd = cmd.strip() if cmd else cmd
    # validate input
    if not actual_cmd:
        raise ValueError(
            f'The argument {locals()} needs to be given. Got: {actual_cmd}'
        )
    # call it
    ret_code, stdout, stderr = _run_subprocess(actual_cmd)
    #
    _log_bytes(stdout, STDOUT_LOG_LEVEL)
    _log_bytes(stderr, STDERR_LOG_LEVEL)
    #
    if ret_code != 0:
        LOGGER.warning(
            f'Command [{actual_cmd}] did not succeed '
            '(return code {ret_code}), check logs'
        )
    #
    return ret_code


# pylint: disable=broad-except
def _run_subprocess(cmd: str) -> typing.Tuple[int, bytes, bytes]:
    try:
        proc = subprocess.Popen(
            cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as ex:
        LOGGER.fatal(f'Could not execute [{cmd}]. Exception: {ex}')
        raise ex
    try:
        stdout, stderr = proc.communicate()
    except Exception as ex:
        LOGGER.fatal('Could not retrieve outputs for [{cmd}]. Exception: {ex}')
    return proc.returncode, stdout, stderr


def _log_bytes(output: bytes, log_level: int) -> None:
    for line in output.decode('utf-8').split(os.linesep):
        LOGGER.log(log_level, line)
