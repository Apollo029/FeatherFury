# commands/reset_class.py
from discord import app_commands

def reset_class(interaction: discord.Interaction):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="reset_class", description="Reset your class and race (admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def reset_class(interaction: discord.Interaction, bot: discord.Client):
    await interaction.response.defer()
    user = interaction.user
    guild = interaction.guild
    if user.id in bot.global_player_profiles:
        current_class = bot.global_player_profiles[user.id].get("class")
        current_race = bot.global_player_profiles[user.id].get("race")
        bot.global_player_profiles[user.id] = {
            "class": None,
            "attributes": [],
            "race": None,
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
            "level": 1,
            "xp": 0,
            "race_effects": {"effects": [], "power_index": 0}
        }
        class_role = discord.utils.get(guild.roles, name=current_class) if current_class else None
        race_role = discord.utils.get(guild.roles, name=current_race) if current_race else None
        if class_role and class_role in user.roles:
            await user.remove_roles(class_role)
        if race_role and race_role in user.roles:
            await user.remove_roles(race_role)
        await interaction.followup.send(f"{user.mention}, your class and race have been reset!")
    else:
        await interaction.followup.send(f"{user.mention}, you have no class or race to reset.")

