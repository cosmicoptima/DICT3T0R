from discord import Client, Intents, TextChannel

DEBUG_CHANNEL = 1088962537460084806

intents = Intents.default()
intents.members = True
intents.message_content = True

client = Client(intents=intents)


async def debug_print(text: str):
    channel = client.get_channel(DEBUG_CHANNEL)
    if isinstance(channel, TextChannel):
        await channel.send(f"```\n{text}\n```")
