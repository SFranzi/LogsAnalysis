# !/usr/bin/env python3

import psycopg2

DBNAME = "news"

# VIEWS
# -------------------------------------------------------------------------------------------------------------------------------
# 1. top_articles
# 2. requests_per_day
# 3. errors_per_day

# --------------------------------------------------------------------------------------------------------------------------------
# 1. What are the most popular three articles of all time?
"""
Returns the most popular three articles by views from the 'database',
most popular first.
"""


def get_articles():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select title, count(*) from log, articles \
               where articles.slug = substring(log.path,10) \
               group by articles.title order by count desc limit 3;")
    articles = c.fetchall()
    db.close()
    for row in articles:
        print("* " + str(row[0]) + " -- " + str(row[1]) + " views")


# 2. Who are the most popular article authors of all time?
""" Returns the most popular authors by page views, most popular first """


def get_authors():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, sum(top_articles.views) \
               as total_views from authors, top_articles \
               where authors.id = top_articles.author group by authors.name \
               order by total_views desc;")
    authors = c.fetchall()
    db.close()
    for row in authors:
        print("* " + str(row[0]) + " -- " + str(row[1]) + " views")


# 3. On which days did more than 1% of requests lead to errors?
""" Returns the days and percent of errors of which are more than 1% """


def get_error_days():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select TO_CHAR(requests.date, 'dd-Mon-YYYY'), \
               (errors_per_day::float/requests_per_day) as error_rate \
               from requests, errors where requests.date = errors.date) \
               as error_table where error_rate > 0.01;")
    days = c.fetchall()
    db.close()
    for row in days:
        print("* " + str(row[0]) + " -- " +
              str(round(row[1] * 100, 2)) + "% errors")


if __name__ == '__main__':

    print "\n"
    print "THE TOP 3 ARTICLES ARE:" 
    print "\n"
    get_articles()
    print "\n"
    print "TOP AUTHORS ARE:"
    print "\n"
    get_authors()
    print "\n"
    print "DAY WHERE MORE THAN 1 PERCENT LEAD TO ERRORS:"
    print "\n"
    get_error_days()
    print "\n"
