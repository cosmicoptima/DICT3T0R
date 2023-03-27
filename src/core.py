from asyncio import create_task
from discord import Client, Intents, TextChannel
from traceback import format_exc

DEBUG_CHANNEL = 1088962537460084806

intents = Intents.default()
intents.members = True
intents.message_content = True

client = Client(intents=intents)


def debug_print(text: str):
    channel = client.get_channel(DEBUG_CHANNEL)
    if isinstance(channel, TextChannel):
        create_task(channel.send(f"```\n{text}\n```"))


# decorator to debug print on exceptions

def debug_on_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            debug_print(format_exc())

    return wrapper
