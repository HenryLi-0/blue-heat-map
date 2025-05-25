import os, time

def clamp(value:int, maxV:int):
    return max(-maxV, min(value, maxV))

def roundf(value:int, precision:int):
    return round(value*(10**precision))/(10**precision)

class Debug:
    init = False
    debug = None
    @staticmethod
    def get():
        if not(Debug.init):
            Debug.debug = Debug()
            Debug.debug.log("Debug", False, "new debug log")
        return Debug.debug
    def __init__(self):
        self.init = True
        self.initTime = round(time.time())
        self.path = os.path.join("app", "storage", "debug-{}.txt".format(self.initTime))
        with open(self.path, "w") as f:
            f.write("")
            f.close()
    def log(self, name, error, text):
        data = "{:8} | {} | {:20} | {}".format(
            round((time.time() - self.initTime)*1000)/1000,
            "X" if error else " ",
            name,
            text
        )
        with open(self.path, "a") as f:
            f.write(data)
            f.close()