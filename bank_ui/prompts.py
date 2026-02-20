

class Prompts:
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
        self.yes_or_no = ["Yes", "No"]
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

    def first_deposit(self) -> int|None:
        """
        Ask the user if they want to make an initial deposit.
        :return: User choice from yes/no options (int) or None if invalid.
        """
        print("Do you want to make deposit?")
        return self.show_options(self.yes_or_no)

    def _validate_entry(self, entry, data_entry) -> int|float|str|None:
        """
        Validate and convert user input based on expected data type.
        :param entry: Raw user input string.
        :param data_entry: Expected type ('id', 'amount', 'name').
        :return: Converted value (int, float, str) or None if invalid.
        """
        try:
            match data_entry:
                case "id":
                    return int(entry)
                case "amount":
                    return float(entry)
                case "name":
                    if not entry.strip():
                        return None
                    return entry.strip()
        except ValueError:
            return None


    def amount_entry(self) -> float|None:
        """
        Prompt the user to enter an amount.
        :return: Float value of amount or None if invalid.
        """
        amount = input("Enter amount: ")
        return self._validate_entry(amount, "amount")

    def bank_id_entry(self) -> int|None:
        """
        Prompt the user to enter a bank ID.
        :return: Integer bank ID or None if invalid.
        """
        bank_id = input("Enter bank ID: ")
        return self._validate_entry(bank_id, "id")

    def account_id_entry(self) -> int|None:
        """
        Prompt the user to enter an account ID.
        :return: Integer account ID or None if invalid.
        """
        acc_id = input("Enter account ID: ")
        return self._validate_entry(acc_id, "id")

    def account_owner_entry(self) -> str|None:
        """
        Prompt the user to enter the account owner's name.
        :return: Owner name string or None if invalid/empty.
        """
        owner_name =  input("Enter account owner name: ")
        return self._validate_entry(owner_name, "name")

    def bank_name_entry(self) -> str|None:
        """
        Prompt the user to enter a bank name.
        :return: Bank name string or None if invalid/empty.
        """
        bank_name = input("Enter bank name: ")
        return self._validate_entry(bank_name, "name")
