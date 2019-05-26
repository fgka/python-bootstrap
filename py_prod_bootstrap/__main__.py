#!/usr/bin/env python3
# vim: ai:sw=4:ts=4:sta:et:fo=croql
# coding=utf-8
"""
.. py:currentmodule:: __main__.py

CLI entry point
"""
import argparse
import logging
import sys

from py_prod_bootstrap import my_prog

LOGGER = logging.getLogger(__name__)
DEFAULT_LOG_LEVEL = logging.getLevelName(logging.INFO)
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - ' \
                     '%(filename)s:%(lineno)d - %(message)s'

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


def _expanded_main(log_level: str, cmd: str) -> int:
    """
    Just a wrapper that consumes system level settings, applies them, \
            and calls :py:func:`my_prog.main`.

    :param str log_level: Sets the log level to be used, including root logger.
    :param str cmd: Wich command to be run by :py:func:`my_prog.main`.
    :rtype: int
    :returns: The return code on the shell command exectution.
    """
    # set log level
    LOGGER.setLevel(log_level.upper())
    # set global level
    logging.getLogger().setLevel(LOGGER.level)
    #
    LOGGER.info('Running %s(%s)', __name__, locals())
    # call actual logic
    return my_prog.main(cmd.strip())


def _set_root_logger(log_level: int = DEFAULT_LOG_LEVEL,
                     log_format: str = DEFAULT_LOG_FORMAT) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(handler)


def _create_parser() -> argparse.ArgumentParser:
    # description
    result = argparse.ArgumentParser(
        description='Example executable entry point.')
    # arguments
    result.add_argument(CLI_ARG_LOG_LEVEL,
                        help='Defines the minimum log level.',
                        default=DEFAULT_LOG_LEVEL)
    result.add_argument(CLI_ARG_CMD,
                        help='Which shell command to run.',
                        required=True)
    #
    return result


# pylint: disable=invalid-name
if __name__ == "__main__":  # pragma: no cover
    main()
