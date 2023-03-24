import cohere
import openai
import json
import typing
import random
from typing import Optional

OAI_MODEL = "gpt-3.5-turbo"
COH_MODEL = "xlarge"
TOKEN_FILE = "tokens.json"

tokens = None
with open(TOKEN_FILE) as f:
    tokens = json.load(f)

class Rotate(cohere.Client):
    def __init__(self, clients):
        self.clients = clients

    def random_client(self) -> cohere.Client:
        return random.choice(self.clients)

    def __getattribute__(self, name):
       self.random_client().__getattribute__(name)

co = Rotate([cohere.Client(token) for token in tokens["cohere"]])
openai.api_key = tokens["openai"]


def gen_prompt(desc: str, examples: list[dict[str, str]]) -> str:
    """Make a formatted prompt from a description and examples."""

    def format_ex(ex: dict) -> str:
        res = ""
        for name, val in ex.items():
            res += f"{name}: {val}\n"
        return res.strip("\n")

    return (
        desc
        + "\n\n"
        + "\n--\n".join(format_ex(ex) for ex in examples)
        + "\n--\n"
        # + f"{list(examples[0].keys())[0]}:"
    )


def parse_resp(generation: str, fields: list[str]) -> Optional[dict[str, str]]:
    """Format the result of a prompt from gen_prompt."""
    used_fields = []
    res = {}

    lines = generation.split("\n")
    for line in lines:
        split = line.split(": ")
        if len(split) != 2:
            continue
        title, body = split
        if title in fields:
            used_fields.append(title)
            res[title] = body

    # Only return responses that have every field.
    for field in fields:
        if not (field in used_fields):
            return None
    return res
