# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Tristan Ueding
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import warnings

# PIP
# compatibility! python-systemd lib strongly depends on systemd
try:
    import systemd.journal
    use_journal = True
except ImportError:
    # warnings.warn('Unable to log to journal!')
    use_journal = False

debugLevelChoices = {
    "Info": logging.INFO,
    "Warn": logging.WARNING,
    "Debug": logging.DEBUG
}

def get_logger(name_logger):
    return logging.getLogger(name_logger)


# logging to file is possible if desired by calling build_logger with a path
def build_logger(name_logger,path = None,logLevel = None):

    # the log level is not specified
    # make the default just print info statements
    if not logLevel:
        logLevel = logging.INFO


    # one logger to rule em' all
    LOGGER = logging.getLogger(name_logger)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        "[%Y-%m-%d %H:%M:%S]"
    )

    # handler for logging to console
    # default behaviour of the StreamHandler
    console_loghandler = logging.StreamHandler()
    console_loghandler.setLevel(logLevel)
    console_loghandler.setFormatter(formatter)
    LOGGER.addHandler(console_loghandler)

    # journal handler
    if use_journal is True:
        journal_loghandler = systemd.journal.JournalHandler()
        journal_loghandler.setLevel(logLevel)
        journal_loghandler.setFormatter(formatter)
        LOGGER.addHandler(journal_loghandler)

    # handler for logging to file
    # make this optional - normally we log to journal
    if path is not None:
        file_loghandler = logging.FileHandler(path)
        file_loghandler.setLevel(logLevel)
        file_loghandler.setFormatter(formatter)
        LOGGER.addHandler(file_loghandler)

    # loglevel for both handlers
    LOGGER.setLevel(logLevel)

    return LOGGER
