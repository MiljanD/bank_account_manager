
import pymysql
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Db:
    """
    Manage database connection using PyMySQL.
    """
    def __init__(self):
        """
        Initialize database connection using environment variables.
        """
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
        """
        Return active database connection.
        :return: PyMySQL connection object.
        """
        return self.__connection

    def close(self):
        """
        Close the database connection.
        :return: None.
        """
        if self.__connection:
            self.__connection.close()