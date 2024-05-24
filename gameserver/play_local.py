import subprocess
import os

# Change to the desired directory
os.chdir("gameserver")

# Call script1.py in a new terminal window
subprocess.Popen(["start", "cmd", "/k", "python", "server.py"], shell=True)

# Call script2.py in a new terminal window
subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)

# Call script3.py in a new terminal window
subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)