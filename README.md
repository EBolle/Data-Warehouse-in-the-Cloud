# On cloud nine with Redshift

Due to the exponential growth of Sparkify they decided to move their data once more. Not only is speed of the essence,
but scalability and flexibility as well. By implementing Redshift they gain several advantages:

- Very fast querying performance due to Massively Parallel Processing, even with enormous amounts of data
- Easy to scale, in a matter of minutes one can launch additional clusters to increase storage and performance
- It is secure, no need to worry about security or hire very costly specialists

For more information and as a resource please have a look [here][redshift_resource]. Due to the switch of data warehouse
several adjustments to the data definition and manipulation has been made.

## The data flow

Raw .json files that reside on Amazon S3 are first inserted into 2 staging tables on Redshift. These staging tables
are then transformed and loaded into 4 dimension tables and 1 fact table, adhering to a typical star schema.

### Staging tables

- `staging_events`
- `staging_songs`

Both staging tables are distributed evenly, since they are mostly queried without additional joins. Hence, by evenly
distributing the data across all the nodes we gain better performance. Since the order of the timestamp (`ts`) variable
in `staging_events` is used in a insertion query, and we expect this order to stay relevant for future tables, we added
a sortkey.

### The star schema

The dimension tables `users`, `songs`, and `artists` are fully copied to each node using the all distribution strategy.
There are 2 reasons for this:

- they are relatively small
- they are not expected to have large and frequent upserts, at least not in comparison to `time` and `songplays`

The dimension table `time` is evenly distributed and has a sorted primary key since it is a direct derivative of the fact 
table. Since it holds an actual timestamp of an event there is no limit to the number of possible rows. Since we expect
Sparkify to keep growing we need to evenly distribute the data to keep acceptable speed.

Naturally, the fact table is evenly distributed due to its size, expected large and frequent upserts, and the
possibility to be queried without joins. 

<img src=[star_schema]>

## Streamlit dashboard

<img src="https://user-images.githubusercontent.com/49920622/105627366-df263480-5e36-11eb-97d2-1b7d5e3904bd.PNG">

ETL processes are interesting, but at the end of the day we want to leverage the insights we generate with the data.
To give you a glimpse of what is possible we developed a small Streamlit dashboard that gives insights into:

- Where are the artists located in the world?
- What is the typical listening behaviour throughout a month?
- Is that different for paying customers? If so, can we explain why that is? 

To be able to use the dashboard please read the next section carefully.

## Instructions

Before you can run the scripts, there are a few things you need to do:
- create and activate a virtual environment
- create a .env file and set your AWS credentials and Redshift settings
- run the scripts in a particular order

Furthermore, note that the logic needed to execute the scripts and app are stored in the /src folder.
The Python version used for this project is 3.8.5. 

### create and activate a virtual environment 

You can either use Anaconda or virtualenv to create the virtual environment, if you are not familiar with virtual
environments please read this [article][virtual_envs] first.


```bash
conda env create -f environment.yml
conda activate redshift

python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt 
```

### create a .env file and set your credentials

We assume that you already have a working Redshift cluster and a ARN with read access to S3. You need to specify the
cluster endpoint and your database settings to create the connection and execute the scripts. Last but not least you need
to include the correct S3 url's. 

To keep things simple and safe you can update the .env.example file, and remove .example from  the filename. For more 
information about working with secrets look [here][secrets].

If any of these requirements sounds unfamiliar please have a look at the [AWS documentation][aws_documentation].

### Run the scripts in a particular order

Once your Redshift cluster is running and all the credentials and settings have been set, you can execute the following
scripts in this exact order fro the top-level of the folder project.

```bash
python scripts/create_tables.py
python scripts/etl.py
streamlit run src/streamlit_app.py
```

Once you run the streamlit command your webbrowser will open a new tab with the Streamlit dashboard.

## Contact

In case of suggestions or remarks please contact the Data Engineering department.

[redshift_resource]: https://www.sisense.com/blog/5-advantages-using-redshift-data-warehouse/
[star_schema]: "https://user-images.githubusercontent.com/49920622/103062485-97e62300-45ae-11eb-908d-4f27cca6f2a6.png"
[virtual_envs]: https://realpython.com/python-virtual-environments-a-primer/
[secrets]: https://pybit.es/persistent-environment-variables.html
[aws_documentation]: https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html