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
    nextPage = ''
    courseDetail = ''
    courseCode = ''
    courseUrl = ''
    coursePlan = ''
    introText = ''

    headers = {
        'User-Agent': 'Ghost',
        'From': 'jh222xk@student.lnu.se'
    }

    def date_handler(self, obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def scrape(self, site):
        """
        Scrapes a given url and parses the information
        """
        if not site.startswith('http://') or site.startswith('https://'):
            site = "http://" + site

        # Could sleep here to be nice
        #time.sleep(3)

        page = requests.get(site, headers=self.headers)

        self.soup = BeautifulSoup(page.content)
        self.nextPage = self.getNextPage()
        self.title = self.getTitle()
        self.href = self.getHref()
        self.courseUrl = self.getUrl()
        self.courseCode = self.getCourseCode()
        self.coursePlan = self.getCoursePlan()
        self.introText = self.getEntryContent()

    def getNextPage(self):
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

    def getCourseCode(self):
        """
        Get our course codes available.
        """
        try:
            codes = self.soup.find('div', {'id': 'header-wrapper'}).find('ul').findAll('li')[2].get_text()
        except Exception, e:
            return ""
        return codes

    def getEntryContent(self):
        """
        Get our intro text for our courses.
        """
        try:
            entries = self.soup.find('div', {'class': 'entry-content'}).find('p').get_text()
        except Exception, e:
            return ""
        return entries

    def getTitle(self):
        """
        Get the title of our courses.
        """
        try:
            titles = self.soup.find('div', {'id': 'header-wrapper'}).find('h1').get_text()
        except Exception, e:
            return ""
        return titles

    def getUrl(self):
        """
        Get the url of our courses.
        """
        try:
            urls = self.soup.find('div', {'id': 'header-wrapper'}).find('h1').find('a').get('href')
        except Exception, e:
            return ""
        return urls

    def getCoursePlan(self):
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

    def getHref(self):
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
