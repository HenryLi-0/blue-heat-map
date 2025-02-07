# blue-heat-map
someone broke my redstone contraption :/ (very unfortunate)

logically, the solution is to write something to analyze player server activity!

**NOTE: still under development!**

### Setup:

The Minecraft server this is analyzing must use [Bluemap](https://github.com/BlueMap-Minecraft/BlueMap), and have `[web view]/maps/world/live/players.json` accessible!

If you're really commited to this, you can have any device with an internet connection to, ideally, run this! Here's some steps for a `Raspberry Pi Zero 2W`!

**TO-DO: update this in the future!**

1. `scp` the file from the computer to the raspberry pi (use the actual file location on the raspberry pi for the other steps)
2. `ssh` into the rasbperry pi with Windows Powershell
3. `nano main.py` and modify settings if needed (`PLAYERS_JSON` and `RPI`)
4. `sudo nohup python main.py &` to start running the script in the background
5. should run continuously until something breaks!
   - use `ps aux | grep python` to check if its running
   - use `sudo kill [PID]` to kill the process (PID is in the number in the second column)
