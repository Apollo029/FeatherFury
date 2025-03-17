# commands/edit_bot.py
from discord import app_commands
from data.attributes import PRIMARY_ATTRIBUTES

def edit_bot_profile(interaction: discord.Interaction, bot_user: discord.Member, class_type: str, attributes: str):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="edit_bot_profile", description="Edit a bot's profile (admin only)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(bot_user="The bot to edit", class_type="The bot's new class", attributes="Comma-separated attributes (e.g., Fire,Water,Ice)")
async def edit_bot_profile(interaction: discord.Interaction, bot: discord.Client, bot_user: discord.Member, class_type: str, attributes: str):
    await interaction.response.defer()
    if not bot_user.bot:
        await interaction.followup.send(f"{bot_user.mention} is not a bot!")
        return
    if class_type not in CLASS_STATS and class_type != "All Classes":
        await interaction.followup.send(f"Invalid class type {class_type}. Available: {', '.join(CLASS_STATS.keys())}")
        return
    attr_list = [attr.strip() for attr in attributes.split(",")]
    if len(attr_list) > 3:
        await interaction.followup.send("A bot can only have up to 3 attributes!")
        return
    for attr in attr_list:
        if attr not in PRIMARY_ATTRIBUTES:
            await interaction.followup.send(f"Invalid attribute {attr}. Available: {', '.join(PRIMARY_ATTRIBUTES)}")
            return
    bot.global_player_profiles[bot_user.id] = {
        "class": class_type,
        "attributes": attr_list,
        "race": bot.global_player_profiles.get(bot_user.id, {}).get("race", "BotRace_1"),
        "stats": {
            "wins": 0,
            "losses": 0,
            "total_battles": 0,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "critical_hits": 0,
            "critical_wins": 0,
            "bots_beaten": 0,
            "losses_to_bots": 0
        },
        "level": bot.global_player_profiles.get(bot_user.id, {}).get("level", 1),
        "xp": 0,
        "race_effects": bot.global_player_profiles.get(bot_user.id, {}).get("race_effects", {"effects": [], "power_index": 0})
    }
    await interaction.followup.send(f"Updated profile for {bot_user.mention}: Class: {class_type}, Attributes: {attr_list}")

