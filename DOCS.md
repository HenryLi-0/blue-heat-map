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
storage/
├── players.csv
├── UUID/
│   ├── time.dat
│   ├── time2.dat
│   └── ...
├── UUID2/
│   ├── time.dat
│   └── ...
```

`players.csv` contains a basic table with UUIDs and player names, while the other folders for different players contains different `.dat` files for different sessions. This would allow for viewing of specific player data, along with decent orginization! The structure of our `.dat` files have a couple optimizations, intended to reduce file size!

First, every `.dat` file will have the timestamp as it's file name. This marks the start of the player's session! The `.dat` file will use raw binary for storage, as it would be more efficient for these purposes! The file starts off with the exact position of the player. First, for X and Z coordinates, 26 bits allows for logging more than 30M blocks in both positive and negative numbers, which would allow the full world to be graphed. Next, the Y coordinate would be 8 bits, allowing for 2000 blocks in both positive and negative numbers, as Y coordinates aren't really as important in huge numbers (since, build height ranges from -64 to 320). Therefore, this first block of information takes up 60 bits, or 7.5 bytes!

Afterwards, the optimizations start appearing! Let's first lay some expectations for the quality of our data. Every second seems reasonable to roughly graph what the player's doing, in terms of location. Therefore, let's assume the time interval between every log is a second. With this, we can graph 60 bits every second per player! However, let's think about this. That's ~0.62 megabytes per player per day. Now, the server I'm running this on isn't active often, so such a rate is pretty ok. However, let's say you want to use this on a massive server of one hundred daily active players. That's ~618 MB a day! This is a lot, considering how much we can compact this.

With that said, in game, it is a common occurence for players to stop for at least a second. Therefore, assuming continous running where we log once per second is unnecesarry. Addtionally, logging the exact coordinate also isn't necessarry. For our purposes, being +/- 1 block off isn't too bad, as we just need a general location of the player at a given time. In this case, we can have a system like this:

1. We set a divider.
2. We first write a 64 bit infomration into the file, containing the start information.
3. We set a divider.
4. We wait for the player to move, then start logging the delta time between this and the last move.
5. We set a divider.
6. Then, we log the delta location change.
7. One second into the future...
   - If the player is still moving, we log a divider and delta location change. 
   - If the player is no longer moving, we don't log anything, and go back to step 3.

This way, we're only logging important information. Of course, we can't exactly quantify how much this saves space, as it depends on player movement. But wait, notice how it's saving delta time and delta position. We don't exactly need the exact position every time, just how much it has changed since the last snapshot. Of course, since we are expressing it in binary without accounting for decimals, we will have to track the differences and round up or down in the number for our delta location change while saving. 

Also, one more thing, let's explain what a divider is! Dividers are just little bits of data that state how long the log block after it will be. For example, if upcoming that is 9 bits long, we can do `01001`, which makes the program read the next 9 bits, and then that's the data! Then it expects the next divider, and so on! It will always be 5 bits long (max 32 log block length). By the way, that makes our starting block contain 65 bits of data now!

More optimizations! We don't even need to save every axis! So, we now have a structure like this:

- 6 bits: Data divider
- 2 bits: The type of data (XYZ or time)
- n bits: The change
- Total: 6+2+n bits

In this case, we can save a huge amount of data, given the player walks roughly 5.6 m/s! We will take more bits if we need more information, which really saves a lot of data! This means that, the worse case is if a player is moving extremely quickly, which, as far as Minecraft mechanics go, can't be too bad... unless someone's using a super powerful ender pearl cannon or something.

Ok, so now let's do the worst case scenario, a player that starts moving, stops for a second, then repeats. And they have an elytra. Then, let's just assume they go 60 bps in every axis (which doesn't happen, but let's just assume). In this case, one player joins, we write 60 bits of data, then we have a time log, with 8 bits, being `00011000` for `00011` divider `00` time and `0` seconds since log start. Each divider for space would be `01001`, since the following block data would be 9 bits long. Then, every second includes 3x 15 bits ($6+2+7$).

Therefore, $65+45n$ means, for our cursed server, we would have approximatly ~1MB of data every ~31 minutes, or ~46.3 MB a day! And that's with 100 players online actively with one of the worse case scenarios (aka, this is super compact!)! 

An issue though, we currently have compacted our data so much that a single bit flip to anything would absolutely destroy our setup, either by corrupting a delta, changing all following positions, or by changing a divider, which corrupts all data after it. To fix these issues, we can insert an 8 bit `00000000` after a log block every minute (or long period of inactivity). Additionally, we can create a new session every hour, just to make organizing easier, while also allowing us to correct for small errors and possible data corruptions! In the event that the 8 bit safety log is corrupted, we can always fast forward to the next log block, or, if necessary, the next session. It's likely that the operating system would correct for these errors, but just as a fail safe, and for potentially faster data recall!

Ok, that's great and all, but let's put this into practice. Each `.dat` file will consist of a session of logs.

Let's see an example!

```markdown
# UUID/time.dat

# starting block
11000 # divider
0 000 0000 0000 0000 0000 0000 # x
0 000 0000 # y
0 000 0000 0000 0000 0000 0000 # z

# log (10 seconds after start) (move 1 block XYZ)
00110 # divider
00 1010 # time
00101 # divider
01 0 1 # x
00101 # divider
10 0 1 # y
00101 # divider
11 0 1 # z

# log (after 1 second) (move back, -1 block XYZ)
00101 # divider
01 1 1 # x
00101 # divider
10 1 1 # y
00101 # divider
11 1 1 # z

# after every minute
0000 0000 # safety divider

# after 1 hour, create a new session
```

Real nice! Now, let's get realistic estimates for our quiet server with two players every other day. To simplify math, let's just say one player is always online that is constantly moving 1 block forward and to the side.

So, with this math, every session of one hour would have $65+\left(\left(5+4+5+4\right)\cdot60+8\right)\cdot60$ bits, or 65345 bits, or 8168.125 bytes or ~8 kilobytes. Not too bad!

Now, for every day, we get $\frac{\left(65+\left(\left(5+4+5+4\right)\cdot60+8\right)\cdot60\right)\cdot24}{8\cdot1024\cdot1024}$ MB, which evaluates to ~0.187 megabytes, or ~191.44 kilobytes! Scaling this up, one year of tracking this player moving like this would only be ~68.23804 megabytes a year! Meaning approximately 1 gigabyte of this player's movement every ~15 years!

Now of course, player movement isn't this perfect, but it does show that this system can definitely run on a quiet server for a long time, probably at least a year, without maintainence or checking data limits! Now, does having ~68 megabytes a year instead of ~391 megabytes a year (assuming a 26*4 log block every second) really make a difference for a server that probably won't last multiple years? Probably not. However, what is neat is the ~82.547% reduction in file size!

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
