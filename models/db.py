
import pymysql
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Db:
    def __init__(self):
        try:
            self.__connection = pymysql.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE"),
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Database connection failed: {e}")


    def _get_connection(self):
        return self.__connection

    def close(self):
        if self.__connection:
            self.__connection.close()