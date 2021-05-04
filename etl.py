import os
import glob
import psycopg2
from psycopg2 import Error
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    
    # open song file
    # FROM: https://knowledge.udacity.com/questions/459063
    df = pd.read_json(filepath, lines = True)

    # insert song record
    # FROM: https://knowledge.udacity.com/questions/97110
    # FROM: https://zetcode.com/python/psycopg2/
    for rIndex, row in df.iterrows():
        
        # Get Song Data
        song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[rIndex].tolist()
        # Try insercting the song data
        try:
            cur.execute(song_table_insert, song_data)
        # Ensure the exectution of the insertion was succesful
        except Error as e:
            print(e)
        
        # insert artist record
        # FROM: https://knowledge.udacity.com/questions/97110
        # FROM: https://zetcode.com/python/psycopg2/
        # query = "INSERT INTO cars (id, name, price) VALUES (%s, %s, %s)"
        # cur.executemany(query, cars)
        artist_data = df[['artist_id', 
                          'artist_name', 
                          'artist_location',
                          'artist_latitude', 
                          'artist_longitude']].values[rIndex].tolist()
        # Try insercting the artist data
        try:
            cur.execute(artist_table_insert, artist_data)
        # Ensure the exectution of the insertion was succesful
        except Error as e:
            print(e)

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines = True) 

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    # FROM: https://knowledge.udacity.com/questions/543309
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df.copy()
    
    # insert time data records
    # we have to data files (df and t), which are version of the same file
    # ONE merely has its contents correctly converted to datetime format
    time_data = [
        df.ts.values, 
        t.dt.hour.values, 
        t.dt.day.values,
        t.dt.weekofyear.values, 
        t.dt.month.values, 
        t.dt.year.values,
        t.dt.weekday.values
    ]
    
    column_labels = ["start_time", "hour", "day", "week", "month", "year", "weekday"]
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except Error as e:
            print(e)

    # load user table
    user_df = df[["userId", "firstName","lastName", "level", "gender", "location"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()
        except Error as e:
            print(e)
            results = None
        
        if results:
            songid, artistid = results
            # Confirm what has been said here:
            # https://knowledge.udacity.com/questions/142826
            print ("--------------------------")
            print ("FOUND AN ARIST AND SONG IT")
            print ("--------------------------")
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except Error as e:
            print(e)

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        print(datafile)
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    
    import create_tables
    create_tables.main()
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()