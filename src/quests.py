from dataclasses import dataclass
from language import generate
from enum import Enum


@dataclass
class Quest:
    desc: str
    exp: int


class Power(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    GODLY = "godly"


@dataclass
class Boon:
    desc: str
    strength: Power


EXAMPLE_QUESTS: list[tuple[str, int]] = [
    ("Retrieve a heavy book from the top shelf.", 2),
    ("Murder somebody and hide the body.", 6),
    ("Turn everybody in the universe into paperclips.", 40),
    ("Use the toilet without wiping.", 3),
    ("Defeat the wizard in hand-to-hand battle.", 8),
]


def generate_quest() -> Quest:
    """Generate a quest."""

    raw_quest = generate(
        "The following is a list of absurd and humorous quests, along with a experience values.",
        [{"Quest": q, "Experience": str(e)} for (q, e) in EXAMPLE_QUESTS],
        ["Quest", "Experience"],
    )
    if not raw_quest:
        raise Exception("No parse in generate_quest completion.")
    return Quest(raw_quest["Quest"], int(raw_quest["Experience"]))


EXAMPLE_BOONS: list[tuple[str, Power]] = [
    ("Your senses have expanded to full 360 degree visual awareness.", Power.MEDIUM),
    (
        "You have a small understanding of mathematics, allowing you to follow simple conversations about statistics.",
        Power.WEAK,
    ),
    # ("You gain an extra 1d8 bonus to your initiative rolls.", Strength.WEAK),
    ("You gain the ability to fly.", Power.STRONG),
    (
        "You may turn one person a day into a hamster. If you do so, you become unable to walk.",
        Power.STRONG,
    ),
]


def generate_boon(strength: Power) -> Boon:
    """Generate a boon."""

    raw_boon = generate(
        "The following is a list of absurd and humorous boons.",
        [{"Strength": s.value, "Boon": b} for (b, s) in EXAMPLE_BOONS],
        ["Strength", "Boon"],
        {"Strength": strength.value},
    )
    if not raw_boon:
        raise Exception("No parse in generate_boon completion.")
    return Boon(raw_boon["Boon"], Power(raw_boon["Strength"]))
