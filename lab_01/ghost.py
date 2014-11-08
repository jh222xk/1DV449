# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import argparse
import requests
import re
import time


class Ghost:
    url = "http://coursepress.lnu.se/kurser"
    title = ''
    href = ''
    next_page = ''
    course_detail = ''
    course_code = ''
    course_url = ''
    course_plan = ''
    intro_text = ''
    latest_post_url = ''
    latest_post_title = ''
    latest_post_author = ''
    latest_post_time = ''

    program_urls = ''

    headers = {
        'User-Agent': 'Ghost',
        'From': 'jh222xk@student.lnu.se'
    }

    def scrape(self, site):
        """
        Scrapes a given url and parses the information
        """
        if not site.startswith('http://') or site.startswith('https://'):
            site = "http://" + site

        # Could sleep here to be nice
        # time.sleep(3)

        page = requests.get(site, headers=self.headers)

        self.soup = BeautifulSoup(page.content)

        # Course stuff
        self.next_page = self.get_next_page()
        self.title = self.get_title()
        self.href = self.get_href()
        self.course_url = self.get_url()
        self.course_code = self.get_course_code()
        self.course_plan = self.get_course_plan()
        self.intro_text = self.get_entry_content()
        self.latest_post_url = self.get_latest_post_url()
        self.latest_post_title = self.get_latest_post_title()
        self.latest_post_author = self.get_latest_post_author()
        self.latest_post_time = self.get_latest_post_time()

        # Program stuff
        self.program_urls = self.get_program_urls()

    def get_next_page(self):
        """
        Get the pagination, get our next pages.
        """
        try:
            links = self.soup.findAll('a', {'class': 'next'})
            links = links[0]['href']
        # If there is no 'next' link found just return ""
        except IndexError:
            return ""
        return links

    def get_course_code(self):
        """
        Get our course codes available.
        """
        try:
            codes = self.soup.find(
                'div', {'id': 'header-wrapper'}).find('ul').findAll('li')[2].get_text()
        except Exception, e:
            return ""
        return codes

    def get_entry_content(self):
        """
        Get our intro text for our courses.
        """
        try:
            entries = self.soup.find(
                'div', {'class': 'entry-content'}).find('p').get_text()
        except Exception, e:
            return ""
        return entries

    def get_title(self):
        """
        Get the title of our courses.
        """
        try:
            titles = self.soup.find(
                'div', {'id': 'header-wrapper'}).find('h1').get_text()
        except Exception, e:
            return ""
        return titles

    def get_url(self):
        """
        Get the url of our courses.
        """
        try:
            urls = self.soup.find(
                'div', {'id': 'header-wrapper'}).find('h1').find('a').get('href')
        except Exception, e:
            return ""
        return urls

    def get_course_plan(self):
        """
        Get our course plan for the courses.
        """
        url = ''
        try:
            planUrl = self.soup.find('ul', {'class': 'sub-menu'}).findAll('li')
            for aurl in planUrl:
                tempUrl = aurl.find('a').get_text()
                # Get only the urls that has "Kursplan" in them
                if "Kursplan" in tempUrl:
                    url = aurl.find('a').get('href')
        except Exception, e:
            return ""
        return url

    def get_latest_post_url(self):
        posts = []
        try:
            ul = self.soup.find(
                'ul', {'class': 'item-list'}).findAll('div', {'class': 'meta'})
            for post_url in ul:
                for anchor in post_url.findAll('a'):
                    posts.append(anchor.get('href'))
        except Exception, e:
            return ""
        return posts

    def get_latest_post_author(self):
        try:
            authors = self.soup.find(
                'p', {'class': 'entry-byline'}).find('strong').get_text()
        except Exception, e:
            return ""
        return authors

    def get_latest_post_time(self):
        try:
            text = self.soup.find('p', {'class': 'entry-byline'}).get_text()
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', text)
            date = match.group()
        except Exception, e:
            return ""
        return date

    def get_latest_post_title(self):
        try:
            title = self.soup.find('h1', {'class': 'entry-title'}).get_text()
        except Exception, e:
            return ""
        return title

    def get_program_urls(self):
        """
        Get all the programs hrefs which we will fetch later on.
        """
        ul = self.soup.find('ul', {'class': 'item-list'})
        hrefs = []
        try:
            for title in ul.findAll('div', {'class': 'item-title'}):
                for anchor in title.findAll('a'):
                    # Get only the one with "program" in the url
                    if "/program/" in anchor.get('href'):
                        hrefs.append(anchor.get('href'))
        except Exception, e:
            pass
        return hrefs

    def get_href(self):
        """
        Get all the courses hrefs which we will fetch later on.
        """
        ul = self.soup.find('ul', {'class': 'item-list'})
        hrefs = []
        try:
            for title in ul.findAll('div', {'class': 'item-title'}):
                for anchor in title.findAll('a'):
                    # Get only the one with "kurs" in the url
                    if "kurs" in anchor.get('href'):
                        hrefs.append(anchor.get('href'))
        except Exception, e:
            pass
        return hrefs

    def date_handler(self, obj):
        """
        Handler for saving dates as JSON.
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj
