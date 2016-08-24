from BfReader import BfReader
import sys

if (len(sys.argv) <= 1):
    exit("No file name specified")

with open(sys.argv[1], 'r') as f:
    msg = f.read()

x = BfReader()
x.eval_bf(msg)
#print(len(msg))
