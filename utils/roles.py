# utils/roles.py
import discord

async def assign_dead_role(guild, user):
    dead_role = discord.utils.get(guild.roles, name="Dead")
    if not dead_role:
        try:
            dead_role = await guild.create_role(name="Dead", color=discord.Color.grey())
            print(f"Created Dead role in {guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to create Dead role in {guild.name}")
            return
    if dead_role:
        try:
            await user.add_roles(dead_role)
            print(f"Assigned Dead role to {user.display_name}")
        except discord.Forbidden:
            print(f"Failed to assign Dead role to {user.display_name} - missing permissions")
