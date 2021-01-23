from dotenv import load_dotenv
import os

load_dotenv()

# IAM_ROLE
ARN = os.getenv('ARN')

# Redshift cluster
DWH_DB = os.getenv('DWH_DB')
DWH_DB_USER = os.getenv('DWH_DB_USER')
DWH_DB_PASSWORD = os.getenv('DWH_DB_PASSWORD')
DWH_ENDPOINT = os.getenv('DWH_ENDPOINT')
DWH_PORT = os.getenv('DWH_PORT')

# S3 URL's
LOG_DATA = os.getenv('LOG_DATA')
SONG_DATA = os.getenv('SONG_DATA')
