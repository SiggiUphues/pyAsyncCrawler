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


from distutils.core import setup
setup(
    name='asyncio_mailcrawler',
    version='0.1',
    description='Create a webcrawler searching for mails',
    long_description='''Enter a webside, search on site
                        and subsites for mail adresses an print them out''',
    author='Tristan Ueding',
    author_email='tristan.ueding@uni-bielefeld.de',
    packages=[
        'mailcrawler',
    ],
    scripts=[
        'bin/slow_crawler',
        'bin/asyncio_crawler',
    ],
)
