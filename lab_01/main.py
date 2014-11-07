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
    CACHE_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATA_FILE_NAME = 'data.json'

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

    try:
        with open(global_data.DATA_FILE_NAME) as dataFile:
            jsonData = json.load(dataFile)
        lastFetched = jsonData[-1].values()[0]
        lastFetched = datetime.datetime.strptime(lastFetched, global_data.CACHE_DATETIME_FORMAT)
    except Exception, e:
        lastFetched = None

    if lastFetched is None or lastFetched < datetime.datetime.now() - datetime.timedelta(minutes = 5):
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
                print 'Senaste post titel: %s' % scraper.latestPostTitle if scraper.latestPostTitle else 'No latest title information'
                print 'Senaste post skribent: %s' % scraper.latestPostAuthor if scraper.latestPostAuthor else 'No latest author information'
                print 'Senaste post datum: %s' % scraper.latestPostTime if scraper.latestPostTime else 'No latest date information'

            # Append our data to the list
            data.append({
                'course_code': scraper.courseCode if scraper.courseCode else 'No course code information',
                'title': scraper.title if scraper.title else 'No title information',
                'course_url': scraper.courseUrl if scraper.courseUrl else 'No url information',
                'course_plan': scraper.coursePlan if scraper.coursePlan else 'No course plan information',
                'intro_text': scraper.introText if scraper.introText else 'No intro information',
                'latest_post_title': scraper.latestPostTitle if scraper.latestPostTitle else 'No latest title information',
                'latest_post_author': scraper.latestPostAuthor if scraper.latestPostAuthor else 'No latest author information',
                'latest_post_date': scraper.latestPostTime if scraper.latestPostTime else 'No latest date information',
                'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
            })

            if scraper.nextPage:
                # Then fetch all the pages
                queue += ["http://coursepress.lnu.se%s" % (scraper.nextPage)]

        print "*** Done scrapping!"
        print "*** Saving data..."

        # Get the number of courses fetched
        data.append({'count': len(data)})
        data.append({'last_fetch': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT)})

        # Save the data to file
        with open(global_data.DATA_FILE_NAME, 'w') as outfile:
            json.dump(data, outfile, default=scraper.date_handler, indent=True, encoding='utf-8')
        time.sleep(1)
        print "*** Done saving"
    else:
        print "We still have some cached data, check '%s'" % global_data.DATA_FILE_NAME
