from models.db import Db
from bank_account import BankAccount


class BankAccountDAO(Db):
    def __init__(self):
        super().__init__()


    def insert(self, bank_id, account: BankAccount) -> int:
        query = "INSERT INTO account_manager.accounts (bank_id, owner, balance) VALUES (%s, %s, %s)"
        return self._execute_query(query, (bank_id, account.owner, account.balance), commit=True)

    def balance_update(self, account: BankAccount) -> None:
        query = "UPDATE account_manager.accounts SET balance=%s WHERE id=%s"
        return self._execute_query(query, (account.balance, account.id), commit=True)

    def delete_account(self, account: BankAccount) -> None:
        query = "DELETE FROM account_manager.accounts WHERE id=%s"
        self._execute_query(query, (account.id,), commit=True)

    def all_accounts(self) -> list[dict]:
        query = "SELECT * FROM account_manager.accounts"
        return self._execute_query(query, fetch="all")

    def accounts_by_name(self, owner) -> list[dict]:
        query = "SELECT * FROM account_manager.accounts WHERE owner=%s"
        return self._execute_query(query, (owner,), fetch="all")

    def accounts_by_bank(self, bank_id) -> list[dict]:
        query = "SELECT * FROM account_manager.accounts WHERE bank_id=%s"
        return self._execute_query(query, (bank_id,), fetch="all")

    def account_by_id(self, acc_id) -> dict:
        query = "SELECT * FROM account_manager.accounts WHERE id=%s"
        return self._execute_query(query, (acc_id,))

    def all_accounts_transactions(self) -> list[dict]:
        query = ("SELECT "
                 "b.name AS bank_name, "
                 "a.owner AS account_owner, "
                 "t.operation AS operation, t.amount AS amount "
                 "FROM account_manager.accounts a "
                 "INNER JOIN account_manager.bank b on b.id = a.bank_id "
                 "INNER JOIN account_manager.transactions t on a.id = t.acc_id "
                 "ORDER BY a.id ")
        return self._execute_query(query, fetch="all")

    def transactions_by_account_id(self, account: BankAccount) -> list[dict]:
        query = ("SELECT "
                 "* "
                 "FROM account_manager.accounts a "
                 "INNER JOIN account_manager.bank b on a.bank_id = b.id "
                 "INNER JOIN account_manager.transactions t on a.id = t.acc_id "
                 "WHERE a.id =%s "
                 "ORDER BY a.id ")
        return self._execute_query(query, (account.id,), fetch="all")
