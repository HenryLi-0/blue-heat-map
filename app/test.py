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
