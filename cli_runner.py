from library.library_argument_parser import LibraryArgumentParser


def run_parser() -> None:
    """ prepare and run parser that executes operation based on command line arguments """

    parser = LibraryArgumentParser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    run_parser()
