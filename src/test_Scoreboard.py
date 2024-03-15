from Scoreboard import Scoreboard
import string
import re

Scoreboard.loadScores()

print(Scoreboard.toStr())

Scoreboard.export()