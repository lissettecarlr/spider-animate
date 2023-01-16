import os
from sys import argv


projectPath = os.path.dirname(os.path.realpath(argv[0])).replace("\\", "/")

class defaultConfig(object):
    projectName = "temp"
    alarmClock = "23:00"
    overSleep = 60
    cycleSleep = 1

