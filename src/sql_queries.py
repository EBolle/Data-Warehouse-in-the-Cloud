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
    year int
);
"""

songplays_table_create = """
"""

users_table_create = """
CREATE TABLE users (
    userid int primary key,
    first_name text,
    last_name text,
    gender text,
    level text
);
"""

songs_table_create = """
"""

artists_table_create = """
"""

time_table_create = """
"""

# STAGING TABLES

staging_events_copy = f"""
COPY staging_events FROM {LOG_DATA}
CREDENTIALS 'aws_iam_role={ARN}'
REGION 'us-west-2'
JSON 'auto ignorecase';
"""

staging_songs_copy = f"""
COPY staging_events FROM {SONG_DATA}
CREDENTIALS 'aws_iam_role={ARN}'
REGION 'us-west-2'
JSON 'auto ignorecase';
"""

# FINAL TABLES

songplays_table_insert = """
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
"""

artists_table_insert = """
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

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplays_table_create,
                        users_table_create, songs_table_create, artists_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplays_table_drop, users_table_drop,
                      songs_table_drop, artists_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplays_table_insert, users_table_insert, songs_table_insert, artists_table_insert,
                        time_table_insert]
