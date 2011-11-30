#!/usr/bin/python
from parser import parse_file
from basic_block import find_basic_blocks

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        exit(1)

    statements = parse_file(argv[1])
    blocks = find_basic_blocks(statements)

    #for i, statement in enumerate(statements):
    #    print i, statement

    for i, block in enumerate(blocks):
        print '\nbasic block %d:' % i

        for statement in block:
            print statement
