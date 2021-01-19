from logger import logger
import psycopg2
from settings import DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
from src.sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    logger.info("Dropping the tables..")
    for idx, query in enumerate(drop_table_queries, start=1):
        try:
            cur.execute(query)
        except Exception as error:
            logger.exception(f"ERROR while dropping table {idx}: {error}")
        else:
            conn.commit()


def create_tables(cur, conn):
    logger.info("Creating the tables..")
    for idx, query in enumerate(create_table_queries, start=1):
        try:
            cur.execute(query)
        except Exception as error:
            logger.exception(f"ERROR while creating table {idx}: {error}")
        else:
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
    logger.info("** create_tables script started **")
    main()
    logger.info("** create_tables script finished **")
