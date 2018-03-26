# README
My log-analysis-project by Jonathan Samonte

##### System Requirements
* VirtualBox
* Vagrant
* Python 2.7
* FSND-Virtual-Machine
* ```newsdata.sql```

(Note: ```newsdata.sql``` is needed as the sql database which is connected to the vagrant VM and is not provided in the folder)

Provided in the logs-analysis-project folder are these files:
* ```newsdata.py```
* ```output.txt```
* ```README.md```


## Directions
Run ```newsdata.py``` on the vagrant shell with the python command. The expected outputs of the file should be identical to ```output.txt```


# Created Views
Here are the views that I added into the newsdata.sql database by using the ```create view``` command in psql:

(Note: If you wish to know more about these views, you can start off by running this statement in the psql news database:
```
select * from (INSERT_VIEW_TITLE);
```
and then explore from there.)

### ```articles_views```
```articles_views``` is used to answer Questions 1 & 2
```sh
select max(articles.author) as authors_id, articles.title, count(*) as views
from articles, log
where log.path = concat('/article/',articles.slug)
group by articles.title
order by views desc;
```

### ```error_status_by_date```
```error_status_by_date``` is (indirectly) used to answer Question 3
```sh
select time::date as date, count(status) as error_total
from log
where status = '404 NOT FOUND'
group by date
order by date asc;
```

### ```success_status_by_date```
```success_status_by_date``` is (indirectly) used to answer Question 3
```sh
select time::date as date, count(status) as success_total
from log
where status = '200 OK'
group by date
order by date asc;
```

### ```error_request_percentages```
```error_request_percentages``` is used to answer Question 3 by utilizing the ```error_status_by_date``` view and the ```success_status_by_date``` view
```sh
select success_status_by_date.date,
    max(error_status_by_date.error_total) as error_total,
    max(success_status_by_date.success_total) as success_total,
    round(max(error_status_by_date.error_total:: numeric/ success_status_by_date.success_total::numeric) * 100,2) as error_percentage
from error_status_by_date, success_status_by_date
where error_status_by_date.date = success_status_by_date.date
group by success_status_by_date.date
order by success_status_by_date.date asc;
```
