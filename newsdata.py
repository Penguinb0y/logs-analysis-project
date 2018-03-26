# "Python Code" for news-analysis-project that
# communicates with the newsdata.sql database


import psycopg2

# define database
DBNAME = "news"


# Return output of the top viewed articles
def top_three_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    print("\nThe top three most viewed articles are: \n")
    query = """
        select articles_views.title, articles_views.views
        from articles_views
        limit 3;
        """
    c.execute(query)
    results = c.fetchall()
    # Reformat print output
    for results in results[:3]:
        print(" \"{:}\" " " -- {:} views\n".format(results[0], results[1]))
    db.close()
    return None


# Return output of the top viewed authors
def top_three_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
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
    c.execute(query)
    results = c.fetchall()
    # Reformat print output
    for results in results[:3]:
        print("{:} -- {:} total views\n".format(results[0], results[1]))
    db.close()
    return None


# Return output of the error percentage above one percent
def error_percentages():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    print("\nThe day(s) where more than 1% of requests lead to errors were:\n")
    query = """
        select date, error_percentage
        from error_request_percentages
        where error_percentage >= 1;
        """
    c.execute(query)
    results = c.fetchall()
    # Reformat print output
    for results in results[:3]:
        print("{:} -- {:}%\n".format(results[0], results[1]))
    db.close()
    return None


# Run functions
top_three_articles()
print("-----------------------------------------------\n")
top_three_authors()
print("-----------------------------------------------\n")
error_percentages()
