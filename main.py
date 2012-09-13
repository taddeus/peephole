#!/usr/bin/python
from sys import argv, exit

from src.parser import parse_file


options = {'-v': 1}


# Parse arguments
def exit_with_usage():
    print 'Usage: python %s [ options ] SOURCE_FILE' % argv[0]
    print 'options: -i SOURCE_OUT_FILE | -o OUT_FILE | -v VERBOSE_LEVEL'
    exit(1)


if len(argv) % 2:
    exit_with_usage()
elif len(argv) > 2:
    values = argv[2:-1:2]

    if argv[1][0] != '-':
        exit_with_usage()

    for i, option in enumerate(argv[1:-1:2]):
        if option not in ['-i', '-o', '-v']:
            print 'unknown option "%s"' % option
            exit(1)

        if i >= len(values):
            print 'No value given for option "%s"' % option
            exit(1)

        options[option] = values[i]


# Parse file
program = parse_file(argv[-1])
program.verbose = int(options['-v'])


# Save input assembly in new file for easy comparison
if '-i' in options:
    program.save(options['-i'])


# Perform optimizations
program.optimize()


# Save output assembly
if '-o' in options:
    program.save(options['-o'])
