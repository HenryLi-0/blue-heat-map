# Documentation!

Here's just a bit of documentation on how this thing works! Skip around sections if needed!

## Concept
*The basic idea behind parts of this!*

### The "API"

Even though I'm not exactly sure if `[web view]/maps/world/live/players.json` is intended to act like an API, it still sort of functions like one. Here's an example of what it can contain:

```json
{
    "players": [
        {
            "uuid": "some uuid",
            "name": "some username",
            "foreign": false,
            "position": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "rotation": {
                "pitch": 0.0,
                "yaw": 90.0,
                "roll": 0.0
            }
        }
    ]
}
```

Here's what these values seems to mean, determined by observing how the data changes:
- "uuid": the player UUID, different for every player
- "name": the player's username
- "foreign": `false` when in the overworld, `true` when in the nether
- "position": contains `xyz` data about the player's position, using the Minecraft coordinate system (`y` is occasionally up to +/-1 off)
- "rotation": contains player rotation data

### Data Storage

Data storage, when you're storing a bunch of player activity to process, is obviously a task that needs to be done in a not too janky way. First, let's sort out what information we think is useful. Let's say I want to look at who broke my redstone contraption. To do this, we need player location information. With this, some one can see that if a player is in the area recently, they likely caused the incident. However, how can we be sure? Another possible situation this interaction could have been just a random player exploring the area that just so unfortunately stumbled into the mess. Therefore, time data would also be very handy! Also, one more thing that's pretty obvious, we need the player UUID and username!

So, we have the user, their coordinates and its time information, which would allow us to graph the movement of players across time! Very handy! However, a couple more things to sort out. The "API" currently returns the coordinate position to a strangely accurate decimal precision. Realistically, one or two numbers behind the decimal point is already enough for our purposes, if not zero numbers. Thinking about it, that data isn't all too useful, so we'll determine it once storage estimated come out.

Therefore, we can create a storage system:

```
...storage/
├── players.csv
└── players/
    ├── UUID0.csv
    ├── UUID1.csv
    ├── UUID2.csv
    └── ...
```

`players.csv` contains a basic table with UUIDs and player names, while `players/` contains different `csv` files for different players. This would allow for viewing of specific player data, along with decent orginization!

stuff

### GUI

The GUI is built with `flask`! It's also my first experiments with trying out `flask` (and like my third try learning this web development stuff), so that's something! 

stuff

## Usage
*How to use this! Includes setup and usage information!*

### Setup

Modules:
- `flask`: The GUI is built with `flask`, which can be installed by running `pip install Flask` on Windows! The Raspberry Pi's setup process is a bit different, at least, in my experince. To learn more about it, just pull up your favorite web browser and it'll probably be able to tell you more! 

### Settings

stuff

### Usage

stuff
