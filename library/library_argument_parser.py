from argparse import ArgumentParser

from library.file_structure.file_structure_manager import get_file_fields_names
from requests_handlers import add_transaction, get_field_value, change_field_value


class LibraryArgumentParser(ArgumentParser):
    """ ArgumentParser class designed for library task """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_argument('file', help='transaction file path')

        subparsers = self.add_subparsers(title='available operations on transaction file', parser_class=ArgumentParser,
                                         required=True)

        parser_add = subparsers.add_parser('add', help='add transaction', aliases=['a'])
        parser_add.add_argument("amount", help="transaction amount", type=int)
        parser_add.add_argument("currency", help="transaction currency")
        parser_add.set_defaults(func=add_transaction)

        parser_get = subparsers.add_parser('get', help='get value of a field', aliases=['g'])
        parser_get.add_argument('field', choices=get_file_fields_names('get'), help='field name')
        parser_get.set_defaults(func=get_field_value)
        parser_get.add_argument('--counter', help="transaction counter for transaction field", required=False)

        parser_change = subparsers.add_parser('change', help='change field value', aliases=['c'])
        parser_change.add_argument("field", choices=get_file_fields_names('change'), help="field name")
        parser_change.add_argument("--counter", help="transaction counter for transaction field", required=False)
        parser_change.add_argument("value", help="New value")
        parser_change.set_defaults(func=change_field_value)
