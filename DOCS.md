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

stuff

### GUI

stuff


## Usage
*How to use this! Includes setup and usage information!*

### Setup

stuff

### Settings

stuff

### Usage

stuff
