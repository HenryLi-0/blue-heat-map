# Tests all logic bits to make sure changes don't break everything!

passing = 0
total = 0

def assertEqual(name:str, expected, actual):
    global passing, total
    total += 1
    passing += (expected == actual) + 0
    if expected == actual:
        print(name.ljust(50), "\033[38;2;170;255;170mSUCCESS\033[0m")
    else:
        print(name.ljust(50), "\033[38;2;255;170;170mFAILING\033[0m", "| Expected:", expected, "Actual:", actual)

def report():
    global passing, total
    print(("\033[38;2;170;255;170m" if passing == total else "\033[38;2;255;170;170m") + "Tests Report | {} / {} passing.".format(passing, total), "\033[0m")

from backend import *

dataLog = DataLog()
assertEqual("DataLog.toBinary(0)", "0", DataLog.toBinary(0))
assertEqual("DataLog.toBinary(1155, 15)", "000010010000011", DataLog.toBinary(1155, 15))
assertEqual("DataLog.toBinary(2265, 15)", "000100011011001", DataLog.toBinary(2265, 15))
dataLog.packStartingBlock(0,0,0)
assertEqual("dataLog.packStartingBlock(0,0,0)", "0000010000000000000000000000010000000100000000000000000000000", dataLog.dataLog[0])
dataLog.packSafety()
assertEqual("packSafety", "00000000", dataLog.dataLog[1])



report()