#!/usr/bin/python
from src.parser import parse_file
from src.optimize import optimize
from src.writer import write_statements

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s SOURCE_FILE [ OUT_FILE [ SOURCE_OUT_FILE ] ]' \
                % argv[0]
        exit(1)

    # Parse File
    original = parse_file(argv[1])

    if len(argv) > 3:
        # Save input assembly in new file for easy comparison
        out = write_statements(original)
        f = open(argv[3], 'w+')
        f.write(out)
        f.close()

    optimized = optimize(original, verbose=1)

    if len(argv) > 2:
        # Save output assembly
        out = write_statements(optimized)
        f = open(argv[2], 'w+')
        f.write(out)
        f.close()
