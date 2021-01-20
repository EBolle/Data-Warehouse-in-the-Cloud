from settings import ARN, LOG_DATA, SONG_DATA


# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplays_table_drop = "DROP TABLE IF EXISTS songplays;"
users_table_drop = "DROP TABLE IF EXISTS users;"
songs_table_drop = "DROP TABLE IF EXISTS songs;"
artists_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create = """
CREATE TABLE staging_events (
    artist text,
    auth text,
    firstName text,
    gender text,
    itemInSession int,
    lastName text,
    length real,
    level text,
    location text,
    method text,
    page text,
    registration real,
    sessionId int,
    song text,
    status int,
    ts bigint NOT NULL sortkey,
    userAgent text,
    userId text)
diststyle even
;
"""

staging_songs_table_create = """
CREATE TABLE staging_songs (
    num_songs int,
    artist_id text,
    artist_latitude real,
    artist_longitude real,
    artist_location text,
    artist_name text,
    song_id text,
    title text,
    duration real,
    year int)
diststyle even 
;
"""

songplays_table_create = """
CREATE TABLE songplays (
    songplay_id int identity(0, 1) PRIMARY KEY,
    start_time date sortkey,
    user_id int,
    level text,
    song_id text,
    artist_id text,
    session_id int,
    location text,
    user_agent text)
diststyle even
;
"""

users_table_create = """
CREATE TABLE users (
    user_id int primary key,
    first_name text,
    last_name text,
    gender text,
    level text)
diststyle all;
"""

songs_table_create = """
CREATE TABLE songs (
    song_id text primary key,
    title text,
    artist_id text,
    year int,
    duration real)
diststyle all
;
"""

artists_table_create = """
CREATE TABLE artists (
    artist_id text primary key,
    name text,
    location text,
    latitude real,
    longitude real)
diststyle all
;
"""

time_table_create = """
CREATE TABLE time (
    start_time date primary key sortkey,
    hour int,
    day int,
    week int,
    month int,
    year int,
    weekday boolean)
diststyle even
;
"""

# STAGING TABLES

staging_events_copy = f"""
COPY staging_events FROM '{LOG_DATA}'
CREDENTIALS 'aws_iam_role={ARN}'
REGION 'us-west-2'
JSON 'auto ignorecase'
;
"""

staging_songs_copy = f"""
COPY staging_songs FROM '{SONG_DATA}'
CREDENTIALS 'aws_iam_role={ARN}'
REGION 'us-west-2'
JSON 'auto ignorecase'
;
"""

# FINAL TABLES

songplays_table_insert = """
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT timestamp 'epoch' + CAST(events.ts AS BIGINT)/1000 * interval '1 second' AS start_time 
,    cast(events.userid as int) as user_id
,    events.level
,    songs.song_id
,    artists.artist_id
,    events.sessionid as session_id
,    events.location
,    events.useragent as user_agent

FROM
    staging_events as events
    left join artists on artists.name=events.artist
    left join songs on songs.title=events.song and songs.duration=events.length

WHERE
    events.page='NextSong'
;
"""

users_table_insert = """
INSERT INTO users 
SELECT cast(userid as int) 
,    firstname
,    lastname
,    gender
,    level

FROM
    (
    SELECT userid
    ,    firstname
    ,    lastname
    ,    gender
    ,    level
    ,    row_number() over (partition by userid order by ts desc) as row_number_ts_desc

    FROM
        staging_events

    WHERE
        userid != ''
    )

WHERE
    row_number_ts_desc = 1 
;
"""

songs_table_insert = """
INSERT INTO songs 
SELECT song_id
,    title
,    artist_id
,    year
,    duration

FROM
    staging_songs
;
"""

artists_table_insert = """
INSERT INTO artists
SELECT artist_id 
,    max(artist_name) as artist_id
,    max(artist_location) as location
,    max(artist_latitude) as latitude
,    max(artist_longitude) as longitude

FROM
    staging_songs

GROUP BY
    artist_id
;
"""

time_table_insert = """
SELECT timestamp as start_time
,    extract(hour from timestamp) as hour
,    extract(day from timestamp) as day
,    extract(week from timestamp) as week
,    extract(month from timestamp) as month
,    extract(year from timestamp) as year
,    case when extract(weekday from timestamp) between 1 and 5 then TRUE else FALSE end as weekday

FROM
    ( 
    SELECT DISTINCT timestamp 'epoch' + CAST(ts AS BIGINT)/1000 * interval '1 second' AS timestamp 

    FROM
        staging_events
     
    WHERE
        page='NextSong'
    )
;  
"""

# QUERY LISTS, make sure songplays_table_insert is the last item of the list

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplays_table_create,
                        users_table_create, songs_table_create, artists_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplays_table_drop, users_table_drop,
                      songs_table_drop, artists_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [users_table_insert, songs_table_insert, artists_table_insert, time_table_insert,
                        songplays_table_insert]
