# README
This is a project designed to implement SQL database skills from the command line and my own code (Python) as internal reporting tools. The Python script uses psycopg2 to query a mock PostgreSQL database for a fictional news website in order to mimic drawing business conclusions from data. 

The mock news database is a large database with over a million rows that that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

The news database consists of three databases: `authors`, `articles`, and `logs`. I used thesed these three databases in SQL to answer three questions:
* What are the most popular three articles of all time? 
* Who are the most popular article authors of all time? 
* On which days did more than 1% of requests lead to errors?

## System Requirements
* VirtualBox 
(Build 5.1 or older; newer versions than that are INCOMPATIBLE)
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
* Vagrant
https://www.vagrantup.com/downloads.html
* A unix-style terminal

VirtualBox is the program that runs your Linux virtual machine and Vagrant is the program that will download a Linux operating system and run it inside the virtual machine. (All of which will be done through a terminal.)

Provided in the logs-analysis-project folder are these files:
* `newsdata.py`
* `output.txt`
* `README.md`
* `vagrantfile`

# Directions
1. On a terminal, `cd` to the `logs-analysis-project` so it's now the working directory.
2. With `logs-analysis-project` as your working directory on your terminal, run the command `$ vagrant up` to have a PostgreSQL server running in a Linux Virtual Machine.
3. When the shell prompt is back, run the command `$ vagrant ssh` to log in to the newly installed VM. (The vagrant directory)
4. When logged into vagrant, `cd` into `/vagrant` which is the folder shared with your virtual machine
5. Download the file `newsdata.sql` which is provided in a zip file in the provided link: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
6. Unzip the file and extract `newsdata.sql` into the vagrant directory
7. On the vagrant directory, use this command to load the data: `psql -d news -f newsdata.sql`
(Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.)
8. ##### (Only needed to be run the first time) Manually add the views with the statements (separately) from the "Created Views" section below
9. Finally, run the command: `python newsdata.py` which should print the results on the terminal
(The desired results should be identical to `output.txt` file)

# Created Views
You must add these views to the news database before running the python script for the first time. (Reference to Number 8 in the Directions.)

To do so: 
1) Run the command: `psql news`
2) Copy and paste the provided statement to the terminal.
3) Press enter.
4) Repeat steps 2 and 3 for all the provided views.
### `articles_views`
```sql
CREATE view articles_views AS 
SELECT
    MAX(articles.author) AS authors_id,
    articles.title,
    COUNT(*) AS views 
FROM
    articles,
    log 
WHERE
    log.path = concat('/article/', articles.slug) 
GROUP BY
    articles.title 
ORDER BY
    views DESC;
```

### ```request_attempts```
```sql
CREATE view request_attempts AS 
SELECT
    TIME::DATE AS DATE,
    COUNT(status) AS total_requests 
FROM
    log 
WHERE
    status = '200 OK' 
    OR status = '404 NOT FOUND' 
GROUP BY
    DATE 
ORDER BY
    DATE ASC;
```

### ```error_request_attempts```
```sql
CREATE view error_request_attempts AS 
SELECT
    TIME::DATE AS DATE,
    COUNT(status) AS error_total 
FROM
    log 
WHERE
    status = '404 NOT FOUND' 
GROUP BY
    DATE 
ORDER BY
    DATE ASC;
```

### ```error_percentages```
```sql
CREATE view error_percentages AS 
SELECT
    r.DATE,
    round(MAX(e.error_total::NUMERIC / r.total_requests::NUMERIC) * 100, 2) AS error_percentage 
FROM
    error_request_attempts e,
    request_attempts r
WHERE
    e.DATE = r.DATE 
GROUP BY
    r.DATE 
ORDER BY
    r.DATE ASC;
```
