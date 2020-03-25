# -*- coding: utf-8 -*-
#
# async_crawler.py - main module of mailcrawler containing asyncio_crawler
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


# PIP
from requests_html import AsyncHTMLSession

# builtin
import argparse

import re
import urllib.parse as urlparse

import multiprocessing
import asyncio
import time
import urllib3

#my modules
from mailcrawler.logfacility import get_logger

LOGGER = get_logger('asyncio_crawler')

urllib3.disable_warnings()

class asyncio_crawler(object):
    def __init__(self,url,depth = 10, numworkers = None):
        #create a async requests_html session
        self.asession = AsyncHTMLSession(workers = numworkers)
        if numworkers:
            self.numworkers = numworkers
        else:
            self.numworkers = multiprocessing.cpu_count() * 5
        self.url = url
        self.host = urlparse.urlparse(url).netloc
        self.regex = re.compile(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE )
        self.depth = depth
        self.runtime = 0
        self.gen_link_counter = 0
        self.mails = set()
        self.links = set()
        self.links_done = set()
        LOGGER.info('-----> ASYNCIO_CRAWLER INITIALIZED <-----')

    async def Task(self):
        '''This function will be used to generate tasks for the asyncio call'''
        if self.links:
            #TO DO: Check if this is also possible with asyncio.Queue
            url = self.links.pop()
            #LOGGER.info(url)
            self.links_done.add(url)
            # use the async html_request framework to do requests, get html text
            # and to generate new links
            try:
                response = await self.asession.get(url)
                for link in response.html.absolute_links:
                    if self.host in link:
                        self.links.add(link)
                # use regular expression to scan for mail adresses
                for mail_addr in re.findall(self.regex,response.html.full_text):
                    self.mails.add(mail_addr)

            except Exception as e:
                # our requests has failed,but we don't care too much
                LOGGER.warning(e)


    def crawl(self):
        '''main loop'''
        #use the requests_html module to get links and mails
        # find all links on the start url
        self.links.add(self.url)
        Task_list = []
        while self.links and self.gen_link_counter < self.depth:
            for link in self.links:
                Task_list.append(self.Task)
            # run asycio task with run command of async requests_html
            self.asession.run(*Task_list)
            self.links.difference_update(self.links_done)
            self.gen_link_counter += 1


    def run(self):
        '''method to be called from executable'''
        LOGGER.info('-----> RUN ASYNCIO_CRAWLER <-----')
        starttime = time.time()
        try:
            self.crawl()
        except KeyboardInterrupt:  # ..abort crawler using CTRL+C
            pass
        except Exception:
            raise
        self.runtime = time.time() - starttime
        self.report()

    def report(self):
        #report all results to console
        LOGGER.info('-----> ASYNCIO_CRAWLER FINISHED <-----')
        LOGGER.info('-----> REPORT FOLLOWS <-----')
        LOGGER.info('-----> Links done: <-----')
        for link in self.links_done:
            LOGGER.info(link)
        LOGGER.info('-----> Got mails: <-----')
        for mail in self.mails:
            LOGGER.info(mail)
        LOGGER.info('-----> Mails found: <-----')
        LOGGER.info(len(self.mails))
        LOGGER.info('-----> Finished linklist: <-----')
        empty = not bool(self.links)
        LOGGER.info(empty)
        LOGGER.info('-----> Generation of links: <-----')
        LOGGER.info(self.gen_link_counter)
        LOGGER.info('-----> Links done: <-----')
        LOGGER.info(len(self.links_done))
        LOGGER.info('-----> Number of Workers: <-----')
        LOGGER.info(self.numworkers)
        LOGGER.info('-----> ASYNCIO_Crawler runtime [s]: <-----')
        LOGGER.info(self.runtime)
