from bank.bank import Bank
from bank.bank_dao import BankDAO
from bank_account.bank_account import BankAccount
from bank_account.bank_account_dao import BankAccountDAO
from bank_ui.prompts import Prompts
from bank_ui.display import Display


class BankApp:
    def __init__(self):
        self.bank_dao = BankDAO()
        self.account_dao = BankAccountDAO()
        self.prompts = Prompts()
        self.display = Display()


    def run(self):
        while True:
            main_menu = self.prompts.show_main_menu()
            if main_menu == 0:
                self.prompts.show_bank_menu()
            elif main_menu == 1:
                self.prompts.show_account_menu()
            elif main_menu == 2:
                self.prompts.show_transaction_menu()
            elif main_menu == 3:
                print("Exiting...")
                break
            else:
                print("Invalid option, try again.")