import sys
import re
import time
from datetime import datetime, timedelta

# Creating a custom string class to be able to write out delta times
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


# end

inFile = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\SlayTheSpire\\sendToDevs\\logs\\SlayTheSpire.log"
stages = []
obtainedCards = []

with open(inFile, 'r') as file:
    lines = file.readlines()

# Begin Session length
sessionBeginMatch = re.search(r'\d{2}:\d{2}:\d{2}.\d{3}', lines[0]).group(0)
sesssionEndMatch = re.search(r'\d{2}:\d{2}:\d{2}.\d{3}', lines[-1]).group(0)

sessionBeginTime = datetime(*(time.strptime(sessionBeginMatch, '%H:%M:%S.%f'))[:7])
sessionEndTime = datetime(*(time.strptime(sesssionEndMatch, '%H:%M:%S.%f'))[:7])

sessionLength = sessionEndTime - sessionBeginTime
# end Session Length

# Begin Stage/ Card gathering
for line in lines:
    lineToSearch = re.search(r"(?<=MainMusic:) .*", line)
    if lineToSearch is not None:
        FoundLine = lineToSearch.group(0)
        if FoundLine not in stages:
            stages.append(FoundLine)
    else:
        lineToSearch = re.search(r"(?<=INFO helpers.CardHelper> Obtained) .*\)", line)
        if lineToSearch is not None:
            FoundLine = lineToSearch.group(0)
            obtainedCards.append(FoundLine)

# end

print("STAGES VISITED: ")
for item in stages:
    print(item)

print("\nNon-Default cards obtained: ")
for item in obtainedCards:
    print(item)

print("\nSession Length: ", strfdelta(sessionLength, "%H hours %M minutes %S seconds"))
