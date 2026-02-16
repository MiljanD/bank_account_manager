

class BankAccount:
    """
    Represents a bank account with an owner and balance.
    Provides methods for depositing and withdrawing funds.
    """
    def __init__(self, owner, balance=0):
        """
        Initialize a new bank account.
        :param owner: Name of the account owner.
        :param balance: Initial balance (default is 0).
        """
        self.owner = owner
        self.balance = balance

    def deposit(self, amount) -> str|None:
        """
        Deposit funds into the account.
        :param amount: Amount to deposit (must be numeric).
        :return: None if successful, otherwise error message..
        """
        if isinstance(amount, (int, float)):
            self.balance += amount
            return None
        return "Amount needs to be numerical value"

    def withdraw(self, amount) -> str|None:
        """
        Withdraw funds from the account.
        :param amount: Amount to withdraw (must be numeric).
        :return: None if successful, otherwise error message (non-numeric or insufficient funds).
        """
        if isinstance(amount, (int, float)):
            if self.balance >= amount:
                self.balance -= amount
                return None
            return "Insufficient funds."
        return "Amount needs to be numerical value"

