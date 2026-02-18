

class BankUI:
    """
    User Interface layer for bank application.
    Provides screen prompts and menus for user interaction.
    Methods return user choices as integer indices or None if input is invalid.
    """
    def __init__(self):
        self.main_options = ["BANK", "ACCOUNT", "TRANSACTIONS", "EXIT"]
        self.bank_options = ["Generate bank", "List of banks", "Return"]
        self.account_options = ["Generate new account", "Account Info", "Make Transaction", "Return"]
        self.operation_options = ["Deposit", "Withdraw", "Transfer", "Return"]
        self.transaction_options = ["All transactions", "Account transactions", "Return"]
        self.separation = 30 * "*"

    def show_options(self, options) -> int|None:
        """
        Display a menu of options and prompt user for selection.
        :param options: List of option strings to display.
        :return: Index of selected option (0-based) or None if input is invalid.
        """
        print(self.separation)
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")
        user_choice = input(f"Chose your option(1-{len(options)}): ")
        print(self.separation)
        if user_choice.isdigit() and int(user_choice) in range(1, len(options) + 1):
            return int(user_choice) - 1
        return None

    def show_main_menu(self) -> int|None:
        """
        Display main menu options (BANK, ACCOUNT, TRANSACTIONS, EXIT).
        :return: Index of selected option or None if input is invalid.
        """
        return self.show_options(self.main_options)

    def show_bank_menu(self) -> int|None:
        """
        Display bank-related options (Generate bank, List of banks, Return).
        :return: Index of selected option or None if input is invalid.
        """
        return self.show_options(self.bank_options)

    def show_account_menu(self) -> int|None:
        """
        Display account-related options (Generate new account, Account Info, Make Transaction, Return).
        :return: Index of selected option or None if input is invalid.
        """
        return self.show_options(self.account_options)

    def show_operation_menu(self) -> int|None:
        """
        Display operation options (Deposit, Withdraw, Transfer, Return).
        :return: Index of selected option or None if input is invalid.
        """
        return self.show_options(self.operation_options)

    def show_transaction_menu(self) -> int|None:
        """
        Display transaction-related options (All transactions, Account transactions, Return).
        :return: Index of selected option or None if input is invalid.
        """
        return self.show_options(self.transaction_options)