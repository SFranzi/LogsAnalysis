# Logs Analysis 
*Internal reporting tool for a newspaper site*

This tool is used to analyse data gathered by a newspaper site. The database consists of the tables authors, articles and log. The log table describes when which article was accessed by a user online. 

### Tech Stack 

The LogsAnalysis project requires the following tech stack:

- [Python]('https://www.python.org/downloads/')
- [PostgreSQL (RDBMS)]('https://www.postgresql.org/download/')
- [Oracle Virtual Box]('https://www.virtualbox.org/wiki/Downloads')
- [Vagrant]('https://www.vagrantup.com/') 

### Program Design 

The reporting tool answers 3 questions sequentially by analysing the data stored in the PostgreSQL database. 

The questions are: 
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The program executes the following way: 

- Connects to the database 
- Defines a database cursor 
- Executes the SQL query
- Fetches the query result 
- Closes the database connection
- Iterates through and prints the result

### Installation and use

##### Install vagrant and run virtual machine
In the projects directory run 
```
$ vagrant init bento/ubuntu-16.04
```
Start virtual machine by running 

```
$ vagrant up
```
Log into virtual machine by 

```
$ vagrant ssh
```

##### Connect to the news database

```
$ psql -d news 
```

##### Create the views 
**top_articles**
This view shows the columns author, title and views of the tables log and articles. Views is the number of times one article title was read online. It is sorted from top to bottom regarding number of views.
```
create view top_articles as select author, title, count(*) as views from log, articles where articles.slug = substring(log.path,10) group by articles.title, articles.author order by views desc;
```

**requests_per_day**
This view shows the number of requests made per day.
```
create view requests as select time::date as date, count(*) as requests_per_day from log group by date;
```

**errors_per_day**
This view shows the number of requests that resulted in errors per day.
```
create view errors as select time::date as date, count(*) as errors_per_day from log where log.status = '404 NOT FOUND' group by date; 
```

### Run

``` 
$ cd /vagrant/LogsAnalysis
$ python news.py
```

To exit the Postgres shell type **Ctrl + d**