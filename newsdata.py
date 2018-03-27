#!/usr/bin/env python
#
# code outputs: top viewed articles, authors, and error request percentages
# from the news database using psql queries

import psycopg2

DBNAME = "news"


def execute_query(query):
    """Takes query statement as parameter and reutrns results"""
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def top_three_articles():
    """Return output of the top viewed articles"""
    print("\nThe top three most viewed articles are: \n")
    query = """
        select articles_views.title, articles_views.views
        from articles_views
        limit 3;
        """
    results = execute_query(query)
    for result in results:
        print("\t\"{:}\" " " -- {:} views\n".format(result[0], result[1]))
    return None


def top_three_authors():
    """Return output of the top viewed authors"""
    print("\nThe top three most viewed authors are: \n")
    query = """
        select max(authors.name) as author,
        sum(articles_views.views) as total_views
        from articles_views
        join authors
        on articles_views.authors_id = authors.id
        group by authors.id
        limit 3;
        """
    results = execute_query(query)
    for result in results:
        print("\t{:} -- {:} total views\n".format(result[0], result[1]))
    return None


def error_percentages():
    """Return output of the error percentage above one percent"""
    print("\nThe day(s) where more than 1% of requests lead to errors were:\n")
    query = """
        select * from error_percentages
        where error_percentage >= 1;
        """
    results = execute_query(query)
    for result in results:
        print("\t{:} -- {:}%\n".format(result[0], result[1]))
    return None


def main():
    """Generate the reports!"""
    top_three_articles()
    top_three_authors()
    error_percentages()

if __name__ == '__main__':
    main()
