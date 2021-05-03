# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop     = "DROP TABLE IF EXISTS users"
song_table_drop     = "DROP TABLE IF EXISTS songs"
artist_table_drop   = "DROP TABLE IF EXISTS artists"
time_table_drop     = "DROP TABLE IF EXISTS times"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int PRIMARY KEY
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY,
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration numeric
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,
    artist_name varchar NOT NULL,
    artist_location varchar,
    artist_latitude numeric,
    artist_longitude numeric
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time numeric NOT NULL
);
""")


# INSERT RECORDS

songplay_table_insert = ("""

""")

user_table_insert = ("""
""")

song_table_insert = ("""
INSERT INTO songs 
    (song_id, title, artist_id, year, duration) 
        VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) 
        DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists
    (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) 
        VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id)
        DO NOTHING;
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]