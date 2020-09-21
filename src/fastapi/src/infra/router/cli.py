#!/usr/bin/env python
import argparse

from di.rdb import RdbCommandFactory
from intarface.command import RdbCommand

if __name__ == "__main__":
    rdb: RdbCommand = RdbCommandFactory.get()

    parser = argparse.ArgumentParser(description="app command")
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser("create_tables", help="see `create_tables -h`")
    parser_add.add_argument(
        "table_names",
        type=str,
        nargs="?",
        default=None,
        choices=rdb.managed_tables,
        help="Create table name",
    )
    parser_add.set_defaults(handler=rdb.create_tables)

    parser_add = subparsers.add_parser("drop_tables", help="see `drop_tables -h`")
    parser_add.add_argument(
        "table_names",
        type=str,
        nargs="?",
        default=None,
        choices=rdb.managed_tables,
        help="Drop table name",
    )
    parser_add.set_defaults(handler=rdb.drop_tables)

    parser_add = subparsers.add_parser("reset_tables", help="see `reset_tables -h`")
    parser_add.add_argument(
        "table_names",
        type=str,
        nargs="?",
        default=None,
        choices=rdb.managed_tables,
        help="Drop and Create table name",
    )
    parser_add.set_defaults(handler=rdb.reset_tables)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(**vars(args))
    else:
        parser.print_help()
