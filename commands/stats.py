# commands/stats.py
from discord import app_commands

def stats(interaction: discord.Interaction, user: discord.Member = None):
    # This function will be called as a method in core/bot.py
    pass  # Logic will be moved to core/bot.py

@app_commands.command(name="stats", description="View your stats or another user's stats")
@app_commands.describe(user="The user to view stats for (default: yourself)")
async def stats(interaction: discord.Interaction, bot: discord.Client, user: discord.Member = None):
    await interaction.response.defer()
    target = user if user else interaction.user
    if target.id not in bot.global_player_profiles:
        await interaction.followup.send(f"{target.mention} has not set up a profile yet!")
        return
    profile = bot.global_player_profiles[target.id]
    embed = discord.Embed(title=f"{target.name}'s Stats", color=discord.Color.gold())
    embed.add_field(name="Class", value=profile["class"] or "None", inline=True)
    embed.add_field(name="Attributes", value=", ".join(profile["attributes"]) if profile["attributes"] else "None", inline=True)
    embed.add_field(name="Race", value=profile["race"] or "None", inline=True)
    embed.add_field(name="Race Effects", value=", ".join([f"{effect['name']}: {effect['value']}" for effect in profile["race_effects"]["effects"]]) if profile["race_effects"]["effects"] else "None", inline=False)
    embed.add_field(name="Level", value=profile["level"], inline=True)
    embed.add_field(name="Wins/Losses", value=f"{profile['stats']['wins']}/{profile['stats']['losses']}", inline=True)
    embed.add_field(name="Total Battles", value=profile["stats"]["total_battles"], inline=True)
    embed.add_field(name="Damage Dealt", value=profile["stats"]["total_damage_dealt"], inline=True)
    embed.add_field(name="Damage Taken", value=profile["stats"]["total_damage_taken"], inline=True)
    embed.add_field(name="Critical Hits", value=profile["stats"]["critical_hits"], inline=True)
    await interaction.followup.send(embed=embed)
