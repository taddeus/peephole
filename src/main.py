#!/usr/bin/python
from parser import parse_file
from optimize import optimize
from writer import write_statements

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        exit(1)

    # Parse File
    statements = parse_file(argv[1])
    statements = optimize(statements, verbose=1)

    # Rewrite to assembly
    out = write_statements(statements)

    if len(argv) > 2:
        # Save output assembly
        f = open(argv[2], 'w+')
        f.write(out)
        f.close()
