#!/usr/bin/env python
# encoding: utf-8
'''
run -- SNPMatrixGenerator CLI

@author:     Matthew Demarest
@license:    Apache License 2.0
@contact:    demarest.7@osu.edu
'''

import sys
import os

import argparse
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import SNPMatrixGenerator

__all__ = []
__version__ = 1.0
__date__ = '2013-08-28'
__updated__ = '2013-09-03'

DEBUG = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def str(self):
        return self.msg

    def unicode(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

    DEPENDENCIES: python-nexus (use pip to install)

  Created by Matthew Demarest on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(dest="inputFile", metavar="input",
                            type=argparse.FileType('r'), help="input file")
        parser.add_argument(dest="outputFile", metavar="output",
                            type=argparse.FileType('w'), help="output file")
        parser.add_argument(dest="collectType", choices={'sample', 'all'},
                            help="which columns from each input matrix " + \
                                 "are transferred to SNP matrix")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
            print args

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

    SNPMatrixGenerator.snpMatrixGenerator(args.inputFile,
                    args.outputFile, args.collectType == "all",
                    args.collectType == "sample")


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    sys.exit(main())
