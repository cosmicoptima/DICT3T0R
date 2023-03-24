import random
import logging
from language import *
from enum import Enum


class Quest:
    def __init__(self, desc, exp):
        self.desc = desc
        self.exp = exp


EXAMPLE_QUESTS: list[tuple[str, int]] = [
    ("Retrieve a heavy book from the top shelf.", 2),
    ("Murder somebody and hide the body.", 6),
    ("Turn everybody in the universe into paperclips.", 40),
    ("Use the toilet without wiping.", 3),
    ("Defeat the wizard in hand-to-hand battle.", 8),
]


def generate_quest() -> Quest:
    """Generate an idea for a quest."""
    res = None
    gen = (
        co.generate(
            model=COH_MODEL,
            prompt=gen_prompt(
                "The following is a list of absurd and humorous quests, along with a experience values."
                + " More difficult quests reward more experience",
                [{"Quest": q, "Experience": str(e)} for (q, e) in EXAMPLE_QUESTS],
            ),
            stop_sequences=["--"],
        )
        .generations[0]
        .text
    )
    print(gen)

    res = parse_resp(gen, ["Quest", "Experience"])
    if res:
        return Quest(desc=res["Quest"], exp=res["Experience"])
    raise Exception("No parse in generate_quest completion.")


class Strength(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    GODLY = "godly"


EXAMPLE_BOONS: list[tuple[str, Strength]] = [
    ("Your senses have expanded to full 360 degree visual awareness.", Strength.MEDIUM),
    (
        "You have a small understanding of mathematics, allowing you to follow simple conversations about statistics.",
        Strength.WEAK,
    ),
    # ("You gain an extra 1d8 bonus to your initiative rolls.", Strength.WEAK),
    ("You gain the ability to fly.", Strength.STRONG),
    ("You may turn one person a day into a hamster. If you do so, you become unable to walk.", Strength.STRONG)
]


def generate_boon(strength: Strength) -> str:
    res = None
    gen = (
        co.generate(
            model=COH_MODEL,
            prompt=gen_prompt(
                "The following is a list of boons, of varying power levels.",
                [
                    {"Power": str(power), "Boon": boon}
                    for (boon, power) in EXAMPLE_BOONS
                ],
                overrides={"Power": str(strength)},
            ),
            stop_sequences=["--"],
        )
        .generations[0]
        .text
    )
    print(gen)

    res = parse_resp(gen, ["Boon"])
    if res:
        return res["Boon"]
    raise Exception("No parse in generate_boon completion.")
