#!/usr/bin/python
from parser import parse_file
from basic_block import find_basic_blocks
from writer import write_statements

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        exit(1)

    statements = parse_file(argv[1])
    blocks = find_basic_blocks(statements)
    out = write_statements(statements)

    statement_no = 1

    for i, block in enumerate(blocks):
        #print 'basic block %d:' % i

        for statement in block:
            #print statement_no, statement
            statement_no += 1

    #print '\nOut:'
    #print out

    if len(argv) > 2:
        f = open(argv[2], 'w+')
        f.write(out)
        f.close()
