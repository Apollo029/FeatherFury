# core/events.py
import discord
import random
from datetime import datetime
import pytz
import asyncio
from data.classes import CLASS_STATS, CLASS_ANNOUNCEMENTS
from data.attributes import ATTRIBUTE_ANNOUNCEMENTS, PRIMARY_ATTRIBUTES, attribute_emojis, FLAIR
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
                class_embed.add_field(name=f"{stats['emoji']} {class_name}", value=f"{stats['description']}\nHP: {stats['hp']}, Attack: {stats['attack']}, Defense: {stats['defense']}, Speed: {stats['speed']}", inline=True)
            class_message = await class_channel.send(embed=class_embed)
            bot.class_selection_message[guild.id] = class_message.id
            print(f"Sent Class Selection embed to {class_channel.name} (Message ID: {class_message.id})")
            for class_name, stats in CLASS_STATS.items():
                try:
                    await class_message.add_reaction(stats['emoji'])
                    print(f"Added reaction {stats['emoji']} to Class Selection")
                except discord.Forbidden:
                    print(f"Missing permissions to add reaction {stats['emoji']} to Class Selection message")

            # Attribute Selection Embed
            attr_embed = discord.Embed(title="Attribute Selection", description="Choose your attributes (up to 3) by reacting to this message!", color=discord.Color.blue())
            for attr in PRIMARY_ATTRIBUTES:
                emoji = attribute_emojis.get(attr, "❓")
                attr_embed.add_field(name=f"{emoji} {attr}", value=f"Attribute: {attr}", inline=True)
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
            race_embed = discord.Embed(title="Race Selection", description="Set your race using `/enter_race name:<your_race> color:<color>` (e.g., `/enter_race name:Arcturan color:0000FF`).\nYour race determines unique buffs and a custom role color!", color=discord.Color.green())
            race_message = await class_channel.send(embed=race_embed)
            bot.race_selection_message[guild.id] = race_message.id
            print(f"Sent Race Selection embed to {class_channel.name} (Message ID: {race_message.id})")

    end_time = datetime.now(pytz.UTC)
    print(f"Finished on_ready for {bot.bot_name} at {end_time}")

    # Setup scheduler for daily active role updates
    print("Setting up daily active role update scheduler")
    schedule.every().day.at("00:00").do(lambda: bot.loop.create_task(update_active_roles(bot)))
    bot.loop.create_task(run_scheduler())
    print("Scheduler started")

    # Initialize bot profiles in a background task
    bot.loop.create_task(initialize_bot_profiles(bot))

async def initialize_bot_profiles(bot):
    print("Initializing bot profiles...")
    for guild in bot.guilds:
        print(f"Initializing bot profiles for {guild.name}...")
        for member in guild.members:
            if member.bot and member.id not in bot.global_player_profiles:
                print(f"Assigning profile to bot {member.name}")
                class_type = random.choice(list(CLASS_STATS.keys()))
                attributes = random.sample(PRIMARY_ATTRIBUTES, min(3, len(PRIMARY_ATTRIBUTES)))
                race = f"BotRace_{member.id % 1000}"
                race_color = random.choice(["red", "green", "blue", "#FF0000", "#00FF00", "#0000FF"])
                race_effects = generate_race_effects(race, race_color, class_type=class_type, attributes=attributes)
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
                        "losses_to_bots": 0
                    },
                    "level": 1,
                    "xp": 0,
                    "race_effects": race_effects,
                    "race_color": race_color
                }
                # Assign class role
                class_role = discord.utils.get(guild.roles, name=class_type)
                if not class_role:
                    try:
                        class_role = await guild.create_role(name=class_type)
                        print(f"Created class role {class_type} in {guild.name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to create class role {class_type} in {guild.name}")
                if class_role and class_role not in member.roles:
                    try:
                        await member.add_roles(class_role)
                        print(f"Assigned class role {class_type} to bot {member.name}")
                    except discord.Forbidden:
                        print(f"Failed to assign class role {class_type} to bot {member.name} - missing permissions")

                # Assign attribute roles
                for attr in attributes:
                    attr_role = discord.utils.get(guild.roles, name=attr)
                    if not attr_role:
                        try:
                            attr_role = await guild.create_role(name=attr)
                            print(f"Created attribute role {attr} in {guild.name}")
                        except discord.Forbidden:
                            print(f"Missing permissions to create attribute role {attr} in {guild.name}")
                    if attr_role and attr_role not in member.roles:
                        try:
                            await member.add_roles(attr_role)
                            print(f"Assigned attribute role {attr} to bot {member.name}")
                        except discord.Forbidden:
                            print(f"Failed to assign attribute role {attr} to bot {member.name} - missing permissions")

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
                if race_role and race_role not in member.roles:
                    try:
                        await member.add_roles(race_role)
                        print(f"Assigned race role {race} to bot {member.name}")
                    except discord.Forbidden:
                        print(f"Failed to assign race role {race} to bot {member.name} - missing permissions")

                print(f"Assigned {class_type} with attributes {attributes}, race {race} to bot {member.name}")
                await update_stats_embed(bot, guild, member.id)

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
    class_emojis = {stats['emoji']: class_name for class_name, stats in CLASS_STATS.items()}

    # Handle class and attribute reactions
    if reaction.message.channel.name == CHANNEL_CONFIGS["class_channel"].lstrip('#'):
        if user.bot:
            print(f"Reaction ignored: user.bot={user.bot}, channel={reaction.message.channel.name}")
            return
        guild = reaction.message.guild

        print(f"User {user.name} reacted with {emoji_name} on message {reaction.message.id}")
        print(f"Checking class selection message ID: {bot.class_selection_message.get(guild.id)}")
        print(f"Checking attribute selection message ID: {bot.attribute_selection_message.get(guild.id)}")

        if reaction.message.id == bot.class_selection_message.get(guild.id):
            if emoji_name in class_emojis:
                print(f"Class reaction detected: {emoji_name}")
                # Allow overwriting existing profile
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
                    "losses_to_bots": 0
                })
                bot.global_player_profiles[user.id]["level"] = bot.global_player_profiles[user.id].get("level", 1)
                bot.global_player_profiles[user.id]["xp"] = bot.global_player_profiles[user.id].get("xp", 0)
                print(f"Assigned or updated class {class_emojis[emoji_name]} to user {user.name} (ID: {user.id})")

                new_role = discord.utils.get(guild.roles, name=class_emojis[emoji_name])
                if not new_role:
                    try:
                        new_role = await guild.create_role(name=class_emojis[emoji_name])
                        print(f"Created role {class_emojis[emoji_name]} in {guild.name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to create role {class_emojis[emoji_name]} in {guild.name}")
                if new_role and new_role not in user.roles:
                    try:
                        await user.add_roles(new_role)
                        print(f"Assigned new class role {class_emojis[emoji_name]} to {user.name}")
                    except discord.Forbidden:
                        print(f"Failed to assign role {class_emojis[emoji_name]} - missing permissions")
                else:
                    print(f"Failed to assign role {class_emojis[emoji_name]} - role not found or already assigned")
                # Use a random class announcement with flair
                announcement = random.choice(CLASS_ANNOUNCEMENTS[class_emojis[emoji_name]])
                flair = random.choice(FLAIR)
                confirmation = await reaction.message.channel.send(f"{announcement.format(player=user.mention, class_name=class_emojis[emoji_name])} {flair}")
                await asyncio.sleep(10)
                await confirmation.delete()
                # Update stats embed for this user
                await update_stats_embed(bot, guild, user.id)
                print(f"User {user.name} now has class: {bot.global_player_profiles[user.id]['class']}")
        elif reaction.message.id == bot.attribute_selection_message.get(guild.id):
            if emoji_name in attribute_emoji_mapping:
                attr = attribute_emoji_mapping[emoji_name]
            else:
                print(f"Unknown reaction {emoji_name}, ignoring")
                return

            print(f"Reaction {emoji_name} received for attribute selection by {user.name}")
            print(f"Attribute reaction detected: {emoji_name} (mapped to {attr})")
            print(f"Current attribute message ID for guild {guild.id}: {bot.attribute_selection_message.get(guild.id)}")
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
                        "losses_to_bots": 0
                    },
                    "level": 1,
                    "xp": 0
                }
            current_attributes = bot.global_player_profiles[user.id]["attributes"]
            print(f"Current attributes for {user.name}: {current_attributes}")
            if len(current_attributes) >= 3:
                print(f"User {user.name} already has 3 attributes, rejecting new attribute")
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
                new_role = discord.utils.get(guild.roles, name=attr)
                if not new_role:
                    try:
                        new_role = await guild.create_role(name=attr)
                        print(f"Created role {attr} in {guild.name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to create role {attr} in {guild.name}")
                if new_role and new_role not in user.roles:
                    try:
                        print(f"Assigning new attribute role {attr} to {user.name}")
                        await user.add_roles(new_role)
                    except discord.Forbidden:
                        print(f"Failed to assign role {attr} - missing permissions")
                else:
                    print(f"Failed to assign role {attr} - role not found or already assigned")
                # Use a random attribute announcement with flair
                announcement = random.choice(ATTRIBUTE_ANNOUNCEMENTS[attr])
                flair = random.choice(FLAIR)
                confirmation = await reaction.message.channel.send(f"{announcement.format(player=user.mention, attribute=attr)} {flair}")
                await asyncio.sleep(10)
                await confirmation.delete()
                # Update stats embed for this user
                await update_stats_embed(bot, guild, user.id)
                try:
                    print(f"Removing attribute reaction {emoji_name} from {user.name}")
                    await reaction.message.remove_reaction(reaction.emoji, user)
                except discord.Forbidden:
                    print(f"Failed to remove attribute reaction {emoji_name} - missing permissions")
                print(f"User {user.name} now has attributes: {bot.global_player_profiles[user.id]['attributes']}")
            else:
                print(f"User {user.name} already has attribute {attr}, rejecting duplicate")
                confirmation = await reaction.message.channel.send(f"{user.mention}, you already have the {attr} attribute!")
                await asyncio.sleep(10)
                await confirmation.delete()
                try:
                    await reaction.message.remove_reaction(reaction.emoji, user)
                except discord.Forbidden:
                    print(f"Failed to remove duplicate attribute reaction - missing permissions")

    # Handle battle reactions
    from battle.state import process_attack, get_random_attacks, NEUTRAL_ATTACKS, DEFENSE_OPTIONS, CLASS_ATTACKS_POOL, ATTRIBUTE_ATTACKS_POOL
    for battle_id, battle in bot.active_battles.items():
        if battle["message"] and reaction.message.id == battle["message"].id and user == battle["turn"] and not user.bot:
            current_player = battle["player1"] if user == battle["player1"].user else battle["player2"]
            opponent = battle["player2"] if user == battle["player1"].user else battle["player1"]
            attacks = get_random_attacks(current_player)

            # Create a new turn message with attack options, stats, and emojis
            attack_lines = []
            for i, attack in enumerate(attacks):
                emoji = None
                if attack["name"] in [a["name"] for a in NEUTRAL_ATTACKS]:
                    emoji = "⚔️"
                elif attack["name"] in [a["name"] for a in DEFENSE_OPTIONS]:
                    emoji = "🛡️"
                else:
                    class_attacks = CLASS_ATTACKS_POOL.get(current_player.class_type, [])
                    if attack["name"] in [a["name"] for a in class_attacks]:
                        emoji = class_emojis.get(current_player.class_type, "❓")
                    for attr, attr_attacks in ATTRIBUTE_ATTACKS_POOL.items():
                        if attack["name"] in [a["name"] for a in attr_attacks]:
                            emoji = next((e for e, a in attribute_emoji_mapping.items() if a == attr), "❓")
                            break
                stats = f"{attack['damage_range'][0]}-{attack['damage_range'][1]} damage" if "damage_range" in attack else "No damage"
                attack_lines.append(f"{emoji} {i+1}. {attack['name']} ({attack['effect']}) - {stats}")

            # Show battle progress (HP)
            progress = f"**Battle Progress**\n{current_player.user.mention}: {current_player.hp}/{current_player.max_hp} HP\n{opponent.user.mention}: {opponent.hp}/{opponent.max_hp} HP\n\n"
            new_message = await battle["thread"].send(f"{progress}{battle['turn'].mention}'s turn!\n" + "\n".join(attack_lines))

            # Clear old reactions and add new ones
            try:
                await battle["message"].clear_reactions()
            except discord.Forbidden:
                print(f"Failed to clear reactions on message {battle['message'].id} - missing permissions")
            for attack in attacks:
                if attack["name"] in [a["name"] for a in NEUTRAL_ATTACKS]:
                    emoji = "⚔️"
                elif attack["name"] in [a["name"] for a in DEFENSE_OPTIONS]:
                    emoji = "🛡️"
                else:
                    class_attacks = CLASS_ATTACKS_POOL.get(current_player.class_type, [])
                    if attack["name"] in [a["name"] for a in class_attacks]:
                        emoji = class_emojis.get(current_player.class_type, "❓")
                    for attr, attr_attacks in ATTRIBUTE_ATTACKS_POOL.items():
                        if attack["name"] in [a["name"] for a in attr_attacks]:
                            emoji = next((e for e, a in attribute_emoji_mapping.items() if a == attr), "❓")
                            break
                try:
                    await new_message.add_reaction(emoji)
                except discord.Forbidden:
                    print(f"Failed to add reaction {emoji} to message {new_message.id} - missing permissions")
            battle["message"] = new_message

            # Process the reaction
            if emoji_name in attribute_emoji_mapping.values():
                attr = next((a for a in attribute_emoji_mapping.values() if emoji_name in [e for e, v in attribute_emoji_mapping.items() if v == a]), None)
                if attr in current_player.attributes:
                    attack_name = next((a["name"] for a in attacks if a["name"].startswith(attr)), None)
                    if attack_name:
                        damage = process_attack(current_player, opponent, attack_name, battle["reinforce_buff"], attacks)
                        await battle["thread"].send(f"{user.mention} used {attack_name}! Dealt {damage} damage to {opponent.user.mention}.")
                        battle["last_action"] = attack_name
                else:
                    await battle["thread"].send(f"{user.mention}, invalid action! Use an attribute, ⚔️, or 🛡️.")
                    return
            elif emoji_name == "⚔️":
                attack_name = next((a["name"] for a in attacks if a["name"] in [na["name"] for na in NEUTRAL_ATTACKS]), None)
                if attack_name:
                    damage = process_attack(current_player, opponent, attack_name, battle["reinforce_buff"], attacks)
                    await battle["thread"].send(f"{user.mention} used {attack_name}! Dealt {damage} damage to {opponent.user.mention}.")
                    battle["last_action"] = attack_name
                else:
                    await battle["thread"].send(f"{user.mention}, invalid action! Use an attribute, ⚔️, or 🛡️.")
                    return
            elif emoji_name == "🛡️":
                defense_name = next((a["name"] for a in attacks if a["name"] in [d["name"] for d in DEFENSE_OPTIONS]), None)
                if defense_name:
                    await battle["thread"].send(f"{user.mention} used {defense_name}! No damage dealt this turn.")
                    battle["last_action"] = defense_name
                else:
                    await battle["thread"].send(f"{user.mention}, invalid action! Use an attribute, ⚔️, or 🛡️.")
                    return
            else:
                await battle["thread"].send(f"{user.mention}, invalid action! Use an attribute, ⚔️, or 🛡️.")
                return

            # Switch turn
            battle["turn"] = battle["player2"].user if user == battle["player1"].user else battle["player1"].user
            # Check for battle end
            if not battle["player1"].alive or not battle["player2"].alive:
                winner = battle["player1"] if battle["player2"].alive else battle["player2"]
                await battle["thread"].send(f"Battle ended! {winner.user.mention} wins!")
                battle["active"] = False
            try:
                await reaction.message.remove_reaction(emoji_name, user)
            except discord.Forbidden:
                print(f"Failed to remove reaction {emoji_name} - missing permissions")

async def update_active_roles(bot):
    print("Updating active roles...")
    for guild in bot.guilds:
        active_role = discord.utils.get(guild.roles, name="Active")
        if not active_role:
            try:
                active_role = await guild.create_role(name="Active", color=discord.Color.green())
                print(f"Created Active role in {guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to create Active role in {guild.name}")
                continue
        inactive_role = discord.utils.get(guild.roles, name="Inactive")
        if not inactive_role:
            try:
                inactive_role = await guild.create_role(name="Inactive", color=discord.Color.gray())
                print(f"Created Inactive role in {guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to create Inactive role in {guild.name}")
                continue
        for member in guild.members:
            if member.bot:
                continue
            last_message = max((m.created_at for m in member.history(limit=100) if not m.bot), default=None)
            if last_message and (datetime.now(pytz.UTC) - last_message).days < 7:
                if inactive_role in member.roles:
                    try:
                        await member.remove_roles(inactive_role)
                        print(f"Removed Inactive role from {member.display_name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to remove Inactive role from {member.display_name}")
                if active_role not in member.roles:
                    try:
                        await member.add_roles(active_role)
                        print(f"Added Active role to {member.display_name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to add Active role to {member.display_name}")
            else:
                if active_role in member.roles:
                    try:
                        await member.remove_roles(active_role)
                        print(f"Removed Active role from {member.display_name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to remove Active role from {member.display_name}")
                if inactive_role not in member.roles:
                    try:
                        await member.add_roles(inactive_role)
                        print(f"Added Inactive role to {member.display_name}")
                    except discord.Forbidden:
                        print(f"Missing permissions to add Inactive role to {member.display_name}")

async def update_stats_embed(bot, guild, user_id):
    member = guild.get_member(user_id)
    if not member:
        return
    profile = bot.global_player_profiles.get(user_id, {})
    if not profile:
        return
    channel = discord.utils.get(guild.text_channels, name=CHANNEL_CONFIGS["stats_channel"].lstrip('#'))
    if not channel:
        return
    # Format race effects with details
    race_effects = profile.get("race_effects", {}).get("effects", [])
    race_effects_display = "\n".join([f"{effect['name']}: {effect['value']}" + (f" (Weakness: {effect['weakness']}, Strength: {effect['strength']})" if effect.get("type") == "dual" else "") for effect in race_effects]) or "None"
    # Determine embed color based on race color (if available)
    race_color = profile.get("race_color", "#FFD700")  # Default to gold if no race color
    try:
        embed_color = discord.Color.from_str(race_color)
    except ValueError:
        embed_color = discord.Color.gold()  # Fallback to gold if invalid color
    embed = discord.Embed(title=f"{member.display_name}'s Stats", color=embed_color)
    embed.add_field(name="Class", value=profile.get("class", "None"), inline=True)
    embed.add_field(name="Attributes", value=", ".join(profile.get("attributes", [])) if profile.get("attributes") else "None", inline=True)
    embed.add_field(name="Race", value=profile.get("race", "None"), inline=True)
    embed.add_field(name="Race Effects", value=race_effects_display, inline=False)
    embed.add_field(name="Level", value=profile.get("level", 1), inline=True)
    embed.add_field(name="Wins/Losses", value=f"{profile.get('stats', {}).get('wins', 0)}/{profile.get('stats', {}).get('losses', 0)}", inline=True)
    embed.add_field(name="Total Battles", value=profile.get("stats", {}).get("total_battles", 0), inline=True)
    embed.add_field(name="Damage Dealt", value=profile.get("stats", {}).get("total_damage_dealt", 0), inline=True)
    embed.add_field(name="Damage Taken", value=profile.get("stats", {}).get("total_damage_taken", 0), inline=True)
    embed.add_field(name="Critical Hits", value=profile.get("stats", {}).get("critical_hits", 0), inline=True)
    if user_id in bot.stats_message_ids.get(guild.id, {}):
        try:
            message = await channel.fetch_message(bot.stats_message_ids[guild.id][user_id])
            await message.edit(embed=embed)
            print(f"Updated stats embed for {member.display_name} (ID: {user_id})")
        except discord.NotFound:
            message = await channel.send(embed=embed)
            bot.stats_message_ids.setdefault(guild.id, {})[user_id] = message.id
            print(f"Created new stats embed for {member.display_name} (ID: {user_id}, Message ID: {message.id})")
        except discord.Forbidden:
            print(f"Missing permissions to edit stats embed for {member.display_name}")
    else:
        message = await channel.send(embed=embed)
        bot.stats_message_ids.setdefault(guild.id, {})[user_id] = message.id
        print(f"Created new stats embed for {member.display_name} (ID: {user_id}, Message ID: {message.id})")

async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)
