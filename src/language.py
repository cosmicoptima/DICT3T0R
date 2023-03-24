import cohere
import json
import openai
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

    def __getattr__(self, name):
        self.random_client().__getattribute__(name)


# co = Rotate([cohere.Client(token) for token in tokens["cohere"]])
co = cohere.Client(tokens["cohere"][0])
openai.api_key = tokens["openai"]


def gen_few_shot_prompt(
    desc: str, examples: list[dict[str, str]], overrides: dict[str, str] = {}
) -> str:
    """Make a formatted few-shot prompt from a description and examples.

    `overrides` contains fields to override in the output."""

    def format_example(ex: dict) -> str:
        res = ""
        for name, val in ex.items():
            res += f"{name}: {val}\n"
        return res.strip("\n")

    return (
        desc
        + "\n\n"
        + "\n--\n".join(format_example(ex) for ex in examples)
        + "\n--\n"
        + format_example(overrides)
        # + f"{list(examples[0].keys())[0]}:"
    )


def parse_response(generation: str, fields: list[str]) -> Optional[dict[str, str]]:
    """Format the result of a prompt from gen_few_shot_prompt."""

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


def generate(
    desc: str,
    examples: list[dict[str, str]],
    fields: list[str],
    overrides: dict[str, str] = {},
):
    prompt = gen_few_shot_prompt(desc, examples, overrides)
    generation = (
        co.generate(prompt, model=COH_MODEL, stop_sequences=["\n--\n"])
        .generations[0]
        .text
    )
    return parse_response(generation, fields)
