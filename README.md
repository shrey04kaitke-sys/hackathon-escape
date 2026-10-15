# Hackathon Escape

Hackathon Escape is a small Python command-line choose-your-own-adventure game. It is
11:30 PM, a hackathon project is due at midnight, the laptop is at 2% battery, and
there is a bug in the code. Can you escape with a working submission?

## Run

Requires Python 3.8 or newer. No external libraries are needed.

```text
python hackathon_escape.py
```

## How to play

Type the number for an available choice and press Enter.

- `i` shows your inventory.
- `h` shows the help message.
- `q` quits.

Every meaningful action costs two minutes and one percent of battery. Invalid input
does not cost time. Pressing Ctrl+D (or sending EOF) exits safely.

Find the chai in the backpack to wake the mentor and receive a debugging hint. Find
the charger in the lab to restore the laptop. The game has five endings:

1. **You Win** - fix the bug with the hint, find the charger, and submit.
2. **Submitted with the Bug** - submit without everything needed to fix the project.
3. **Laptop Died** - spend the last battery before finding the charger.
4. **Took a Nap** - choose to sleep.
5. **Ran Out of Time** - keep acting until midnight.

## How it works

The story scenes are stored in the `SCENES` dictionary. A `GameState` dataclass tracks
the clock, battery, location, inventory, and progress flags. The main loop displays
the current scene, accepts commands, and advances the clock by two minutes for each
action. Ending checks run after actions that consume time, while submission and nap
are immediate story endings.
