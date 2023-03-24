import random
import logging
from language import *


class Quest:
    def __init__(self, desc, exp):
        self.desc = desc
        self.exp = exp


EXAMPLE_QUESTS = [
    ("Retrieve a heavy book from the top shelf.", 2),
    ("Murder somebody and hide the body.", 6),
    ("Turn everybody in the universe into paperclips.", 40),
    ("Use the toilet without wiping.", 3),
    ("Defeat the wizard in hand-to-hand battle.", 8),
]


def generate_quest() -> Quest:
    """Generate an idea for a quest."""
    res = None

    # Retry 3 times to create a response
    for _ in range(3):
        gen = (
            co.generate(
                model=COH_MODEL,
                prompt=gen_prompt(
                    "The following is a list of absurd and humorous quests, along with a experience values."
                    + " More difficult quests reward more experience",
                    [{"Quest": q, "Experience": e} for (q, e) in EXAMPLE_QUESTS],
                ),
                stop_sequences=["--"],
            )
            .generations[0]
            .text
        )
        print(gen)

        res = parse_resp(gen, ["Quest", "Experience"])
        if res:
            return Quest(desc = res["Quest"], exp = res["Experience"])
    raise Exception("No parse in generate_quest completion.")
