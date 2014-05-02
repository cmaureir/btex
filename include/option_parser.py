#!/usr/bin/env python

import argparse as ap


class OptionParser:
    def __init__(self):
        # Parser
        desc = "bTeX: a BibTeX tool that makes your life easy"
        self.parser = ap.ArgumentParser(prog="bTeX",
                                        description=desc,
                                        formatter_class=ap.RawTextHelpFormatter)

        # General options
        self.general_group = self.parser.add_argument_group("General options")
        self.add_general_options()

        subparsers = self.parser.add_subparsers(dest="mode")
        # TO DO
        # sp_check = subparsers.add_parser('check', help='Check the bibTeX file')
        # sp_clean = subparsers.add_parser('clean', help='Clean the bibTeX file')
        sp_parse = subparsers.add_parser('parse', help='Parse the bibTeX file')

    def add_general_options(self):
        file_help = "Input filename"
        self.general_group.add_argument("-f",
                                        dest="filename",
                                        type=str,
                                        help=file_help,
                                        required=True)

    def get_options(self):
        return self.parser.parse_args()
