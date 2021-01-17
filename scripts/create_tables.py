from logger import logger
import psycopg2
from settings import DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
from src.sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    try:
        conn = psycopg2.connect(f"postgresql://{DWH_DB_USER}:{DWH_DB_PASSWORD}@{DWH_ENDPOINT}:{DWH_PORT}/{DWH_DB}")
    except Exception as error:
        logger.exception(f"ERROR while connecting to the Redshift cluster: {error}")
    else:
        cur = conn.cursor()

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()


if __name__ == "__main__":
    logger.info("Creating the tables on the Redshift cluster...")
    main()
    logger.info("The tables have been successfully created.")
