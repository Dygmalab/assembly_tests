from enum import Enum
from keycode import Keycode

MACRO_ACTION_END = 0
MACRO_ACTION_STEP_INTERVAL = 1
MACRO_ACTION_STEP_WAIT = 2
MACRO_ACTION_STEP_KEYDOWN = 3
MACRO_ACTION_STEP_KEYUP = 4
MACRO_ACTION_STEP_TAP = 5
MACRO_ACTION_STEP_KEYCODEDOWN = 6
MACRO_ACTION_STEP_KEYCODEUP = 7
MACRO_ACTION_STEP_TAPCODE = 8

class Macro():

    def __init__(self): 
        self.seq = []

    def format(self):
        return self.seq + [MACRO_ACTION_END]

    def addKeyTap(self, keycode):
        self.seq.append(MACRO_ACTION_STEP_TAPCODE)
        self.seq.append(keycode)

    def addInterval(self, interval):
        self.seq.append(MACRO_ACTION_STEP_INTERVAL)
        self.seq.append(interval)

class Macros():

    def __init__(self): 
        self.macros = []

    def createMacro(self):
        macro = Macro()
        self.macros.append(macro)
        return macro

    def format(self):
        all_macros = []
        for m in self.macros:
            all_macros += m.format()
        all_macros.append(MACRO_ACTION_END)
        macro_string = ""
        for m in all_macros:
            macro_string += str(m)
            macro_string += " "
        return macro_string

macros = Macros()
macro = macros.createMacro()
macro.addInterval(10)
macro.addKeyTap(Keycode.M)
macro.addKeyTap(Keycode.A)
macro.addKeyTap(Keycode.T)
macro.addKeyTap(Keycode.T)
print(macros.format())
