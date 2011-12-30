#!/usr/bin/python
from src.parser import parse_file
from src.optimize import optimize

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s SOURCE_FILE [ OUT_FILE [ SOURCE_OUT_FILE ] ]' \
                % argv[0]
        exit(1)

    # Parse file
    program = parse_file(argv[1])

    if len(argv) > 3:
        # Save input assembly in new file for easy comparison
        program.save(argv[3])

    optimize(program, verbose=1)

    if len(argv) > 2:
        # Save output assembly
        program.save(argv[2])
