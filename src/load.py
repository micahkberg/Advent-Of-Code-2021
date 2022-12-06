import os


def openfile(filename):
    path = '../inputs'
    os.chdir(path)
    with open(filename, 'r') as f:
        lines = f.read().split("\n")
    return lines
