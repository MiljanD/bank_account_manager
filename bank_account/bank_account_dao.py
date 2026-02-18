import pymysql

from models.db import Db
from bank_account import BankAccount


class BankAccountDAO(Db):
    """
    Data Access Object layer for bank operations.
    Encapsulates SQL logic and centralizes query execution via protected methods.
    Returned data types vary depending on method (dicts, list of dicts, int or None).
    Inherits from Db to manage database connection.
    """
    def __init__(self):
        super().__init__()


    def insert(self, bank_id, account: BankAccount) -> int:
        """
        Insert new account into database.
        :param bank_id: ID of associated bank.
        :param account: Bank account object
        :return: ID of newly created account in database.
        """
        query = "INSERT INTO account_manager.accounts (bank_id, owner, balance) VALUES (%s, %s, %s)"
        return self._execute_query(query, (bank_id, account.owner, account.balance), commit=True)

    def balance_update(self, account: BankAccount, amount, operation) -> list[int]|None:
        """
        Updates account balance and inserts details into transaction table(UPDATE and INSERT in one transaction).
        :param account: Bank Account object.
        :param amount:
        :param operation: Deposit(increase of current balance) / Withdraw(decrease of current balance)
        :return: List of affected row counts for each executed query or None if withdraw is not possible due to insufficient funds.
        """
        if operation == "deposit":
            account.deposit(amount)
        elif operation == "withdraw":
            if self.balance_check(account.id, amount):
                account.withdraw(amount)

        update_query = "UPDATE account_manager.accounts SET balance=%s WHERE id=%s"
        insert_to_transaction = "INSERT INTO account_manager.transactions (acc_id, operation, amount) VALUES (%s, %s, %s)"
        queries = [(update_query, (account.balance, account.id)), (insert_to_transaction, (account.id, operation, amount))]

        return self._execute_transaction(queries)

    def delete_account(self, account: BankAccount) -> None:
        """
        Deletes account record from database table.
        :param account: Bank Account object.
        """
        query = "DELETE FROM account_manager.accounts WHERE id=%s"
        self._execute_query(query, (account.id,), commit=True)

    def balance_check(self, acc_id, amount) -> bool:
        """
        Checks if current account balance sufficient for withdraw operation.
        :param acc_id: ID of account.
        :param amount: Desired amount value.
        :return: True or False
        """
        query = "SELECT id FROM account_manager.accounts WHERE balance >= %s AND id=%s"
        if self._execute_query(query, (amount, acc_id,)):
            return True
        return False

    def transfer(self, sender: BankAccount, receiver: BankAccount, amount) -> list[int]|None:
        """
        Manage money transfer between two accounts where update of both account is done in one transaction.
        :param sender: Bank Account from which money is transferred.
        :param receiver: Bank Account to which will receive money.
        :param amount: Amount of transferred money
        :return: List of affected row counts for each executed query or None if current sender balance is not sufficient.
        """
        if self.balance_check(sender.id, amount):
            sender.withdraw(amount)
            update_sender_acc = (
                "UPDATE account_manager.accounts SET balance=%s WHERE id=%s",
                (sender.balance, sender.id)
            )
            insert_sender_trans = (
                "INSERT INTO account_manager.transactions (acc_id, operation, amount) VALUES (%s, %s, %s)",
                (sender.id, "withdraw", amount)
            )

            receiver.deposit(amount)
            update_receiver_acc = (
                "UPDATE account_manager.accounts SET balance=%s WHERE id=%s",
                (receiver.balance, receiver.id)
            )
            insert_receiver_trans = (
                "INSERT INTO account_manager.transactions (acc_id, operation, amount) VALUES (%s, %s, %s)",
                (receiver.id, "deposit", amount)
            )

            queries = [update_sender_acc, insert_sender_trans, update_receiver_acc, insert_receiver_trans]

            return self._execute_transaction(queries)
        return None

    def all_accounts(self) -> list[dict]:
        """
        Select all accounts form database.
        :return: List of accounts(account details are in from of dict)
        """
        query = "SELECT * FROM account_manager.accounts"
        return self._execute_query(query, fetch="all")

    def accounts_by_name(self, owner) -> list[dict]:
        """
        Fetch all accounts of specified account owner.
        :param owner: Account owner name
        :return: List of owners accounts.
        """
        query = "SELECT * FROM account_manager.accounts WHERE owner=%s"
        return self._execute_query(query, (owner,), fetch="all")

    def accounts_by_bank(self, bank_id) -> list[dict]:
        """
        All accounts of specific bank.
        :param bank_id: ID of the bank from database.
        :return: List of all bank details.
        """
        query = "SELECT * FROM account_manager.accounts WHERE bank_id=%s"
        return self._execute_query(query, (bank_id,), fetch="all")

    def account_by_id(self, acc_id) -> dict:
        """
        Fetch account by account ID.
        :param acc_id: ID of account from database.
        :return: Account details in from of dictionary.
        """
        query = "SELECT * FROM account_manager.accounts WHERE id=%s"
        return self._execute_query(query, (acc_id,))

    def all_accounts_transactions(self) -> list[dict]:
        """
        Fetch transaction data for all accounts.
        :return: List of transaction details for all accounts.
        """
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
        """
        Fetch transaction data for specific account.
        :param account: Bank Account object.
        :return: Transaction data for specific account.
        """
        query = ("SELECT "
                 "* "
                 "FROM account_manager.accounts a "
                 "INNER JOIN account_manager.bank b on a.bank_id = b.id "
                 "INNER JOIN account_manager.transactions t on a.id = t.acc_id "
                 "WHERE a.id =%s "
                 "ORDER BY a.id ")
        return self._execute_query(query, (account.id,), fetch="all")
