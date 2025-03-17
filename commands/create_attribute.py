# commands/create_attribute.py
from discord import app_commands
from data.attributes import PRIMARY_ATTRIBUTES, attribute_emojis, attribute_emoji_fallbacks

def create_attribute(interaction: discord.Interaction, name: str, emoji: str):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="create_attribute", description="Create a new attribute (admin only)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name="Name of the new attribute", emoji="Emoji for the new attribute")
async def create_attribute(interaction: discord.Interaction, bot: discord.Client, name: str, emoji: str):
    await interaction.response.defer()
    if name in PRIMARY_ATTRIBUTES:
        await interaction.followup.send(f"Attribute {name} already exists!")
        return
    PRIMARY_ATTRIBUTES.append(name)
    attribute_emojis[emoji] = name
    attribute_emoji_fallbacks[name] = emoji.strip(":") if emoji.startswith(":") and emoji.endswith(":") else name.lower()
    await interaction.followup.send(f"Created new attribute {name} with emoji {emoji}")

