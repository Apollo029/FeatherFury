# utils/roles.py
import discord

async def assign_dead_role(user: discord.Member):
    guild = user.guild
    dead_role = discord.utils.get(guild.roles, name="Dead")
    if not dead_role:
        try:
            dead_role = await guild.create_role(name="Dead")
            print(f"Created Dead role in {guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to create Dead role in {guild.name}")
            return
    if dead_role not in user.roles:
        try:
            await user.add_roles(dead_role)
            print(f"Assigned Dead role to {user.name} in {guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to assign Dead role to {user.name} in {guild.name}")

async def remove_dead_role(user: discord.Member):
    dead_role = discord.utils.get(user.guild.roles, name="Dead")
    if dead_role and dead_role in user.roles:
        try:
            await user.remove_roles(dead_role)
            print(f"Removed Dead role from {user.name} in {user.guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to remove Dead role from {user.name} in {user.guild.name}")

async def assign_battle_ready_role(user: discord.Member):
    guild = user.guild
    battle_ready_role = discord.utils.get(guild.roles, name="Battle Ready")
    if not battle_ready_role:
        try:
            battle_ready_role = await guild.create_role(name="Battle Ready")
            print(f"Created Battle Ready role in {guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to create Battle Ready role in {guild.name}")
            return
    if battle_ready_role not in user.roles:
        try:
            await user.add_roles(battle_ready_role)
            print(f"Assigned Battle Ready role to {user.name} in {guild.name}")
        except discord.Forbidden:
            print(f"Missing permissions to assign Battle Ready role to {user.name} in {guild.name}")
