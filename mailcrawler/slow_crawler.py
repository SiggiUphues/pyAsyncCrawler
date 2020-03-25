# -*- coding: utf-8 -*-
#
# slow_crawler.py - main module of slow_crawler containing simple_crawler
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
from requests_html import HTMLSession

# builtin
import argparse

import re
import urllib.parse as urlparse


import asyncio
import time
import urllib3

#my modules
from mailcrawler.logfacility import get_logger

LOGGER = get_logger('slow_crawler')

urllib3.disable_warnings()

class simple_crawler(object):
    '''main object of mailcrawler module called from executable. Simple
    mailcrawler without any worker using the requests_html framework'''
    def __init__(self,url,depth = 10):

        #crate a requests_html session
        with HTMLSession() as self.session:
            try:
                self.response = self.session.get(url)
            except Exception as e:
                # our requests has failed,but we don't care too much
                LOGGER.warning(e)

        self.url = url
        self.host = urlparse.urlparse(url).netloc
        self.depth = depth
        self.regex = re.compile(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE )
        self.gen_link_counter = 0
        self.runtime = 0
        self.mails = set()
        self.links = set()
        self.links_done = set()

        LOGGER.info('-----> SIMPLE_CRAWLER INITIALIZED <-----')

    def new_response(self,url):
        try:
            # request an url by using the requests_html framework
            self.response = self.session.get(url)
        except Exception as e:
            # our requests has failed,but we don't care too much
            LOGGER.warning(e)

    # generate new links using requests_html
    def gen_links(self):
        for link in self.response.html.absolute_links:
            if self.host in link:
                self.links.add(link)

    # scan a site for mail adresses using a regular expression
    def scan_mails(self):
        for mail_addr in re.findall(self.regex,self.response.html.full_text):
            self.mails.add(mail_addr)

    def crawl(self):
        '''main loop'''
        #use the requests_html module to get links and mails
        # find all links on the start url
        self.gen_links()
        self.gen_link_counter = 1
        #scan for mail adresses on the start url
        self.scan_mails()
        # add scanned url to the list of all scanned urls
        self.links_done.add(self.url)
        # remove all links which are already scanned
        self.links.difference_update(self.links_done)
        while self.gen_link_counter < self.depth:
            links = self.links.copy()
            self.gen_link_counter += 1
            for new_url in links:
                #new_url = self.links.pop()
                #LOGGER.info(new_url)
                self.new_response(new_url)
                self.gen_links()
                self.scan_mails()
                self.links_done.add(new_url)
                self.links.difference_update(self.links_done)
            # if there are no more new links exit
            if not self.links:
                    break

    def run(self):
        '''method to be called from executable'''
        LOGGER.info('-----> RUN SIMPLE_CRAWLER <-----')
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
        LOGGER.info('-----> SIMPLE_CRAWLER FINISHED <-----')
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
        LOGGER.info('-----> SIMPLE_Crawler runtime [s]: <-----')
        LOGGER.info(self.runtime)
