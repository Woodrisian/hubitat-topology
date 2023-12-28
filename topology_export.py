#!/usr/bin/python3

import requests
import os
import re
import json
import subprocess

def extract_data_between_lines(input_text, start_line, end_line):
    # Create a regex pattern to match content between start_line and end_line
    pattern = re.compile(f"{re.escape(start_line)}(.*?){re.escape(end_line)}", re.DOTALL)

    # Search for the pattern in the input text
    match = pattern.search(input_text)

    if match:
        # Extract the content between start_line and end_line
        return match.group(1).strip()
    else:
        # Return None if no match is found
        return None

hubitat = os.environ.get("HUBITAT", "http://hubitat.lan")
response = requests.get(hubitat)

response = requests.get(hubitat+"/hub/zigbee/getChildAndRouteInfo")

devices = dict()

direct = extract_data_between_lines(response.text, "Child Data:", "--------------------------------------------------------------------------------")
repeaters = extract_data_between_lines(response.text, "Neighbor Table Entry", "--------------------------------------------------------------------------------")
routes = response.text.split("Route Table Entry\n\n")[1]

for line in direct.split("\n"):
    if "," in line and len(line)>3:
        id = line.split(', ')[1]
        name = line.split(',')[0].replace("[","")
        type = line.split(',')[2].replace("]","").replace(" type:","")
        if devices.get(id)==None:
            devices[id] = dict()

        devices[id]['name'] = name
        devices[id]['type'] = type
        devices[id]['parent'] = "Hubitat"

for line in repeaters.split("\n"):
    if "," in line and len(line)>3:
        id = line.split(', ')[1].replace("]","")
        name = line.split(',')[0].replace("[","")
        if devices.get(id)==None:
            devices[id] = dict()

        devices[id]['name'] = name
        devices[id]['parent'] = "Hubitat"
        devices[id]['children'] = []
for line in routes.split("\n"):
    if "[" in line and len(line)>3:
        id = line.split('[')[1].split(", ")[1].replace("] via ","")
        name = line.split('[')[1].split(", ")[0]
        parent = line.split('[')[2].split(", ")[1].replace("]","")
        if devices.get(id)==None:
            devices[id] = dict()

        devices[id]['name'] = name
        devices[id]['parent'] = parent
        devices[parent]['children'].append(id)
    
with open("devices.json", 'w') as json_file:
    json.dump(devices, json_file, indent=2)
# Dump devices as json
# Convert this into mermaid
# graph TD;
#       A-->B;
#       A-->C;
#       B-->D;
#       C-->D;
mermaid = "graph TD;\n"
mermaid += "  Hubitat[Hubitat]\n"
for device in devices:
    mermaid += ("  "+device+"["+devices[device]['name']+"]\n")
for device in devices:
    mermaid += ("  "+device+"-->"+devices[device]["parent"]+"\n")

with open("topology.mmd", 'w') as text_file:
    text_file.write(mermaid)

cli_command = "docker run --rm -v $PWD:/home/node/data matthewfeickert/mermaid-cli:latest -i topology.mmd -o output.svg"

result = subprocess.run(cli_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check the result
if result.returncode == 0:
    print("Command executed successfully.")
    print("Output:\n", result.stdout)
else:
    print(f"Error executing command. Exit code: {result.returncode}")
    print("Error message:\n", result.stderr)
