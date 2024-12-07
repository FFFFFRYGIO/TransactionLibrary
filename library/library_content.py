from library.file_content_handler import FileContentHandler
from library.file_structure.file_structure_manager import get_file_fields_names
from utils.get_currency_types import get_currency_types


class LibraryContent:
    """ library content class that stores all library information """

    def __init__(self, file_name: str):
        self.file_loader = FileContentHandler(file_name)
        self.header, self.transactions, self.footer = self.file_loader.load_content()

    def save_content(self) -> None:
        """ save library content to file """

        self.file_loader.save_content(self)

    def add_transaction(self, amount: int, currency: str) -> None:
        """ add new transaction """

        possible_currencies = get_currency_types()
        if currency not in possible_currencies:
            raise ValueError('currency not supported')

        prev_counter = self.transactions[-1]['counter']
        new_counter_value = int(prev_counter) + 1
        new_counter = str(new_counter_value).rjust(len(prev_counter), '0')

        new_transaction = self.transactions[-1].copy()

        new_transaction.update({'counter': new_counter})
        new_transaction.update({'amount': amount})
        new_transaction.update({'currency': currency})

        self.transactions.append(new_transaction)

        self.update_footer()

    def get_value(self, field, counter=None) -> dict:
        """ return value of given field """

        if field in get_file_fields_names(file_part='header'):
            return self.header[field]
        elif field in get_file_fields_names(file_part='transaction'):
            if not counter:
                raise ValueError('missing counter parameter')
            transaction = next((t for t in self.transactions if t['counter'] == counter), None)
            try:
                return transaction[field]
            except TypeError:
                raise ValueError(f'could not find transaction with counter {counter}')
        elif field in get_file_fields_names(file_part='footer'):
            return self.footer[field]
        else:
            raise ValueError('Unknown field type')

    def change_value(self, field: str, counter: str, value: str) -> None:
        """ change value of given field """

        if field in get_file_fields_names(file_part='header'):
            if isinstance(self.header[field], int):
                self.header[field] = value
            else:
                self.header[field] = value
        elif field in get_file_fields_names(file_part='transaction'):
            if not counter:
                raise ValueError('missing counter parameter')
            try:
                transaction_index = int(counter) - 1
            except ValueError:
                raise ValueError(f'counter value {counter} not convertable to int')
            try:
                if isinstance(self.transactions[transaction_index][field], int):
                    self.transactions[transaction_index][field] = int(value)
                else:
                    self.transactions[transaction_index][field] = value
            except TypeError:
                raise ValueError(f'Could not find transaction with counter {counter}')
        elif field in get_file_fields_names(file_part='footer'):
            if isinstance(self.footer[field], int):
                self.footer[field] = int(value)
            else:
                self.footer[field] = value
        else:
            raise ValueError('Unknown field type')

        self.update_footer()

    def update_footer(self) -> None:
        """ update footer values based on current transactions list """

        self.footer['total_counter'] = len(self.transactions)
        self.footer['control_sum'] = sum(t['amount'] for t in self.transactions)
