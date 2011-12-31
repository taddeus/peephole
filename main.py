#!/usr/bin/python
from sys import argv, exit

from src.parser import parse_file


verbose_level = 1


# Parse arguments
if len(argv) < 2:
    print 'Usage: python %s SOURCE_FILE [ OUT_FILE [ SOURCE_OUT_FILE ] ]' \
            % argv[0]
    exit(1)


# Parse file
program = parse_file(argv[1])
program.verbose = verbose_level


# Save input assembly in new file for easy comparison
if len(argv) > 3:
    program.save(argv[3])


# Perform optimizations
program.optimize()


# Save output assembly
if len(argv) > 2:
    program.save(argv[2])
