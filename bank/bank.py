

class Bank:
    """
    Model class for bank objects.
    """
    def __init__(self, name, bank_id=None):
        """
        Instantiating of bank object attributes.
        :param name: Bank name (mandatory).
        :param bank_id: Database ID if the bank (optional).
        """
        self.name = name
        self.id = bank_id


    def __repr__(self):
        return f"<Bank id={self.id}, name={self.name}>"

    def __str__(self):
        return f"Bank ID: {self.id}, Bank Name: {self.name}"

