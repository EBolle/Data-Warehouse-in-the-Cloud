## Who doesn't want to be on cloud nine?

<img src="https://images.pexels.com/photos/2909083/pexels-photo-2909083.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=200">

Source: https://www.pexels.com

### Why Redshift
Due to the exponential growth of Sparkify they decided to move their data once more. Not only is speed of the essence,
but scalability and flexibility as well. By implementing Redshift they gain several advantages:
- Very fast querying performance due to Massively Parallel Processing, even with enormous amounts of data
- Easy to scale, in a matter of minutes one can launch additional clusters to increase storage and performance
- It is secure, no need to worry about security or hire very costly specialists

For more information and as a resource please have a look [here](https://www.sisense.com/blog/5-advantages-using-redshift-data-warehouse/).

Due to the switch of data warehouse several adjustments to the data definition and manipulation has been made.

### How the data flows

Raw .json that reside on a Amazon S3 are first inserted into 2 staging tables on Redshift. These staging tables are then
transformed and loaded into a 4 dimension tables and 1 fact table, following a typical star schema.

#### Staging tables

- staging_events
- staging_songs

Both staging events are distributed evenly, since they are mostly queried without additional joins. Hence, by evenly
distributing the data across all the nodes we gain better performance. Since the order of the timestamp (ts) variable
in staging_events is used in a insertion query, and we expect this order to relevant for possible future tables, we 
added a sortkey.
 


- NOTE:: only artists should have a all distribution, I expect - in a real life application - that users, time
on timestamp level, and songs perhaps change to often? nah... songs should be included as well.. users depends
on the popularity but should be fine all ->> timestamp NOT since it is related to the user activity, is always
unique and can quickly expand.

Run the scripts,  and create a simple interactive dashboard
with streamlit, cool! Adjust the README with decent 

### The star schema

The dimension tables users, songs, and artists are fully copied to each node using the all distribution strategy.
There are 2 reasons for this:
- they are relatively small
- they are not expected to have very large and frequent upserts, at least not in comparison to time and songplays

The dimension table time is evenly distributed and has a sorted primary key since it is a direct derivative of the fact 
table. Since it holds an actual timestamp of an event there is no limit to the number of possible rows. Since we expect
Sparkify to keep growing we need to evenly distribute the data to stay keep acceptable speed.

Naturally, the fact table is evenly distributed due to its size, expected large and frequent upserts, as well as the
possibility to be queried without joins. 

<img src="https://user-images.githubusercontent.com/49920622/103062485-97e62300-45ae-11eb-908d-4f27cca6f2a6.png">

### Streamlit 

### Example queries

- What are the differences in activity during the week? 

```sql
SELECT time.weekday
,    count(*) as n_songs_played
,    count(distinct sp.user_id) as n_unique_users
,    count(*) / count(distinct sp.user_id) as songs_per_user
,    count(*) / sum(count(*)) over () as perc_total_songs_played

FROM
    songplays as sp
    inner join time on time.start_time = sp.start_time
    
GROUP BY
    time.weekday
```

- Is there a difference in behaviour between paid and free users?

```sql
SELECT level
,    count(*) as n_songs_played
,    count(distinct user_id) as n_unique_users
,    count(*) / count(distinct user_id) as songs_per_user
,    count(*) / sum(count(*)) over () as perc_level

FROM
    songplays
    
GROUP BY
    level
```

- What is the gender distribution of our users, and are their differences in their activity?

```sql
SELECT users.gender
,    count(*) as n_songs_played
,    count(distinct sp.user_id) as n_unique_users
,    count(*) / sum(count(*)) over () as perc_songs_played

FROM
    songplays as sp
    inner join users on users.user_id = sp.user_id
    
GROUP BY
    users.gender
```

### Instructions

instructions on setting up a cluster and opening a port.

Before you can run the notebook and scripts, there are a few things you need to do:
- create and activate a virtual environment
- create a .env file and set your credentials

Furthermore, note that the logic needed to execute either the scripts or the notebook is stored in the /src folder.
The Python version used for this project is 3.8.5. 

#### create and activate a virtual environment 

You can either use Anaconda or venv to create the virtual environment. Regardless of your choice, you have to open
a (Anaconda) prompt, clone the project, and navigate to the project folder. Next, enter the following:

##### Anaconda
```bash
conda env create -f environment.yml
conda activate redshift
```

##### venv
```bash
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt 
```

#### create a .env file and set your credentials

Since this project needs to connect to a database, we need to store our credentials in a safe manner. To keep things
simple you can update the .env.example file, and remove .example from the filename. For more information about working
with secrets look [here](https://pybit.es/persistent-environment-variables.html).

### Start

```bash
python scripts/create_tables.py
python scripts/etl.py
```

### Contact

In case of suggestions or remarks please contact the Data Engineering department.
