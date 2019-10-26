import pika
import os
import json
from pprint import pprint
import subprocess

batcmd="cat trackID.json | grep 'spotify:track'"
results = subprocess.check_output(batcmd, shell=True)

with open("tracks.py", "w") as f:
	f.write(results)
