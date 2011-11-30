#!/usr/bin/python
from parser import parse_file
from basic_block import find_basic_blocks
from optimizer import optimize_blocks
from writer import write_statements

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        exit(1)

    # Parse File
    statements = parse_file(argv[1])

    # Create basic blocks
    blocks = find_basic_blocks(statements)

    # Optimize basic blocks
    statements = optimize_blocks(blocks)

    # Rewrite to assembly
    out = write_statements(statements)

    if len(argv) > 2:
        # Save output assembly
        f = open(argv[2], 'w+')
        f.write(out)
        f.close()
