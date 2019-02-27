import os
import sys
from argparse import ArgumentParser

from feedchecker import Checker

parser = ArgumentParser()
parser.add_argument(
    "-i", "--input", dest="input", help="input path to check and filter")
parser.add_argument("-o", "--output", dest="output", help="output path")
parser.add_argument(
    '--timeout',
    dest='request_timeout',
    type=int,
    default=10,
    help='request timeout seconds')
parser.add_argument(
    '--oktimeout',
    action='store_false',
    help='considers a timeout response as a good response')

args = parser.parse_args()

if not args.input:
    sys.exit('Specify an input file, run with -h option for help')
if not args.output:
    sys.exit('Specify an output file, run with -h option for help')
if not os.path.isfile(args.input):
    sys.exit('Cannot find the input file, dude')

checker = Checker(args.input, args.output, args.request_timeout,
                  args.oktimeout)
checker.run()
