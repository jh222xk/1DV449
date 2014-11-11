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
    PROJECT_DATA_FILE_NAME = 'project_data.json'
    SUBJECT_DATA_FILE_NAME = 'subject_data.json'
    BLOG_DATA_FILE_NAME = 'blog_data.json'
    PERSONAL_DATA_FILE_NAME = 'personal_data.json'

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

    course_data = list()
    program_data = list()
    project_data = list()
    subject_data = list()
    blog_data = list()
    personal_data = list()

    personal = False

    try:
        with open(global_data.COURSE_DATA_FILE_NAME) as data_file:
            json_data = json.load(data_file)
        last_fetched = json_data[1].values()[0]
        last_fetched = datetime.datetime.strptime(
            last_fetched, global_data.CACHE_DATETIME_FORMAT)
    except Exception, e:
        last_fetched = None

    if last_fetched is None or last_fetched < datetime.datetime.now() - datetime.timedelta(minutes=global_data.CACHE_MIN):
        print "*** Scraping, please wait..."

        # Fetch as long as queue is not empty
        while len(queue) > 0:
            scraper = Ghost()

            # Get item from head of list which will be the current url
            # which we will scrape.
            current_url = queue.pop(0)

            print "*** Scraping %s" % current_url

            # Scrape it!
            scraper.scrape(current_url)

            # Add our new urls to the queue
            queue += scraper.href

            if "/kurs/" in current_url and personal == False:
                # Debugging
                if global_data.DEBUG:
                    print 'Coursecode: %s' % scraper.course_code if scraper.course_code else 'No course code information'
                    print 'Title: %s' % scraper.title if scraper.title else 'No title information'
                    print 'URL: %s' % scraper.url if scraper.url else 'No url information'
                    print 'Courseplan: %s' % scraper.course_plan if scraper.course_plan else 'No course plan information'
                    print 'Ledtext: %s' % scraper.intro_text if scraper.intro_text else 'No intro information'
                    print 'Senaste post titel: %s' % scraper.latest_post_title if scraper.latest_post_title else 'No latest title information'
                    print 'Senaste post skribent: %s' % scraper.latest_post_author if scraper.latest_post_author else 'No latest author information'
                    print 'Senaste post datum: %s' % scraper.latest_post_time if scraper.latest_post_time else 'No latest date information'

                # Append our data to the list
                course_data.append({
                    'course_code': scraper.course_code if scraper.course_code else 'No course code information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'url': scraper.url if scraper.url else 'No url information',
                    'course_plan': scraper.course_plan if scraper.course_plan else 'No course plan information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

            if scraper.program_urls:
                queue += scraper.program_urls

            if "/program/" in current_url:
                program_data.append({
                    'url': scraper.url if scraper.url else 'No url information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

            if scraper.project_urls:
                queue += scraper.project_urls

            if "/projekt/" in current_url:
                project_data.append({
                    'url': scraper.url if scraper.url else 'No url information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

            if scraper.subject_urls:
                queue += scraper.subject_urls

            if "/subject/" in current_url:
                subject_data.append({
                    'url': scraper.url if scraper.url else 'No url information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

            if scraper.blog_urls:
                queue += scraper.blog_urls

            if scraper.title.strip() in scraper.authors:
                blog_data.append({
                    'url': scraper.url if scraper.url else 'No url information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

            if scraper.next_page:
                # Then fetch all the pages
                queue += ["http://coursepress.lnu.se%s" % (scraper.next_page)]

            if not scraper.next_page and scraper.personal_course_url:
                queue += scraper.personal_course_url

            # Set personal to True only if...
            if "/medlemmar/" in current_url:
                personal = True

            # Fetch only the personal url if...
            if "/kurs/" in current_url and personal == True:
                personal_data.append({
                    'url': scraper.url if scraper.url else 'No url information',
                    'title': scraper.title if scraper.title else 'No title information',
                    'intro_text': scraper.intro_text if scraper.intro_text else 'No intro information',
                    'latest_post_title': scraper.latest_post_title if scraper.latest_post_title else 'No latest title information',
                    'latest_post_author': scraper.latest_post_author if scraper.latest_post_author else 'No latest author information',
                    'latest_post_date': scraper.latest_post_time if scraper.latest_post_time else 'No latest date information',
                    'timestamp': datetime.datetime.now().strftime(global_data.CACHE_DATETIME_FORMAT) if datetime.datetime.now else 'Timestamp failed'
                })

        print "*** Done scraping!"
        print "*** Saving data..."

        # Get the number of courses fetched
        course_data.append({'count': len(course_data)})
        course_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Get the number of programs fetched
        program_data.append({'count': len(program_data)})
        program_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Get the number of projects fetched
        project_data.append({'count': len(project_data)})
        project_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Get the number of subjects fetched
        subject_data.append({'count': len(subject_data)})
        subject_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Get the number of blogs fetched
        blog_data.append({'count': len(blog_data)})
        blog_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Get the number of personal courses fetched
        personal_data.append({'count': len(personal_data)})
        personal_data.append({'last_fetch': datetime.datetime.now().strftime(
            global_data.CACHE_DATETIME_FORMAT)})

        # Sort the list of dicts by title of the courses
        sorted_course_list = sorted(course_data, key=lambda k: k.get('title'))
        sorted_program_list = sorted(program_data, key=lambda k: k.get('title'))
        sorted_project_list = sorted(project_data, key=lambda k: k.get('title'))
        sorted_subject_list = sorted(subject_data, key=lambda k: k.get('title'))
        sorted_blog_list = sorted(blog_data, key=lambda k: k.get('title'))
        sorted_personal_list = sorted(personal_data, key=lambda k: k.get('title'))

        # Save the data to file
        save_data = SaveToJsonFile()
        save_data.save_to_file(global_data.COURSE_DATA_FILE_NAME, sorted_course_list)

        # Save program data
        if program_data:
            save_data.save_to_file(
                global_data.PROGRAM_DATA_FILE_NAME, sorted_program_list)

        if project_data:
            save_data.save_to_file(
                global_data.PROJECT_DATA_FILE_NAME, sorted_project_list)

        if subject_data:
            save_data.save_to_file(
                global_data.SUBJECT_DATA_FILE_NAME, sorted_subject_list)

        if blog_data:
            save_data.save_to_file(
                global_data.BLOG_DATA_FILE_NAME, sorted_blog_list)

        if personal_data:
            save_data.save_to_file(
                global_data.PERSONAL_DATA_FILE_NAME, sorted_personal_list)

        time.sleep(1)

        print "*** Done saving"
    else:
        print "We still have some cached data, check '%s'" % global_data.COURSE_DATA_FILE_NAME
