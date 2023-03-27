from dataclasses import dataclass
from language import render_prompt_template
from enum import Enum


@dataclass
class Quest:
    description: str
    xp: int


class Power(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    GODLY = "godly"


@dataclass
class Boon:
    description: str
    strength: Power


boon_template = render_prompt_template("boon")
quest_template = render_prompt_template("quest")


def generate_quest() -> Quest:
    """Generate a quest."""

    quest_object = quest_template.generate({})
    if quest_object is None:
        raise Exception("No parse in generate_quest completion")
    return Quest(quest_object["Description"], int(quest_object["XP"]))


def generate_boon(strength: Power) -> Boon:
    """Generate a boon."""

    boon_object = boon_template.generate({"Strength": strength.value})
    if not boon_object:
        raise Exception("No parse in generate_boon completion")
    return Boon(boon_object["Description"], Power(boon_object["Strength"]))
