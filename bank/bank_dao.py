import pymysql

from models.db import Db
from bank import Bank


class BankDAO(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()


    def _execute_query(self, query, params=None, commit=False, fetch="one"):
        try:
            with self.con.cursor() as cursor:
                # if params are passed use them in query
                cursor.execute(query, params or ())
            if commit:
                self.con.commit()
                return cursor.lastrowid
            if fetch == "one":
                return cursor.fetchone()
            elif fetch == "all":
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.con.rollback()
            raise RuntimeError(f"Database query failed while executing:{query}, Error: {e}")

    def insert(self, bank: Bank) -> int:
        query = "INSERT INTO account_manager.bank (name) VALUES (%s)"
        # fetch argument can be default since commit arg is True
        return self._execute_query(query, params=(bank.name,), commit=True)


    def all_banks(self) -> list[dict]:
        query = "SELECT * FROM account_manager.bank"
        return self._execute_query(query,fetch="all")


    def get_id_by_name(self, name) -> dict|None:
        query = "SELECT id FROM account_manager.bank WHERE name=%s"
        return self._execute_query(query, params=(name,))


    def find_by_id(self, bank_id) -> dict|None:
        query = "SELECT * FROM account_manager.bank WHERE id=%s"
        return self._execute_query(query, params=(bank_id,))



    def get_last_added_id(self) -> dict|None:
        query = "SELECT id FROM account_manager.bank ORDER BY id DESC LIMIT 1"
        return self._execute_query(query)

    def all_bank_accounts(self) -> list[dict]:
        query = ("SELECT "
                 "b.id AS bank_ID, b.name AS bank_name, "
                 "a.id AS account_ID, a.owner AS owner, a.balance AS balance "
                 "FROM account_manager.bank b "
                 "LEFT JOIN account_manager.accounts a ON b.id = a.bank_id "
                 "ORDER BY b.id"
                 )
        return self._execute_query(query, fetch="all")


    def accounts_by_name(self, name) -> list[dict]:
        query = ("SELECT "
                 "b.id AS bank_ID, b.name AS bank_name, "
                 "a.id AS account_ID, a.owner AS owner, a.balance AS balance "
                 "FROM account_manager.bank b "
                 "LEFT JOIN account_manager.accounts a on b.id = a.bank_id "
                 "WHERE a.owner=%s ORDER BY b.id")
        return self._execute_query(query, params=(name,), fetch="all")
