from argparse import Namespace

from library.file_structure.file_structure_manager import get_file_fields_names
from library.library_content import LibraryContent


def add_transaction(args: Namespace) -> None:
    """ execute add transaction operation """

    content = LibraryContent(args.file)

    try:
        content.add_transaction(args.amount, args.currency)
    except ValueError as e:
        print(e)
        exit()

    content.save_content()

    print("transaction added successfully")


def get_field_value(args: Namespace) -> None:
    """ execute get field value operation """

    content = LibraryContent(args.file)

    try:
        value = content.get_value(args.field, args.counter)
    except ValueError as e:
        print(e)
        exit()

    print(value)


def change_field_value(args: Namespace) -> None:
    """ execute change field value operation """

    content = LibraryContent(args.file)

    try:
        content.change_value(args.field, args.counter, args.value)
    except ValueError as e:
        print(e)
        exit()

    content.save_content()

    if args.field in get_file_fields_names(file_part='transaction'):
        print(f"field \'{args.field}\' for counter \'{args.counter}\' changed to \'{args.value}\' successfully")
    else:
        print(f"field \'{args.field}\' changed to \'{args.value}\' successfully")
