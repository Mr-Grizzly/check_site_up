import os
import sys
import json
import time

# Settings #
jsonFile_PATH = "record.json"
logFile_PATH = "siteCheck.log"

'''
	JSON structure:
	{websiteName:{'checks':100, 'up':97}}
'''

# Get Website Input #
if len(sys.argv) > 1:
	url = sys.argv[1]
else:
	quit("###ERROR: No url input was given.")

# Check Website Up #
command = f"ping {url} -c 1"
output = os.popen(command).read()


if "packets transmitted, " in output and "packets received, " in output:
	siteIsUp = True
else:
	siteIsUp = False

# Handle Output #
# Update Log File #
with open(logFile_PATH, 'a+') as logFile:
	current_time = time.strftime('%x - %X')
	if siteIsUp:
		writeString = (f"\n{current_time} | {url} | online")
	else:
		writeString = (f"\n{current_time} | {url} | NOT DETECTED / OFFLINE")

	logFile.write(writeString)

# Download Json Count File Data #
with open(jsonFile_PATH) as jsonFile:
	DATA = json.load(jsonFile)

# Update Data #
if url in DATA:
	DATA[url]["checks"] += 1
	if siteIsUp:
		DATA[url]["up"] += 1

elif url not in DATA:
	DATA[url] = {"checks": 1}
	if siteIsUp:
		DATA[url]["up"] = 1

# Save Updated Data #
print(DATA)
with open(jsonFile_PATH, 'w') as jsonFile:
	json.dump(DATA, jsonFile)
