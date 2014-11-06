#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import argparse
import sys
import json
import datetime
import time

from ghost import Ghost

class global_data:
    DEBUG = False

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description=
        """
            Fetches a site and scrapes some information
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument(
        "-u", "--url", default=Ghost.url, help="Simply provide the url you want to fetch.")
    args = arg_parser.parse_args()

    queue = list()
    queue.append(args.url)

    data = list()

    print "*** Scrapping, please wait..."

    # Fetch as long as queue is not empty
    while len(queue) > 0:
        scraper = Ghost()

        # Get item from head of list
        scraper.scrape(queue.pop(0))
        # Add our new urls to the queue
        queue += scraper.href

        # Debugging
        if global_data.DEBUG:
            print 'Coursecode: %s' % scraper.courseCode if scraper.courseCode else 'No course code information'
            print 'Title: %s' % scraper.title if scraper.title else 'No title information'
            print 'URL: %s' % scraper.courseUrl if scraper.courseUrl else 'No url information'
            print 'Courseplan: %s' % scraper.coursePlan if scraper.coursePlan else 'No course plan information'
            print 'Ledtext: %s' % scraper.introText if scraper.introText else 'No intro information'

        # Append our data to the list
        data.append({
            'course_code': scraper.courseCode if scraper.courseCode else 'No course code information',
            'title': scraper.title if scraper.title else 'No title information',
            'course_url': scraper.courseUrl if scraper.courseUrl else 'No url information',
            'course_plan': scraper.coursePlan if scraper.coursePlan else 'No course plan information',
            'intro_text': scraper.introText if scraper.introText else 'No intro information',
            'timestamp': datetime.datetime.now() if datetime.datetime.now else 'Timestamp failed'
        })

        if scraper.nextPage:
            # Then fetch all the pages
            queue += ["http://coursepress.lnu.se%s" % (scraper.nextPage)]

    print "*** Done scrapping!"
    print "*** Saving data..."

    # Get the number of courses fetched
    data.append({'count': len(data)})

    # Save the data to file
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, default=scraper.date_handler, indent=True, encoding='utf-8')
    time.sleep(1)
    print "*** Done saving"
