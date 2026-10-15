"""Hackathon Escape: a small command-line choose-your-own-adventure game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GameState:
    hour: int = 23
    minute: int = 30
    battery: int = 2
    inventory: List[str] = field(default_factory=list)
    bug_inspected: bool = False
    hint_received: bool = False
    location: str = "desk"
    running: bool = True

    def time_text(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"

    def advance(self) -> None:
        self.minute += 2
        if self.minute >= 60:
            self.hour += self.minute // 60
            self.minute %= 60
        self.battery -= 1

    def has(self, item: str) -> bool:
        return item in self.inventory


SCENES: Dict[str, Dict[str, object]] = {
    "desk": {
        "title": "The Final Hour",
        "text": (
            "It is 11:30 PM. Your hackathon project is due at midnight, "
            "your laptop is at 2% battery, and a bug is blocking the final run."
        ),
    },
    "lab": {
        "title": "The Dark Lab",
        "text": "You slip into the lab. A forgotten charger glints beneath a workbench.",
    },
    "mentor": {
        "title": "The Mentor's Corner",
        "text": "Your mentor is asleep in a chair, surrounded by empty mugs.",
    },
}


def show_status(state: GameState) -> None:
    print(f"\n[{state.time_text()} | battery: {max(state.battery, 0)}%]")


def show_inventory(state: GameState) -> None:
    if state.inventory:
        print("Inventory: " + ", ".join(state.inventory))
    else:
        print("Inventory: empty")


def show_help() -> None:
    print("Choose a numbered option, i to inspect your inventory, h for help, or q to quit.")


def finish(state: GameState, title: str, message: str) -> None:
    print(f"\n=== {title} ===")
    print(message)
    state.running = False


def check_automatic_endings(state: GameState) -> bool:
    if state.battery <= 0 and not state.has("charger"):
        finish(
            state,
            "LAPTOP DIED",
            "The screen flickers once, then goes black. Your last save is trapped inside.",
        )
        return True
    if state.hour >= 24 or (state.hour == 0 and state.minute >= 0):
        finish(
            state,
            "RAN OUT OF TIME",
            "Midnight arrives before you can submit. The hackathon window is closed.",
        )
        return True
    return False


def take_action(state: GameState) -> None:
    """Spend two minutes and one percent battery on a meaningful action."""
    state.advance()
    show_status(state)
    check_automatic_endings(state)


def choose(state: GameState, prompt: str, options: List[str]) -> Optional[int]:
    print(f"\n{prompt}")
    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")
    while state.running:
        try:
            answer = input("> ").strip().lower()
        except EOFError:
            print("\nInput ended. Exiting safely.")
            state.running = False
            return None
        if answer == "i":
            show_inventory(state)
        elif answer == "h":
            show_help()
        elif answer == "q":
            print("You close the laptop and leave the hackathon floor.")
            state.running = False
            return None
        else:
            try:
                selected = int(answer)
            except ValueError:
                print("Please enter a choice number, i, h, or q.")
                continue
            if 1 <= selected <= len(options):
                return selected
            print("That choice is not available right now.")
    return None


def play(state: GameState) -> None:
    print("HACKATHON ESCAPE")
    print("A tiny choose-your-own-adventure game. Every action costs 2 minutes and 1% battery.")
    show_help()
    show_status(state)

    while state.running:
        if state.location == "desk":
            options = [
                "Inspect the bug",
                "Search your backpack",
                "Go to the lab",
                "Visit the sleeping mentor",
                "Submit the project",
                "Take a nap",
            ]
            selected = choose(state, f"{SCENES['desk']['title']}: {SCENES['desk']['text']}", options)
            if selected is None:
                return
            if selected == 1:
                state.bug_inspected = True
                print("You find a suspicious off-by-one error, but you need a debugging hint.")
                take_action(state)
            elif selected == 2:
                if state.has("chai"):
                    print("Your backpack is empty except for the chai you already found.")
                else:
                    state.inventory.append("chai")
                    print("You find a warm cup of chai. Maybe it can wake someone up.")
                take_action(state)
            elif selected == 3:
                state.location = "lab"
                take_action(state)
            elif selected == 4:
                state.location = "mentor"
                take_action(state)
            elif selected == 5:
                if state.bug_inspected and state.hint_received and state.has("charger"):
                    finish(state, "YOU WIN", "You fix the bug, plug in the laptop, and submit with 2 minutes to spare!")
                elif state.bug_inspected and state.hint_received:
                    finish(state, "SUBMITTED WITH THE BUG", "You submit the project, but the laptop is still dying and the bug remains.")
                else:
                    finish(state, "SUBMITTED WITH THE BUG", "You submit in a panic. The judges can see the bug, but at least something arrived.")
            elif selected == 6:
                finish(state, "TOOK A NAP", "You set an alarm for 11:35 PM and immediately fall asleep. It does not ring.")
        elif state.location == "lab":
            options = ["Pick up the charger", "Return to the desk"]
            selected = choose(state, f"{SCENES['lab']['title']}: {SCENES['lab']['text']}", options)
            if selected is None:
                return
            if selected == 1:
                if state.has("charger"):
                    print("You already have the charger.")
                else:
                    state.inventory.append("charger")
                    state.battery = 100
                    print("You find the charger and connect it. The laptop jumps to 100%!")
                state.location = "desk"
                take_action(state)
            else:
                state.location = "desk"
                take_action(state)
        elif state.location == "mentor":
            options = ["Offer the chai", "Leave quietly"]
            selected = choose(state, f"{SCENES['mentor']['title']}: {SCENES['mentor']['text']}", options)
            if selected is None:
                return
            if selected == 1:
                if state.has("chai"):
                    state.hint_received = True
                    state.inventory.remove("chai")
                    print("The mentor wakes, drinks the chai, and says: 'Check the loop boundary.'")
                else:
                    print("You whisper a greeting, but the mentor sleeps through it. Chai would help.")
                state.location = "desk"
                take_action(state)
            else:
                state.location = "desk"
                take_action(state)


def main() -> None:
    play(GameState())


if __name__ == "__main__":
    main()
