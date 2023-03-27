from core import debug_print

from abc import ABC, abstractmethod
import cohere
from dataclasses import dataclass
import json
import openai
import random
from typing import Any, List, Optional
from yaml import CLoader, load

OAI_MODEL = "gpt-3.5-turbo"
COH_MODEL = "xlarge"
TOKEN_FILE = "tokens.json"

tokens = None
with open(TOKEN_FILE) as f:
    tokens = json.load(f)

openai.api_key = tokens["openai"]


def cohere_token_is_valid(token: str) -> bool:
    client = cohere.Client(token)
    try:
        client.tokenize(" ")
        return True
    except cohere.CohereAPIError:
        return False


cohere_clients = []
cohere_tokens = []

for token in tokens["cohere"]:
    if cohere_token_is_valid(token):
        cohere_clients.append(cohere.Client(token))
        cohere_tokens.append(token)
    else:
        debug_print(f"Invalid token, removing: {token}")

tokens["cohere"] = cohere_tokens
with open(TOKEN_FILE, "w") as f:
    json.dump(tokens, f)


def co() -> cohere.Client:
    return random.choice(cohere_clients)


def add_cohere_token(token: str) -> bool:
    if cohere_token_is_valid(token):
        cohere_clients.append(cohere.Client(token))
        with open(TOKEN_FILE, "w") as f:
            json.dump(tokens, f)
        return True

    return False


class PromptTemplate(ABC):
    @abstractmethod
    def generate(self, _: Any) -> Any:
        pass


@dataclass
class FewShotObjectPromptTemplate(PromptTemplate):
    description: str
    input_keys: List[str]
    output_keys: List[str]
    examples: List[dict[str, str]]

    def _generate_prompt(self, input_dict: dict[str, str]) -> str:
        def format_item(item: dict) -> str:
            input_keys = [k for k in item.keys() if k in self.input_keys]
            output_keys = [k for k in item.keys() if k in self.output_keys]
            keys = input_keys + output_keys
            return "\n".join([f"{k}: {item[k]}" for k in keys])

        items = self.examples + [input_dict]
        return (
            self.description
            + "\n\n"
            + "\n--\n".join(format_item(item) for item in items)
        )

    def _parse_response(self, response: str) -> Optional[dict[str, str]]:
        output = {}

        lines = response.split("\n")
        for line in lines:
            try:
                key, value = line.split(": ")
            except ValueError:
                continue
            
            output[key] = value

        if set(output.keys()) == set(self.output_keys):
            return output
        return None
    
    def generate(self, input_dict: dict[str, str]) -> Optional[dict[str, str]]:
        prompt = self._generate_prompt(input_dict)
        response = (
            co().generate(
                prompt,
                model=COH_MODEL,
                stop_sequences=["\n--\n"],
                max_tokens=256,
                temperature=1,
                p=0.9,
            )
            .generations[0]
            .text
        )
        return self._parse_response(response)


def render_prompt_template(path: str) -> PromptTemplate:
    with open(f"prompts/{path}.yml") as f:
        data = load(f, Loader=CLoader)

    if data["type"] == "few-shot-object":
        return FewShotObjectPromptTemplate(
            data["description"],
            data["input_keys"],
            data["output_keys"],
            data["examples"],
        )

    raise ValueError(f"Invalid prompt template type: {data['type']}")
