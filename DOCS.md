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

Initially, the plan was to create an extremely compact system, with the side effects of having a lot of negative tradeoffs, from complexity to risk of data loss to needing the entire file to parse for a potentially +/- 1 second timestamp. Additionally, a single bit flip would corrupt the entire file, so I guess that was a bad idea? Anyways, check the commit history if you want to read the docs on that, the entire plan was (keyword: was) written here.

Anyways, new plan? SQLite. Should make things sweeter to write! Similarly to the original idea, we will have the same file structure:

```
storage/
├── players.db
├── UUID/
│   ├── time.db
│   ├── time2.db
│   └── ...
├── UUID2/
│   ├── time.db
│   └── ...
```

The `storage` folder contains everything, with a `players.db` file to store the player UUIDs and their usernames. Then, we have individual folders with the player UUID, each containing files named `time.db` for each session. Each session represents a time from log on to log off. In the event the session goes over a set time frame, a new session is created! The timestamp in the file name should speed up processing.

Here's what we log! `(delta timestamp, x, y, z, f)`, and that's all! After a set amount of sessions, the system should automatically compress `.db` files into a zip! Running this on a set of ten `.db` files for 3600 logs each (representative of one log per second for an hour), we get `1310720 bytes`. That's for data looking like: `(1155 843086 513 126799 0)` for each log! Afterwards, after compression of these ten log files, we get `724992 bytes`, a 44.6% reduction!

Given this, if ten hours of logging a player roughly equates to `0.8 MB`, rounding up for safety, this suggests `0.08 MB per hour`! Now, scaling this upwards, let's estimate our server to have a single active player at all times, constantly moving! Realistically, the server this is built for won't have that type of activity, but just a stress test! That means, with `1 GB` of storage, the system could log roughly `533 days` of information, which is pretty good for our needs! (yes, not as cool as 1 GB per ~15 years, but that system would've been horrifying to implement, use, and maintain)

And that's really it!

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
