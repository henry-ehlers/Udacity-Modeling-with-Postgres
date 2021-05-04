# Udacity Nanodegree "Data Engineering" - Project #1 - Modeling with Postgres

## Introduction

"A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results."
  
  \- as described by Udacity
  
## The Project

"In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL. "

  \- as described by Udacity

## How to Run

- In order to run this particular project you will need to utilize `Python 3`, as well as the two Python libraries `pandas`, `psycopg2`, `os`, `glob`, and `sql_queries`. 
- Actually running the project is as simply as calling `python etl.py` from the command line. The required module `create_tables.py` is called automatically from within the `etl.py` script.

## The Database

The database presented here consists of 4 dimension tables (`songs`, `artists`, `users`, and `time`), and 1 fact table `songplayes`, arranged in a 'Star Schema'. The foreign keys contained within the songplays table allow for a lookups in their respective dimension tables. As described by the Udacity Nanodegree in Lesson #2 Section #19 - 'Benefits of Star Schemas', such 'Star Schemas' offer fast aggregrations, and simplified queries, owing to their denormalized structure. Here, I hope to briefly describe the make-up of this database, an the fields contained within the aformentioned five tables.

### Songs Table

A table containing the unique songs listened to by users of Sparkify. The primary key (`song_id varchar`) field allows for lookups of a particular song's `title varchar`, an artist's unique `artist_id varchar` (which functions as a foreign key), the `year int` a song was published, and the song's `duration int`. 

### Artists Table

A table containing the unique artists listened to bu users of Sparkify. The primary key (`artist_id varchar`) allows for lookups of a particular artist's `name varchar`, their `location varchar`, and their `latitude int` and `longitude int`. 

### Time Table

A table which contains data describing when a user logged onto the Sparkify service. The unique key of this table (`start_time bigint`) allows for the lookup of that starttime's `hour int`, `day int`, `week int`, `month int`, `year int`, and `weekday int`.

### Users Table

A table containing unique users of the Sparkify service. As such the primary key (`user_id varchar`) links to a users' `first_name varchar`, `last_name varchar`, `gender varchar`, `location varchar` (not to be confused with the artist's location), and `level varchar` (note: level describes what payment plan they are on, such as 'free' or 'paid').

### SongPlays Table

Finally, the fact table around which this 'Star Schema' is based, contains information on which song, created by which artists, were listened to by which user, at what starting time. The primary key `songplay_id serial` is merely an integer which increases in value as entries are added. Each such entry links to a unique `user_id`, `song_id`, `start_time`, and `artist_id`. In addition, the table contains columns on the particular user's `level`, the user's `session_id` and `user_agent`, as well as the artist's `location`. The choice to denormalize this table to (redundantly) include `level` and `location` allows for faster queries of particular lookups relating to these fields.
