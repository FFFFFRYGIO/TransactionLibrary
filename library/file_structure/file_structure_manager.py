import os
from typing import List, Tuple

from pandas import DataFrame, read_csv

structure_source = os.path.join('library', 'file_structure', 'file_structure.csv')
fields_data = read_csv(structure_source, sep=';', dtype={'default_value': str})


def get_file_fields_names(subparser_requesting: str = None, file_part: str = None) -> List[str]:
    """ get list of fields based on the purpose """

    if subparser_requesting:
        if subparser_requesting == 'get':
            return fields_data[fields_data['is_allowed_to_print']]['field_name'].tolist()
        if subparser_requesting == 'change':
            return fields_data[fields_data['is_allowed_to_change']]['field_name'].tolist()

    if file_part:
        part_fields = fields_data[fields_data['field_group'] == file_part]
        return part_fields[part_fields['is_allowed_to_print']]['field_name'].tolist()

    return fields_data['field_name'].tolist()


def get_file_parts() -> Tuple[DataFrame, DataFrame, DataFrame]:
    """ return information about header, transaction and footer fixed width format """

    header_fields = fields_data[fields_data['field_group'] == 'header']
    transaction_fields = fields_data[fields_data['field_group'] == 'transaction']
    footer_fields = fields_data[fields_data['field_group'] == 'footer']

    return header_fields, transaction_fields, footer_fields


def get_file_parts_id_info() -> List[DataFrame]:
    """ return information about header, transaction and footer id information from fixed width format """

    id_info_elements = ['first_position', 'last_position', 'default_value']

    parts_id_information = []

    for part in ['header', 'transaction', 'footer']:
        part_fields = fields_data[fields_data['field_group'] == part]
        part_id_info = part_fields.loc[part_fields['field_name'] == 'id', id_info_elements].iloc[0]
        parts_id_information.append(part_id_info)

    return parts_id_information
