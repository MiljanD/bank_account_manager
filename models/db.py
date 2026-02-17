
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
        :return: None
        """
        if self.__connection:
            self.__connection.close()

    def _execute_query(self, query, params=None, commit=False, fetch="one"):
        """
        Protected method that centralizes SQL query execution using the active connection.
        Handles parameter binding, transaction commit/rollback, and fetch modes.
        Raises RuntimeError on database errors. Intended for internal DAO usage.

        :param query:SQL query string.
        :param params:Parameters for the SQL query (tuple or list).
        :param commit:Whether to commit the transaction (for INSERT, UPDATE or DELETE).
        :param fetch:Fetch mode for SELECT queries ('one' or 'all').
        :return:dict, list of dicts, int, or None depending on query type.
        """
        try:
            with self._get_connection() as cursor:
                # if params are passed use them in query
                cursor.execute(query, params or ())
            if commit:
                self._get_connection().commit()
                return cursor.lastrowid
            if fetch == "one":
                return cursor.fetchone()
            elif fetch == "all":
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            self._get_connection().rollback()
            raise RuntimeError(f"Database query failed while executing:{query}, Error: {e}")

    def _execute_transaction(self, queries: list[tuple]) -> list[int]:
        """
        Execute multiple SQL queries as a single transaction.
        All queries are executed in order; if any query fails, the entire transaction is rolled back.
        :param queries: List of tuples (query, params) representing SQL statements and their parameters.
        :raises RuntimeError: If any query fails during execution.
        :return: List of affected row counts for each executed query.
        """
        try:
            affected_rows = []
            for query in queries:
                with self._get_connection().cursor() as cursor:
                    cursor.execute(query[0], query[1])
                    affected_rows.append(cursor.rowcount)
            self._get_connection().commit()
            return affected_rows
        except pymysql.MySQLError as e:
            self._get_connection().rollback()
            raise RuntimeError(f"Database query failed while executing transaction: {e}")
