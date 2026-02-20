from bank.bank import Bank
from bank.bank_dao import BankDAO
from bank_account.bank_account import BankAccount
from bank_account.bank_account_dao import BankAccountDAO
from bank_ui.prompts import Prompts
from bank_ui.display import Display


class BankApp:
    """
    Main application class that orchestrates bank and account operations.
    Uses DAO classes for data persistence, Prompts for user interaction,
    and Display for formatted output.
    """
    def __init__(self):
        """Initialize DAOs, Prompts, and Display components."""
        self.bank_dao = BankDAO()
        self.account_dao = BankAccountDAO()
        self.prompts = Prompts()
        self.display = Display()

    def bank_creation(self) -> None:
        """
        Create a new bank entry based on user input.
        Prompts for bank name and inserts it into the database.
        """
        bank_name = self.prompts.bank_name_entry()
        if bank_name:
            bank = Bank(bank_name)
            self.bank_dao.insert(bank)
        else:
            print("Invalid entry for bank name.")


    def show_all_banks(self) -> None:
        """
        Retrieve and display all banks from the database.
        """
        all_banks = self.bank_dao.all_banks()
        self.display.display_content(all_banks)

    def handle_bank_menu(self) -> None:
        """
        Handle user choices from the bank menu.
        Delegates to bank creation or listing methods.
        """
        bank_menu = self.prompts.show_bank_menu()
        if bank_menu == 0:
            self.bank_creation()
        elif bank_menu == 1:
            self.show_all_banks()

    def account_creation(self) -> None:
        """
        Create a new bank account for a selected bank.
        Prompts for bank ID, owner name, and optional initial deposit.
        """
        self.display.display_content(self.bank_dao.all_banks())

        bank_id = self.prompts.bank_id_entry()
        owner_name = self.prompts.account_owner_entry()
        if bank_id and owner_name:
            account = BankAccount(owner_name)
            account.id = self.account_dao.insert(bank_id, account)
            make_deposit = self.prompts.first_deposit()
            if make_deposit == 0:
                deposit_amount = self.prompts.amount_entry()
                if deposit_amount:
                    self.account_dao.balance_update(account, deposit_amount, "deposit")
        else:
            print("Invalid entry for bank id or owner name.")

    def show_account_details(self) -> None:
        """
        Display details of a specific account by ID.
        """
        acc_choice = self.prompts.account_id_entry()
        if acc_choice:
            acc_data = self.account_dao.account_by_id(acc_choice)
            self.display.display_content(acc_data)
        else:
            print("Invalid entry of account id.")

    def make_deposit(self, acc, amount) -> None:
        """
        Perform a deposit operation on the given account.
        :param acc: BankAccount instance
        :param amount: Deposit amount
        """
        self.account_dao.balance_update(acc, amount, "deposit")

    def make_withdraw(self, acc, amount) -> None:
        """
        Perform a withdrawal operation on the given account.
        :param acc: BankAccount instance
        :param amount: Withdrawal amount
        """
        self.account_dao.balance_update(acc, amount, "withdraw")

    def make_transfer(self, sender_account, amount) -> BankAccount|None:
        """
       Transfer funds from one account to another.
       Prompts for receiver account ID.
       :param sender_account: BankAccount instance (sender)
       :param amount: Transfer amount
       :return: Receiver account if successful, else None
       """
        receiver_acc_id = self.prompts.account_id_entry()
        if receiver_acc_id:
            receiver_data = self.account_dao.account_by_id(receiver_acc_id)
            receiver_account = BankAccount(receiver_data["owner"], receiver_data["balance"],
                                           receiver_data["id"])
            self.account_dao.transfer(sender_account, receiver_account, amount)
            return receiver_account
        return None

    def handle_account_menu(self) -> None:
        """
        Handle user choices from the account menu.
        Delegates to account creation, details, or operations.
        """
        account_menu = self.prompts.show_account_menu()
        if account_menu == 0:
           self.account_creation()

        elif account_menu == 1:
            self.show_account_details()

        elif account_menu == 2:
            operation_choice = self.prompts.show_operation_menu()
            acc_id = self.prompts.account_id_entry()

            if acc_id:
                account_data = self.account_dao.account_by_id(acc_id)
                operation_account = BankAccount(account_data["owner"], account_data["balance"], account_data["id"])
                operation_amount = self.prompts.amount_entry()

                if operation_amount:
                    if operation_choice == 0:
                        self.make_deposit(operation_account, operation_amount)
                        print(f"{operation_account.owner} deposited {operation_amount} to account {operation_account.id}")
                    elif operation_choice == 1:
                        self.make_withdraw(operation_account, operation_amount)
                        print(f"{operation_account.owner} withdrawn {operation_amount} from account {operation_account.id}")
                    elif operation_choice == 2:
                        receiver = self.make_transfer(operation_account, operation_amount)
                        if receiver:
                            print(f"From account {operation_account.id}, {operation_account.owner} transferred {operation_amount}"
                                f" to account {receiver.id} of owner {receiver.owner}")

    def show_all_transactions(self) -> None:
        """
        Retrieve and display all transactions across accounts.
        """
        all_transactions = self.account_dao.all_accounts_transactions()
        self.display.display_content(all_transactions)

    def show_transaction_by_acc_id(self) -> None:
        """
        Display all transactions for a specific account by ID.
        """
        transaction_account_id = self.prompts.account_id_entry()
        if transaction_account_id:
            trans_acc_data = self.account_dao.account_by_id(transaction_account_id)
            transaction_account = BankAccount(trans_acc_data["owner"], trans_acc_data["balance"], trans_acc_data["id"])
            transaction_data = self.account_dao.transactions_by_account_id(transaction_account)
            self.display.display_content(transaction_data)

    def handle_transaction_menu(self) -> None:
        """
        Handle user choices from the transaction menu.
        Delegates to transaction listing methods.
        """
        transaction_menu = self.prompts.show_transaction_menu()
        if transaction_menu == 0:
            self.show_all_transactions()
        elif transaction_menu == 1:
            self.show_transaction_by_acc_id()


    def run(self) -> None:
        """
        Main loop of the application.
        Displays the main menu and routes user choices
        to the appropriate handlers until exit.
        """
        while True:
            main_menu = self.prompts.show_main_menu()

            match main_menu:
                case 0:
                    self.handle_bank_menu()
                case 1:
                    self.handle_account_menu()
                case 2:
                    self.handle_transaction_menu()
                case 3:
                    print("Exiting...")
                    break
                case _:
                    print("Invalid option, try again.")
