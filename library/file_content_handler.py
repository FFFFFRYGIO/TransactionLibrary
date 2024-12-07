from typing import Tuple, List

from library.file_structure.file_structure_manager import get_file_parts, get_file_parts_id_info


class FileContentHandler:
    """ file content handler that gathers and saves library content to file """

    def __init__(self, file_name: str):
        self.file_name = file_name

        self.header_fields, self.transaction_fields, self.footer_fields = get_file_parts()

        self.hid, self.tid, self.fid = get_file_parts_id_info()

    def load_content(self) -> Tuple[dict, List[dict], dict]:
        """ load file content to class from file """

        with open(self.file_name) as f:
            lines = f.readlines()

            header = {}
            transactions = []
            footer = {}

            for line in lines:

                if line[self.hid['first_position'] - 1:self.hid['last_position']] == self.hid['default_value']:
                    for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.header_fields.iterrows():
                        if f_type == 'int':
                            header.update({f_name: int(line[pos_first - 1:pos_last].strip())})
                        else:
                            header.update({f_name: line[pos_first - 1:pos_last].strip()})

                elif line[self.tid['first_position'] - 1:self.tid['last_position']] == self.tid['default_value']:
                    transaction = {}
                    for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.transaction_fields.iterrows():
                        if f_type == 'int':
                            transaction.update({f_name: int(line[pos_first - 1:pos_last].strip())})
                        else:
                            transaction.update({f_name: line[pos_first - 1:pos_last].strip()})
                    transactions.append(transaction)

                elif line[self.fid['first_position'] - 1:self.fid['last_position']] == self.fid['default_value']:
                    for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.footer_fields.iterrows():
                        if f_type == 'int':
                            footer.update({f_name: int(line[pos_first - 1:pos_last].strip())})
                        else:
                            footer.update({f_name: line[pos_first - 1:pos_last].strip()})

            return header, transactions, footer

    def save_content(self, library_content) -> None:
        """ save file content from class to file """

        with open(self.file_name, 'w') as f:
            header_str = ''
            for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.header_fields.iterrows():
                field_length = pos_last - (pos_first - 1)
                if f_type == 'int':
                    header_str += str(library_content.header.get(f_name)).rjust(field_length, '0')
                else:
                    header_str += library_content.header.get(f_name).ljust(field_length)
            f.write(header_str + '\n')

            for transaction in library_content.transactions:
                transaction_str = ''
                for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.transaction_fields.iterrows():
                    field_length = pos_last - (pos_first - 1)
                    if f_type == 'int':
                        transaction_str += str(transaction.get(f_name)).rjust(field_length, '0')
                    else:
                        transaction_str += transaction.get(f_name).ljust(field_length)
                f.write(transaction_str + '\n')

            footer_str = ''
            for _, (_, pos_first, pos_last, f_type, f_name, _, _, _) in self.footer_fields.iterrows():
                field_length = pos_last - (pos_first - 1)
                if f_type == 'int':
                    footer_str += str(library_content.footer.get(f_name)).rjust(field_length, '0')
                else:
                    footer_str += library_content.footer.get(f_name).ljust(field_length)
            f.write(footer_str + '\n')
