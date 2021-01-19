from logger import logger
import psycopg2
from settings import DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
from src.sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    logger.info("Loading the staging tables")
    for idx, query in enumerate(copy_table_queries, start=1):
        try:
            cur.execute(query)
        except Exception as error:
            logger.exception(f"ERROR while loading staging table {idx}: {error}")
        else:
            conn.commit()
            logger.info(f"Staging table {idx} / {len(copy_table_queries)} has been successfully loaded.")


def insert_tables(cur, conn):
    logger.info("Loading the analytical tables")
    for idx, query in enumerate(insert_table_queries, start=1):
        try:
            cur.execute(query)
        except Exception as error:
            logger.exception(f"ERROR while loading analytical table {idx}: {error}")
        else:
            conn.commit()
            logger.info(f"Analytical table {idx} / {len(insert_table_queries)} has been successfully loaded.")


def main():
    try:
        conn = psycopg2.connect(f"postgresql://{DWH_DB_USER}:{DWH_DB_PASSWORD}@{DWH_ENDPOINT}:{DWH_PORT}/{DWH_DB}")
    except Exception as error:
        logger.exception(f"ERROR while connecting to the Redshift cluster: {error}")
    else:
        cur = conn.cursor()
    
        load_staging_tables(cur, conn)
        insert_tables(cur, conn)

        conn.close()


if __name__ == "__main__":
    logger.info("** ETL script started **")
    main()
    logger.info("** ETL script finished **")
