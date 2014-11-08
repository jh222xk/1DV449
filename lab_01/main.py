#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import argparse
import sys
import json
import datetime
import time

from ghost import Ghost


class SaveToJsonFile:

    def save_to_file(self, file_name, data):
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile, default=scraper.date_handler,
                      indent=True, encoding='utf-8')

    def read_file(self, file_name):
        with open(file_name) as dataFile:
            jsonData = json.load(dataFile)
        return jsonData


class global_data:
    DEBUG = False
    CACHE_MIN = 0
    CACHE_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    COURSE_DATA_FILE_NAME = 'course_data.json'
    PROGRAM_DATA_FILE_NAME = 'program_data.json'

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description="""
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
    program_data = list()

    try:
        with open(global_data.COURSE_DATA_FILE_NAME) as data_file:
            json_data = json.load(data_file)
        last_fetched = json_data[1].values()[0]
        last_fetched = datetime.datetime.strptime(
            last_fetched, global_data.CACHE_DATETIME_FORMAT)
    except Exception, e:
        last_fetched = None

    if last_fetched is None or last_fetched < datetime.datetime.now() - datetime.timedelta(minutes=global_data.CACHE_MIN):
        print "*** Scrapping, please wait..."

        # Fetch as long as queue is not empty
        while len(queue) > 0:
            scraper = Ghost()

            # Get item from head of list
            scraper.scrape(queue.pop(0))
            # Add our new urls to the queue
            queue += scraper.href

            # print len(queue)

            # Debugging
            if global_data.DEBUG:
                print 'Coursecode: %s' % scraper.course_code if scraper.course_code else 'No course code information'
                print 'Title: %s' % scraper.title if scraper.title else 'No title information'
                print 'URL: %s' % scraper.course_url if scraper.course_url else 'No url information'
                print 'Courseplan: %s' % scraper.course_plan if scraper.course_plan else 'No course plan information'
                print 'Ledtext: %s' % scraper.intro_text if scraper.intro_text else 'No intro information'
                print 'Senaste post titel: %s' % scraper.latest_post_title if scraper.latest_post_title else 'No latest title information'
                print 'Senaste post skribent: %s' % scraper.latest_post_author if scraper.latest_post_author else 'No latest author information'
                print 'Senaste post datum: %s' % scraper.latest_post_time if scraper.latest_post_time else 'No latest date information'

            # Append our data to the list
            data.append({
                'course_code': scraper.course_code if scraper.course_code else 'No course code information',
                'title': scraper.title if scraper.title else 'No title information',
                'course_url': scraper.course_url if scraper.course_url else 'No url information',
                'course_plan': scraper.course_plan if scraper.course_plan else 'No course plan information',
                'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
            })

            if scraper.next_page:
                # Then fetch all the pages
                queue += ["http://coursepress.lnu.se%s" % (scraper.next_page)]

            for program in scraper.program_urls:
                program_data.append({
                    'url': program,
                    'title': scraper.title
                })

        print "*** Done scrapping!"
        print "*** Saving data..."

        # Get the number of courses fetched
        data.append({'count': len(data)})
        data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Sort the list of dicts by title of the courses
        sortedList = sorted(data, key=lambda k: k.get('title'))

        # Save the data to file
        save_data = SaveToJsonFile()
        save_data.save_to_file(global_data.COURSE_DATA_FILE_NAME, sortedList)
        if program_data:
            save_data.save_to_file(
                global_data.PROGRAM_DATA_FILE_NAME, program_data)
        time.sleep(1)

        print "*** Done saving"
    else:
        print "We still have some cached data, check '%s'" % global_data.COURSE_DATA_FILE_NAME
