# core/events.py
import discord
import random
from datetime import datetime, timedelta  # Add this import
import pytz
import asyncio
import json
from data.classes import CLASS_STATS, CLASS_ANNOUNCEMENTS
from data.attributes import ATTRIBUTE_ANNOUNCEMENTS, PRIMARY_ATTRIBUTES, attribute_emojis, FLAIR, ATTRIBUTE_DESCRIPTIONS
from data.constants import CHANNEL_CONFIGS
from data.class_types import generate_race_effects

async def on_ready(bot):
    print("on_ready event triggered")
    start_time = datetime.now(pytz.UTC)
    print(f"Starting on_ready for {bot.bot_name} at {start_time}...")

    # Print guild information
    guilds = bot.guilds
    print(f"Found {len(guilds)} guilds")

    # Setup for each guild
    for guild in guilds:
        print(f"Processing guild setup for {guild.name} (ID: {guild.id})")
        # Find or create necessary channels
        for channel_name in CHANNEL_CONFIGS.values():
            channel = discord.utils.get(guild.text_channels, name=channel_name.lstrip('#'))
            raw_channel_name = channel_name.lstrip('#')
            print(f"Checking for existing channel: {channel_name} (raw: {raw_channel_name}), found: {channel.name if channel else None}")
            if not channel:
                try:
                    channel = await guild.create_text_channel(raw_channel_name)
                    print(f"Created channel {channel_name} in {guild.name}")
                except discord.Forbidden:
                    print(f"Missing permissions to create channel {channel_name} in {guild.name}")
                    continue
            print(f"Reusing existing channel: {channel.name} (ID: {channel.id})")

        # Clear the stats channel (temporary for this test)
        stats_channel = discord.utils.get(guild.text_channels, name=CHANNEL_CONFIGS["stats_channel"].lstrip('#'))
        if stats_channel:
            try:
                async for message in stats_channel.history(limit=100):
                    if message.author == bot.user:
                        await message.delete()
                        print(f"Deleted old stats message in {guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to delete messages in {stats_channel.name}")

        # Restore profiles from stats embeds (this will now be empty after clearing)
        if stats_channel:
            try:
                async for message in stats_channel.history(limit=100):
                    if message.author == bot.user and message.embeds:
                        embed = message.embeds[0]
                        if "Stats" in embed.title:
                            user_name = embed.title.split("'s")[0]
                            user = discord.utils.get(guild.members, display_name=user_name)
                            if user:
                                profile = {
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
                                        "losses_to_bots": 0,
                                        "monthly_trophies": 0,
                                        "quarterly_trophies": 0
                                    },
                                    "level": 1,
                                    "xp": 0,
                                    "teamwork_xp": 0,
                                    "class_mastery_xp": 0,
                                    "class_mastery_title": "Novice",
                                    "attribute_mastery_xp": {},
                                    "attribute_mastery_titles": {},
                                    "counterance_xp": {},
                                    "battle_tokens": {str(guild.id): 3},
                                    "race_effects": {"effects": [], "power_index": 0},
                                    "race_color": "#FFD700"
                                }
                                for field in embed.fields:
                                    if field.name == "Class":
                                        profile["class"] = field.value if field.value != "None" else None
                                    elif field.name == "Attributes":
                                        profile["attributes"] = field.value.split(", ") if field.value != "None" else []
                                    elif field.name == "Race":
                                        profile["race"] = field.value if field.value != "None" else None
                                    elif field.name == "Level":
                                        profile["level"] = int(field.value)
                                    elif field.name == "Wins (Players/Bots)":
                                        wins, bots_beaten = map(int, field.value.split("/"))
                                        profile["stats"]["wins"] = wins
                                        profile["stats"]["bots_beaten"] = bots_beaten
                                    elif field.name == "Losses (Players/Bots)":
                                        losses, losses_to_bots = map(int, field.value.split("/"))
                                        profile["stats"]["losses"] = losses
                                        profile["stats"]["losses_to_bots"] = losses_to_bots
                                    elif field.name == "Total Battles":
                                        profile["stats"]["total_battles"] = int(field.value)
                                    elif field.name == "Damage Dealt":
                                        profile["stats"]["total_damage_dealt"] = int(field.value)
                                    elif field.name == "Damage Taken":
                                        profile["stats"]["total_damage_taken"] = int(field.value)
                                    elif field.name == "Critical Hits":
                                        profile["stats"]["critical_hits"] = int(field.value)
                                    elif field.name == "Trophies (Monthly/Quarterly)":
                                        monthly, quarterly = map(int, field.value.split("/"))
                                        profile["stats"]["monthly_trophies"] = monthly
                                        profile["stats"]["quarterly_trophies"] = quarterly
                                    elif field.name == "Battle Tokens":
                                        profile["battle_tokens"][str(guild.id)] = int(field.value)
                                    elif field.name == "XP":
                                        profile["xp"] = int(field.value)
                                    elif field.name == "Teamwork XP":
                                        profile["teamwork_xp"] = int(field.value)
                                    elif field.name.endswith("Mastery"):
                                        type_name = field.name.split(" Mastery")[0]
                                        title, xp = field.value.split(" (")
                                        xp = int(xp.split(" XP")[0])
                                        if type_name == profile["class"]:
                                            profile["class_mastery_xp"] = xp
                                            profile["class_mastery_title"] = title
                                        else:
                                            profile["attribute_mastery_xp"][type_name] = xp
                                            profile["attribute_mastery_titles"][type_name] = title
                                bot.global_player_profiles[user.id] = profile
                                bot.stats_message_ids.setdefault(guild.id, {})[user.id] = message.id
                                print(f"Restored profile for {user.display_name} (ID: {user.id}) from stats embed")
                            else:
                                await message.delete()
                                print(f"Deleted old stats embed for {user_name} (user not found)")
            except discord.Forbidden:
                print(f"Missing permissions to read messages in {stats_channel.name}")

        # Clear old selection messages
        class_channel = discord.utils.get(guild.text_channels, name=CHANNEL_CONFIGS["class_channel"].lstrip('#'))
        if class_channel:
            try:
                async for message in class_channel.history(limit=100):
                    if message.author == bot.user and any(x in message.content for x in ["Class Selection", "Attribute Selection", "Race Selection"]):
                        await message.delete()
                        print(f"Deleted old selection message '{message.content}' in {guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to delete messages in {class_channel.name}")

        # Send new selection embeds
        if class_channel:
            # Class Selection Embed
            class_embed = discord.Embed(title="Class Selection", description="Choose your class by reacting to this message!", color=discord.Color.gold())
            for class_name, stats in CLASS_STATS.items():
                if class_name != "Omega Fury":  # Exclude Omega Fury for players
                    class_embed.add_field(name=f"{stats['emoji']} {class_name}", value=f"{stats['description']}\nHP: {stats['hp']}, Attack: {stats['attack']}, Defense: {stats['defense']}, Speed: {stats['speed']}", inline=True)
            class_message = await class_channel.send(embed=class_embed)
            bot.class_selection_message[guild.id] = class_message.id
            print(f"Sent Class Selection embed to {class_channel.name} (Message ID: {class_message.id})")
            for class_name, stats in CLASS_STATS.items():
                if class_name != "Omega Fury":
                    try:
                        await class_message.add_reaction(stats['emoji'])
                        print(f"Added reaction {stats['emoji']} to Class Selection")
                    except discord.Forbidden:
                        print(f"Missing permissions to add reaction {stats['emoji']} to Class Selection message")

            # Attribute Selection Embed
            attr_embed = discord.Embed(title="Attribute Selection", description="Choose your attributes (up to 3) by reacting to this message!", color=discord.Color.blue())
            for attr in PRIMARY_ATTRIBUTES:
                emoji = attribute_emojis.get(attr, "❓")
                description = ATTRIBUTE_DESCRIPTIONS.get(attr, "No description available.")
                attr_embed.add_field(name=f"{emoji} {attr}", value=description, inline=True)
            attr_message = await class_channel.send(embed=attr_embed)
            bot.attribute_selection_message[guild.id] = attr_message.id
            print(f"Sent Attribute Selection embed to {class_channel.name} (Message ID: {attr_message.id})")
            for attr in PRIMARY_ATTRIBUTES:
                emoji = attribute_emojis.get(attr, "❓")
                try:
                    await attr_message.add_reaction(emoji)
                    print(f"Added reaction {emoji} to Attribute Selection")
                except discord.Forbidden:
                    print(f"Missing permissions to add reaction {emoji} to Attribute Selection message")

            # Race Selection Embed
            race_embed = discord.Embed(title="Race Selection", description="Set your race using `/enter_race name:<race_name> color:<color>` to define your unique race and role color!", color=discord.Color.green())
            race_message = await class_channel.send(embed=race_embed)
            bot.race_selection_message[guild.id] = race_message.id
            print(f"Sent Race Selection embed to {class_channel.name} (Message ID: {race_message.id})")

    end_time = datetime.now(pytz.UTC)
    print(f"Finished on_ready for {bot.bot_name} at {end_time}")

    # Initialize bot profiles in a background task
    bot.loop.create_task(initialize_bot_profiles(bot))

    # Start daily quest updates
    bot.loop.create_task(update_daily_quests(bot))

async def initialize_bot_profiles(bot):
    print("Initializing bot profiles...")
    for guild in bot.guilds:
        print(f"Initializing bot profiles for {guild.name}...")
        bot_members = [member for member in guild.members if member.bot and member.id not in bot.global_player_profiles]
        batch_size = 2  # Process 2 bots at a time
        for i in range(0, len(bot_members), batch_size):
            batch = bot_members[i:i + batch_size]
            for member in batch:
                print(f"Assigning profile to bot {member.name}")
                if member.id == bot.user.id:  # FeatherFury
                    class_type = "Omega Fury"
                    attributes = PRIMARY_ATTRIBUTES.copy()
                    race = "Omega Race"
                    race_color = "#FF0000"  # Red for Omega Race
                    race_effects = {
                        "effects": [
                            {"name": "Omega Power", "value": "+50% damage to all attributes", "type": "normal"},
                            {"name": "Omega Strength", "value": "+20 to all stats", "type": "normal"}
                        ],
                        "power_index": 50
                    }
                    bot.global_player_profiles[member.id] = {
                        "class": class_type,
                        "attributes": attributes,
                        "race": race,
                        "stats": {
                            "wins": 0,
                            "losses": 0,
                            "total_battles": 0,
                            "total_damage_dealt": 0,
                            "total_damage_taken": 0,
                            "critical_hits": 0,
                            "critical_wins": 0,
                            "bots_beaten": 0,
                            "losses_to_bots": 0,
                            "monthly_trophies": 0,
                            "quarterly_trophies": 0
                        },
                        "level": 100,
                        "xp": 10000,
                        "teamwork_xp": 5000,
                        "class_mastery_xp": 2000,
                        "class_mastery_title": "Grand Master",
                        "attribute_mastery_xp": {attr: 2000 for attr in attributes},
                        "attribute_mastery_titles": {attr: "Grand Master" for attr in attributes},
                        "counterance_xp": {},
                        "battle_tokens": {str(guild.id): 20},
                        "race_effects": race_effects,
                        "race_color": race_color,
                        "is_bot": True,
                        "has_been_beaten": {}
                    }
                else:
                    class_type = random.choice([c for c in CLASS_STATS.keys() if c != "Omega Fury"])
                    attributes = random.sample(PRIMARY_ATTRIBUTES, min(3, len(PRIMARY_ATTRIBUTES)))
                    race = f"BotRace_{member.id % 1000}"
                    race_color = random.choice(["red", "green", "blue", "#FF0000", "#00FF00", "#0000FF"])
                    race_effects = await generate_race_effects(race, race_color, class_type=class_type, attributes=attributes, is_bot=True)
                    bot.global_player_profiles[member.id] = {
                        "class": class_type,
                        "attributes": attributes,
                        "race": race,
                        "stats": {
                            "wins": 0,
                            "losses": 0,
                            "total_battles": 0,
                            "total_damage_dealt": 0,
                            "total_damage_taken": 0,
                            "critical_hits": 0,
                            "critical_wins": 0,
                            "bots_beaten": 0,
                            "losses_to_bots": 0,
                            "monthly_trophies": 0,
                            "quarterly_trophies": 0
                        },
                        "level": 1,
                        "xp": 0,
                        "teamwork_xp": 0,
                        "class_mastery_xp": 0,
                        "class_mastery_title": "Novice",
                        "attribute_mastery_xp": {attr: 0 for attr in attributes},
                        "attribute_mastery_titles": {attr: "Novice" for attr in attributes},
                        "counterance_xp": {},
                        "battle_tokens": {str(guild.id): 3},
                        "race_effects": race_effects,
                        "race_color": race_color,
                        "is_bot": True
                    }
                # Assign class role
                class_role = discord.utils.get(guild.roles, name=class_type)
                if not class_role:
                    try:
                        class_role = await guild.create_role(name=class_type)
                        print(f"Created class role {class_type} in {guild.name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to create class role {class_type} in {guild.name}")
                        continue
                if class_role:
                    try:
                        await member.add_roles(class_role)
                        print(f"Assigned class role {class_type} to bot {member.name}")
                    except discord.Forbidden:
                        print(f"Failed to assign class role {class_type} to bot {member.name} - missing permissions")
                        continue

                # Assign attribute roles
                for attr in attributes:
                    attr_role = discord.utils.get(guild.roles, name=attr)
                    if not attr_role:
                        try:
                            attr_role = await guild.create_role(name=attr)
                            print(f"Created attribute role {attr} in {guild.name}")
                        except discord.Forbidden:
                            print(f"Missing permissions to create attribute role {attr} in {guild.name}")
                            continue
                    if attr_role:
                        try:
                            await member.add_roles(attr_role)
                            print(f"Assigned attribute role {attr} to bot {member.name}")
                        except discord.Forbidden:
                            print(f"Failed to assign attribute role {attr} to bot {member.name} - missing permissions")
                            continue

                # Assign race role with color
                race_role = discord.utils.get(guild.roles, name=race)
                if not race_role:
                    try:
                        hex_color = race_color
                        if not race_color.startswith("#"):
                            color_map = {
                                "red": "#FF0000",
                                "green": "#00FF00",
                                "blue": "#0000FF",
                                "white": "#FFFFFF",
                                "black": "#000000",
                                "yellow": "#FFFF00",
                                "purple": "#800080",
                                "orange": "#FFA500",
                                "pink": "#FFC0CB",
                                "cyan": "#00FFFF"
                            }
                            hex_color = color_map.get(race_color.lower(), "#FFFFFF")
                            if len(race_color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in race_color):
                                hex_color = f"#{race_color}"
                        race_role = await guild.create_role(name=race, color=discord.Color.from_str(hex_color))
                        print(f"Created race role {race} with color {hex_color} in {guild.name}")
                    except (discord.Forbidden, ValueError) as e:
                        print(f"Failed to create race role {race} for bot {member.name}: {e}")
                        continue
                if race_role:
                    try:
                        await member.add_roles(race_role)
                        print(f"Assigned race role {race} to bot {member.name}")
                    except discord.Forbidden:
                        print(f"Failed to assign race role {race} to bot {member.name} - missing permissions")
                        continue

                print(f"Assigned {class_type} with attributes {attributes}, race {race} to bot {member.name}")
                try:
                    await update_stats_embed(bot, guild, member.id)
                except Exception as e:
                    print(f"Failed to update stats embed for bot {member.name}: {e}")
            # Add a delay between batches to prevent overloading the event loop
            await asyncio.sleep(1.0)

async def on_message(bot, message: discord.Message):
    print(f"on_message event triggered for message {message.id}")
    if message.author == bot.user:
        return
    # Add message handling logic if needed

async def on_reaction_add(bot, reaction: discord.Reaction, user: discord.User):
    emoji_name = reaction.emoji.name if isinstance(reaction.emoji, discord.Emoji) else str(reaction.emoji)
    print(f"Reaction received: {user.name} reacted with {emoji_name} on message {reaction.message.id} in channel {reaction.message.channel.name}")

    # Map Unicode emojis to their attribute names
    attribute_emoji_mapping = {
        "🔥": "Fire",
        "💧": "Water",
        "❄️": "Ice",
        "⚡": "Electric",
        "🌍": "Earth",
        "🌿": "Nature",
        "🔩": "Metal",
        "💨": "Air",
        "✨": "Light",
        "🌑": "Shadow",
        "💖": "Life",
        "💀": "Death"
    }

    # Define class_emojis at the top to be accessible everywhere
    class_emojis = {stats['emoji']: class_name for class_name, stats in CLASS_STATS.items() if class_name != "Omega Fury"}

    # Handle class and attribute reactions
    if reaction.message.channel.name != CHANNEL_CONFIGS["class_channel"].lstrip('#'):
        print(f"Reaction ignored: channel {reaction.message.channel.name} does not match class channel {CHANNEL_CONFIGS['class_channel']}")
        return
    if user.bot:
        print(f"Reaction ignored: user.bot={user.bot}, channel={reaction.message.channel.name}")
        return
    guild = reaction.message.guild
    if not guild:
        print(f"No guild found for reaction message {reaction.message.id}")
        return

    # Check bot permissions
    bot_member = guild.get_member(bot.user.id)
    if not bot_member:
        print(f"Bot not found in guild {guild.name} (ID: {guild.id})")
        return
    bot_permissions = bot_member.guild_permissions
    if not bot_permissions.manage_roles:
        print(f"Bot lacks 'Manage Roles' permission in guild {guild.name} (ID: {guild.id})")
        await reaction.message.channel.send("I lack the 'Manage Roles' permission to assign roles. Please grant this permission to my role.")
        return

    print(f"User {user.name} reacted with {emoji_name} on message {reaction.message.id}")
    print(f"Class selection message ID: {bot.class_selection_message.get(guild.id)}")
    print(f"Attribute selection message ID: {bot.attribute_selection_message.get(guild.id)}")

    if reaction.message.id == bot.class_selection_message.get(guild.id):
        if emoji_name not in class_emojis:
            print(f"Invalid class emoji {emoji_name}, ignoring")
            return
        print(f"Class reaction detected: {emoji_name}")
        bot.global_player_profiles[user.id] = bot.global_player_profiles.get(user.id, {})
        bot.global_player_profiles[user.id]["class"] = class_emojis[emoji_name]
        bot.global_player_profiles[user.id]["attributes"] = bot.global_player_profiles[user.id].get("attributes", [])
        bot.global_player_profiles[user.id]["race"] = bot.global_player_profiles[user.id].get("race", None)
        bot.global_player_profiles[user.id]["stats"] = bot.global_player_profiles[user.id].get("stats", {
            "wins": 0,
            "losses": 0,
            "total_battles": 0,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "critical_hits": 0,
            "critical_wins": 0,
            "bots_beaten": 0,
            "losses_to_bots": 0,
            "monthly_trophies": 0,
            "quarterly_trophies": 0
        })
        bot.global_player_profiles[user.id]["level"] = bot.global_player_profiles[user.id].get("level", 1)
        bot.global_player_profiles[user.id]["xp"] = bot.global_player_profiles[user.id].get("xp", 0)
        bot.global_player_profiles[user.id]["teamwork_xp"] = bot.global_player_profiles[user.id].get("teamwork_xp", 0)
        bot.global_player_profiles[user.id]["class_mastery_xp"] = bot.global_player_profiles[user.id].get("class_mastery_xp", 0)
        bot.global_player_profiles[user.id]["class_mastery_title"] = bot.global_player_profiles[user.id].get("class_mastery_title", "Novice")
        bot.global_player_profiles[user.id]["attribute_mastery_xp"] = bot.global_player_profiles[user.id].get("attribute_mastery_xp", {})
        bot.global_player_profiles[user.id]["attribute_mastery_titles"] = bot.global_player_profiles[user.id].get("attribute_mastery_titles", {})
        bot.global_player_profiles[user.id]["counterance_xp"] = bot.global_player_profiles[user.id].get("counterance_xp", {})
        bot.global_player_profiles[user.id]["battle_tokens"] = bot.global_player_profiles[user.id].get("battle_tokens", {str(guild.id): 3})
        print(f"Assigned class {class_emojis[emoji_name]} to user {user.name} (ID: {user.id})")
        print(f"Current profile for {user.name}: {bot.global_player_profiles[user.id]}")

        # Assign class role
        class_role = discord.utils.get(guild.roles, name=class_emojis[emoji_name])
        if not class_role:
            try:
                class_role = await guild.create_role(name=class_emojis[emoji_name])
                print(f"Created class role {class_emojis[emoji_name]} in {guild.name}")
            except discord.Forbidden as e:
                print(f"Missing permissions to create class role {class_emojis[emoji_name]} in {guild.name}: {e}")
                await reaction.message.channel.send(f"Failed to create role {class_emojis[emoji_name]} due to missing permissions!")
                return
        if class_role:
            try:
                await user.add_roles(class_role)
                print(f"Assigned class role {class_emojis[emoji_name]} to {user.name}")
            except discord.Forbidden as e:
                print(f"Failed to assign class role {class_emojis[emoji_name]} to {user.name} - missing permissions: {e}")
                await reaction.message.channel.send(f"Failed to assign role {class_emojis[emoji_name]} due to missing permissions!")
                return

        announcement = random.choice(CLASS_ANNOUNCEMENTS[class_emojis[emoji_name]])
        flair = random.choice(FLAIR)
        confirmation = await reaction.message.channel.send(f"{announcement.format(player=user.mention, class_name=class_emojis[emoji_name])} {flair}")
        print(f"Sent class announcement for {user.name}: {announcement.format(player=user.mention, class_name=class_emojis[emoji_name])} {flair}")
        await asyncio.sleep(10)
        await confirmation.delete()
        print(f"Deleted class announcement for {user.name}")
        await update_stats_embed(bot, guild, user.id)
        print(f"User {user.name} now has class: {bot.global_player_profiles[user.id]['class']}")
    elif reaction.message.id == bot.attribute_selection_message.get(guild.id):
        if emoji_name not in attribute_emoji_mapping:
            print(f"Unknown attribute reaction {emoji_name}, ignoring")
            return
        attr = attribute_emoji_mapping[emoji_name]
        print(f"Attribute reaction detected: {emoji_name} (mapped to {attr})")

        if user.id not in bot.global_player_profiles:
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
                    "losses_to_bots": 0,
                    "monthly_trophies": 0,
                    "quarterly_trophies": 0
                },
                "level": 1,
                "xp": 0,
                "teamwork_xp": 0,
                "class_mastery_xp": 0,
                "class_mastery_title": "Novice",
                "attribute_mastery_xp": {},
                "attribute_mastery_titles": {},
                "counterance_xp": {},
                "battle_tokens": {str(guild.id): 3}
            }
        current_attributes = bot.global_player_profiles[user.id]["attributes"]
        print(f"Current attributes for {user.name}: {current_attributes}")
        if len(current_attributes) >= 3:
            confirmation = await reaction.message.channel.send(f"{user.mention}, you can only select up to 3 attributes!")
            await asyncio.sleep(10)
            await confirmation.delete()
            try:
                await reaction.message.clear_reaction(emoji_name)
            except discord.Forbidden:
                print(f"Failed to clear reaction {emoji_name} - missing permissions")
            return
        if attr not in current_attributes:
            current_attributes.append(attr)
            bot.global_player_profiles[user.id]["attributes"] = current_attributes
            bot.global_player_profiles[user.id]["attribute_mastery_xp"][attr] = 0
            bot.global_player_profiles[user.id]["attribute_mastery_titles"][attr] = "Novice"
            print(f"Updated attributes for {user.name}: {current_attributes}")
            attr_role = discord.utils.get(guild.roles, name=attr)
            if not attr_role:
                try:
                    attr_role = await guild.create_role(name=attr)
                    print(f"Created attribute role {attr} in {guild.name}")
                except discord.Forbidden as e:
                    print(f"Missing permissions to create attribute role {attr} in {guild.name}: {e}")
                    await reaction.message.channel.send(f"Failed to create role {attr} due to missing permissions!")
                    return
            if attr_role:
                try:
                    await user.add_roles(attr_role)
                    print(f"Assigned attribute role {attr} to {user.name}")
                except discord.Forbidden as e:
                    print(f"Failed to assign attribute role {attr} to {user.name} - missing permissions: {e}")
                    await reaction.message.channel.send(f"Failed to assign role {attr} due to missing permissions!")
                    return
            announcement = random.choice(ATTRIBUTE_ANNOUNCEMENTS[attr])
            flair = random.choice(FLAIR)
            confirmation = await reaction.message.channel.send(f"{announcement.format(player=user.mention, attribute=attr)} {flair}")
            print(f"Sent attribute announcement for {user.name}: {announcement.format(player=user.mention, attribute=attr)} {flair}")
            await asyncio.sleep(10)
            await confirmation.delete()
            print(f"Deleted attribute announcement for {user.name}")
            await update_stats_embed(bot, guild, user.id)
            print(f"Updated stats embed for {user.name} after adding attribute {attr}")
            try:
                await reaction.message.remove_reaction(reaction.emoji, user)
            except discord.Forbidden:
                print(f"Failed to remove attribute reaction {emoji_name} - missing permissions")
            print(f"User {user.name} now has attributes: {bot.global_player_profiles[user.id]['attributes']}")
        else:
            confirmation = await reaction.message.channel.send(f"{user.mention}, you already have the {attr} attribute!")
            await asyncio.sleep(10)
            await confirmation.delete()
            try:
                await reaction.message.remove_reaction(reaction.emoji, user)
            except discord.Forbidden:
                print(f"Failed to remove duplicate attribute reaction - missing permissions")

async def update_stats_embed(bot, guild, user_id, embed=None, interaction=None):
    member = guild.get_member(user_id)
    if not member:
        print(f"Member {user_id} not found in guild {guild.name}")
        if interaction:
            await interaction.followup.send(f"Member with ID {user_id} not found in the server!")
        return
    profile = bot.global_player_profiles.get(user_id, {})
    if not profile:
        print(f"Profile for user {user_id} not found")
        if interaction:
            await interaction.followup.send(f"Profile for user with ID {user_id} not found!")
        return
    print(f"Profile for {member.display_name} (ID: {user_id}): {profile}")
    channel = discord.utils.get(guild.text_channels, name=CHANNEL_CONFIGS["stats_channel"].lstrip('#'))
    if not channel:
        print(f"Stats channel not found in guild {guild.name}")
        if interaction:
            await interaction.followup.send(f"Stats channel not found in the server!")
        return

    # Calculate leaderboard stats (exclude bots)
    all_profiles = [p for uid, p in bot.global_player_profiles.items() if guild.get_member(uid) and not p.get("is_bot", False)]
    if not all_profiles:
        # If no player profiles, set default values to avoid errors
        highest_stats = {stat_name: 0 for stat_name, _ in [
            ("Wins (Players)", lambda p: p["stats"]["wins"]),
            ("Wins (Bots)", lambda p: p["stats"]["bots_beaten"]),
            ("Total Battles", lambda p: p["stats"]["total_battles"]),
            ("Damage Dealt", lambda p: p["stats"]["total_damage_dealt"]),
            ("Damage Taken", lambda p: p["stats"]["total_damage_taken"]),
            ("Critical Hits", lambda p: p["stats"]["critical_hits"]),
            ("Monthly Trophies", lambda p: p["stats"]["monthly_trophies"]),
            ("Quarterly Trophies", lambda p: p["stats"]["quarterly_trophies"]),
            ("XP", lambda p: p["xp"]),
            ("Teamwork XP", lambda p: p["teamwork_xp"])
        ]}
        lowest_stats = highest_stats.copy()
    else:
        stats_to_compare = [
            ("Wins (Players)", lambda p: p["stats"]["wins"]),
            ("Wins (Bots)", lambda p: p["stats"]["bots_beaten"]),
            ("Total Battles", lambda p: p["stats"]["total_battles"]),
            ("Damage Dealt", lambda p: p["stats"]["total_damage_dealt"]),
            ("Damage Taken", lambda p: p["stats"]["total_damage_taken"]),
            ("Critical Hits", lambda p: p["stats"]["critical_hits"]),
            ("Monthly Trophies", lambda p: p["stats"]["monthly_trophies"]),
            ("Quarterly Trophies", lambda p: p["stats"]["quarterly_trophies"]),
            ("XP", lambda p: p["xp"]),
            ("Teamwork XP", lambda p: p["teamwork_xp"])
        ]
        highest_stats = {}
        lowest_stats = {}
        for stat_name, stat_func in stats_to_compare:
            sorted_profiles = sorted(all_profiles, key=stat_func, reverse=True)
            highest_stats[stat_name] = stat_func(sorted_profiles[0])
            lowest_stats[stat_name] = stat_func(sorted_profiles[-1])

    # Create or update the embed
    race_effects = profile.get("race_effects", {}).get("effects", [])
    race_effects_display = "\n".join([
        f"{effect['name']}: {effect['value']}" + 
        (f" (Weakness: {effect['weakness']}, Strength: {effect['strength']})" if effect.get("type") == "dual" else "")
        for effect in race_effects
    ]) or "None"
    race_color = profile.get("race_color", "#FFD700")
    try:
        embed_color = discord.Color.from_str(race_color)
    except ValueError:
        embed_color = discord.Color.gold()
    embed = discord.Embed(title=f"{member.display_name}'s Stats", color=embed_color)
    embed.add_field(name="Class", value=profile.get("class", "None"), inline=True)
    embed.add_field(name="Attributes", value=", ".join(profile.get("attributes", [])) if profile.get("attributes") else "None", inline=True)
    embed.add_field(name="Race", value=profile.get("race", "None"), inline=True)
    embed.add_field(name="Race Effects", value=race_effects_display, inline=False)
    embed.add_field(name="Level", value=profile.get("level", 1), inline=True)
    wins = profile.get("stats", {}).get("wins", 0)
    wins_display = f"{wins} {'👑' if wins == highest_stats['Wins (Players)'] and not profile.get('is_bot', False) else '😢' if wins == lowest_stats['Wins (Players)'] and not profile.get('is_bot', False) else ''}"
    bots_beaten = profile.get("stats", {}).get("bots_beaten", 0)
    bots_beaten_display = f"{bots_beaten} {'👑' if bots_beaten == highest_stats['Wins (Bots)'] and not profile.get('is_bot', False) else '😢' if bots_beaten == lowest_stats['Wins (Bots)'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Wins (Players/Bots)", value=f"{wins_display}/{bots_beaten_display}", inline=True)
    total_battles = profile.get("stats", {}).get("total_battles", 0)
    total_battles_display = f"{total_battles} {'👑' if total_battles == highest_stats['Total Battles'] and not profile.get('is_bot', False) else '😢' if total_battles == lowest_stats['Total Battles'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Total Battles", value=total_battles_display, inline=True)
    damage_dealt = profile.get("stats", {}).get("total_damage_dealt", 0)
    damage_dealt_display = f"{damage_dealt} {'👑' if damage_dealt == highest_stats['Damage Dealt'] and not profile.get('is_bot', False) else '😢' if damage_dealt == lowest_stats['Damage Dealt'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Damage Dealt", value=damage_dealt_display, inline=True)
    damage_taken = profile.get("stats", {}).get("total_damage_taken", 0)
    damage_taken_display = f"{damage_taken} {'👑' if damage_taken == highest_stats['Damage Taken'] and not profile.get('is_bot', False) else '😢' if damage_taken == lowest_stats['Damage Taken'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Damage Taken", value=damage_taken_display, inline=True)
    critical_hits = profile.get("stats", {}).get("critical_hits", 0)
    critical_hits_display = f"{critical_hits} {'👑' if critical_hits == highest_stats['Critical Hits'] and not profile.get('is_bot', False) else '😢' if critical_hits == lowest_stats['Critical Hits'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Critical Hits", value=critical_hits_display, inline=True)
    monthly_trophies = profile.get("stats", {}).get("monthly_trophies", 0)
    quarterly_trophies = profile.get("stats", {}).get("quarterly_trophies", 0)
    monthly_trophies_display = f"{monthly_trophies} {'👑' if monthly_trophies == highest_stats['Monthly Trophies'] and not profile.get('is_bot', False) else '😢' if monthly_trophies == lowest_stats['Monthly Trophies'] and not profile.get('is_bot', False) else ''}"
    quarterly_trophies_display = f"{quarterly_trophies} {'👑' if quarterly_trophies == highest_stats['Quarterly Trophies'] and not profile.get('is_bot', False) else '😢' if quarterly_trophies == lowest_stats['Quarterly Trophies'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Trophies (Monthly/Quarterly)", value=f"{monthly_trophies_display}/{quarterly_trophies_display}", inline=True)
    battle_tokens = profile.get("battle_tokens", {}).get(str(guild.id), 3)
    embed.add_field(name="Battle Tokens", value=battle_tokens, inline=True)
    xp = profile.get("xp", 0)
    xp_display = f"{xp} {'👑' if xp == highest_stats['XP'] and not profile.get('is_bot', False) else '😢' if xp == lowest_stats['XP'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="XP", value=xp_display, inline=True)
    teamwork_xp = profile.get("teamwork_xp", 0)
    teamwork_xp_display = f"{teamwork_xp} {'👑' if teamwork_xp == highest_stats['Teamwork XP'] and not profile.get('is_bot', False) else '😢' if teamwork_xp == lowest_stats['Teamwork XP'] and not profile.get('is_bot', False) else ''}"
    embed.add_field(name="Teamwork XP", value=teamwork_xp_display, inline=True)
    class_mastery = f"{profile.get('class_mastery_title', 'Novice')} ({profile.get('class_mastery_xp', 0)} XP)"
    embed.add_field(name=f"{profile.get('class', 'None')} Mastery", value=class_mastery, inline=True)
    # Consolidate attribute mastery fields for bots with many attributes
    if profile.get("is_bot", False) and len(profile.get("attributes", [])) > 5:
        attr_mastery_display = "\n".join([
            f"{attr}: {profile.get('attribute_mastery_titles', {}).get(attr, 'Novice')} ({profile.get('attribute_mastery_xp', {}).get(attr, 0)} XP)"
            for attr in profile.get("attributes", [])
        ])
        embed.add_field(name="Attribute Mastery", value=attr_mastery_display or "None", inline=False)
    else:
        for attr in profile.get("attributes", []):
            attr_mastery = f"{profile.get('attribute_mastery_titles', {}).get(attr, 'Novice')} ({profile.get('attribute_mastery_xp', {}).get(attr, 0)} XP)"
            embed.add_field(name=f"{attr} Mastery", value=attr_mastery, inline=True)

    # Send the embed to the user if called from a command
    if interaction:
        await interaction.followup.send(embed=embed)

    # Always update the stats channel
    if user_id in bot.stats_message_ids.get(guild.id, {}):
        try:
            message = await channel.fetch_message(bot.stats_message_ids[guild.id][user_id])
            await message.delete()
            print(f"Deleted old stats embed for {member.display_name} (ID: {user_id})")
        except discord.NotFound:
            print(f"Old stats embed for {member.display_name} (ID: {user_id}) not found")
        except discord.Forbidden:
            print(f"Missing permissions to delete stats embed for {member.display_name}")

    message = await channel.send(embed=embed)
    bot.stats_message_ids.setdefault(guild.id, {})[user_id] = message.id
    print(f"Created new stats embed for {member.display_name} (ID: {user_id}, Message ID: {message.id})")

async def update_daily_quests(bot):
    while True:
        now = datetime.now(pytz.UTC)
        # Schedule for midnight UTC
        next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        seconds_until_midnight = (next_midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)

        for guild in bot.guilds:
            quest_channel = discord.utils.get(guild.text_channels, name=CHANNEL_CONFIGS["quest_channel"].lstrip('#'))
            if not quest_channel:
                try:
                    quest_channel = await guild.create_text_channel(CHANNEL_CONFIGS["quest_channel"].lstrip('#'))
                    print(f"Created quest channel {CHANNEL_CONFIGS['quest_channel']} in {guild.name}")
                except discord.Forbidden:
                    print(f"Missing permissions to create quest channel in {guild.name}")
                    continue

            # Clear old quest messages
            try:
                async for message in quest_channel.history(limit=100):
                    if message.author == bot.user:
                        await message.delete()
                        print(f"Deleted old quest message in {guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to delete messages in {quest_channel.name}")

            # Generate new quests
            from data.quests import generate_daily_quests
            quests = generate_daily_quests()
            embed = discord.Embed(title="Daily Quests", description="Complete these quests to earn Mastery XP! Quests reset daily at midnight UTC.", color=discord.Color.orange())
            for quest_type, quest in quests.items():
                embed.add_field(name=quest_type, value=quest["description"], inline=False)
            await quest_channel.send(embed=embed)
            print(f"Posted daily quests in {guild.name}")
