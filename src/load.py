import os


def openfile(filename):
    path = 'C://Users/bobth/Documents/programming/Advent-Of-Code-2021/inputs'
    with os.chdir(path):
        with open(filename, 'r') as f:
            lines = f.read().split("\n")
    return lines
