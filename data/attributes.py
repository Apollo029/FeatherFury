# data/attributes.py

# Primary attributes available for selection
PRIMARY_ATTRIBUTES = [
    "Fire", "Water", "Ice", "Electric", "Earth", "Nature",
    "Metal", "Air", "Light", "Shadow", "Life", "Death"
]

# Emoji mapping for attributes
attribute_emojis = {
    "Fire": "🔥",
    "Water": "💧",
    "Ice": "❄️",
    "Electric": "⚡",
    "Earth": "🌍",
    "Nature": "🌿",
    "Metal": "🔩",
    "Air": "💨",
    "Light": "✨",
    "Shadow": "🌑",
    "Life": "💖",
    "Death": "💀"
}

# Fallback for attribute emojis
attribute_emoji_fallbacks = {attr: attr.lower() for attr in PRIMARY_ATTRIBUTES}

# Descriptions for attributes
ATTRIBUTE_DESCRIPTIONS = {
    "Fire": "Ignites enemies with fiery attacks, strong against Ice but weak to Water.",
    "Water": "Controls the flow of battle with fluid strikes, strong against Fire but weak to Electric.",
    "Ice": "Freezes foes with chilling precision, strong against Nature but weak to Fire.",
    "Electric": "Shocks opponents with electrifying speed, strong against Water but weak to Earth.",
    "Earth": "Stands firm with grounded power, strong against Electric but weak to Air.",
    "Nature": "Harnesses the power of growth, strong against Earth but weak to Ice.",
    "Metal": "Forged with unyielding strength, strong against Light but weak to Fire.",
    "Air": "Soars with swift, breezy attacks, strong against Earth but weak to Electric.",
    "Light": "Radiates with brilliant energy, strong against Shadow but weak to Metal.",
    "Shadow": "Strikes from the darkness, strong against Life but weak to Light.",
    "Life": "Pulses with vital energy, strong against Death but weak to Shadow.",
    "Death": "Brings grim finality, strong against Nature but weak to Life."
}

# Announcements for attribute selection
ATTRIBUTE_ANNOUNCEMENTS = {
    "Fire": [
        "{player} ignites their power with the {attribute} attribute!",
        "Feel the heat! {player} harnesses the {attribute} attribute!",
        "{player} blazes a trail with the {attribute} attribute!"
    ],
    "Water": [
        "{player} flows with the power of the {attribute} attribute!",
        "A tidal surge! {player} channels the {attribute} attribute!",
        "{player} dives deep with the {attribute} attribute!"
    ],
    "Ice": [
        "{player} chills the battlefield with the {attribute} attribute!",
        "A frosty edge! {player} wields the {attribute} attribute!",
        "{player} freezes foes with the {attribute} attribute!"
    ],
    "Electric": [
        "{player} shocks all with the {attribute} attribute!",
        "A charged strike! {player} uses the {attribute} attribute!",
        "{player} electrifies the fight with the {attribute} attribute!"
    ],
    "Earth": [
        "{player} stands firm with the {attribute} attribute!",
        "A solid foundation! {player} gains the {attribute} attribute!",
        "{player} shakes the ground with the {attribute} attribute!"
    ],
    "Nature": [
        "{player} blooms with the {attribute} attribute!",
        "A natural force! {player} harnesses the {attribute} attribute!",
        "{player} grows strong with the {attribute} attribute!"
    ],
    "Metal": [
        "{player} forges ahead with the {attribute} attribute!",
        "A steel resolve! {player} wields the {attribute} attribute!",
        "{player} shines with the {attribute} attribute!"
    ],
    "Air": [
        "{player} soars with the {attribute} attribute!",
        "A breezy advantage! {player} channels the {attribute} attribute!",
        "{player} sweeps in with the {attribute} attribute!"
    ],
    "Light": [
        "{player} radiates with the {attribute} attribute!",
        "A brilliant glow! {player} harnesses the {attribute} attribute!",
        "{player} shines bright with the {attribute} attribute!"
    ],
    "Shadow": [
        "{player} cloaks in the {attribute} attribute!",
        "A dark presence! {player} uses the {attribute} attribute!",
        "{player} lurks with the {attribute} attribute!"
    ],
    "Life": [
        "{player} thrives with the {attribute} attribute!",
        "A vital surge! {player} channels the {attribute} attribute!",
        "{player} pulses with the {attribute} attribute!"
    ],
    "Death": [
        "{player} reaps with the {attribute} attribute!",
        "A grim power! {player} wields the {attribute} attribute!",
        "{player} brings doom with the {attribute} attribute!"
    ]
}

# Flair messages for announcements
FLAIR = [
    "✨ Epic choice!",
    "🔥 Ready to dominate!",
    "⚡ Power unleashed!",
    "🌟 A new legend rises!",
    "💥 Let’s battle!"
]

# Attribute-specific attacks
ATTRIBUTE_ATTACKS = {
    "Fire": [
        {"name": "Fireball", "damage_range": (15, 25), "effect": "A blazing fireball"},
        {"name": "Flame Storm", "damage_range": (10, 20), "effect": "A storm of flames"},
        {"name": "Uncontrollable Blaze", "damage_range": (12, 22), "effect": "An intense fiery explosion"}
    ],
    "Water": [
        {"name": "Aqua Shot", "damage_range": (15, 25), "effect": "A precise water shot"},
        {"name": "Wave Crash", "damage_range": (10, 20), "effect": "A crashing wave"},
        {"name": "Hydro Blast", "damage_range": (12, 22), "effect": "A high-pressure blast"}
    ],
    "Ice": [
        {"name": "Frost Jet", "damage_range": (15, 25), "effect": "A jet of freezing ice"},
        {"name": "Blizzard Burst", "damage_range": (10, 20), "effect": "A burst of icy wind"},
        {"name": "Glacial Spike", "damage_range": (12, 22), "effect": "A sharp spike of ice"}
    ],
    "Electric": [
        {"name": "Thunder Bolt", "damage_range": (15, 25), "effect": "A powerful electric bolt"},
        {"name": "Shock Wave", "damage_range": (10, 20), "effect": "A wave of electricity"},
        {"name": "Lightning Strike", "damage_range": (12, 22), "effect": "A targeted lightning strike"}
    ],
    "Earth": [
        {"name": "Rock Smash", "damage_range": (15, 25), "effect": "A crushing rock attack"},
        {"name": "Earth Tremor", "damage_range": (10, 20), "effect": "A ground-shaking tremor"},
        {"name": "Boulder Toss", "damage_range": (12, 22), "effect": "A heavy boulder throw"}
    ],
    "Nature": [
        {"name": "Vine Whip", "damage_range": (15, 25), "effect": "A lashing vine attack"},
        {"name": "Thorn Barrage", "damage_range": (10, 20), "effect": "A barrage of sharp thorns"},
        {"name": "Petal Storm", "damage_range": (12, 22), "effect": "A storm of razor-sharp petals"}
    ],
    "Metal": [
        {"name": "Steel Strike", "damage_range": (15, 25), "effect": "A powerful metal strike"},
        {"name": "Iron Slam", "damage_range": (10, 20), "effect": "A heavy iron slam"},
        {"name": "Blade Surge", "damage_range": (12, 22), "effect": "A surge of metallic energy"}
    ],
    "Air": [
        {"name": "Wind Slash", "damage_range": (15, 25), "effect": "A cutting wind blade"},
        {"name": "Gale Force", "damage_range": (10, 20), "effect": "A forceful gust"},
        {"name": "Tornado Spin", "damage_range": (12, 22), "effect": "A spinning tornado attack"}
    ],
    "Light": [
        {"name": "Radiant Beam", "damage_range": (15, 25), "effect": "A beam of radiant light"},
        {"name": "Holy Glow", "damage_range": (10, 20), "effect": "A glowing burst of light"},
        {"name": "Solar Flare", "damage_range": (12, 22), "effect": "A flare of solar energy"}
    ],
    "Shadow": [
        {"name": "Dark Pulse", "damage_range": (15, 25), "effect": "A pulse of dark energy"},
        {"name": "Shadow Veil", "damage_range": (10, 20), "effect": "A veil of shadows"},
        {"name": "Abyssal Strike", "damage_range": (12, 22), "effect": "A strike from the abyss"}
    ],
    "Life": [
        {"name": "Healing Pulse", "damage_range": (15, 25), "effect": "A life-infused strike"},
        {"name": "Vital Strike", "damage_range": (10, 20), "effect": "A vitality boost attack"},
        {"name": "Regen Slash", "damage_range": (12, 22), "effect": "A regenerating cut"}
    ],
    "Death": [
        {"name": "Grim Touch", "damage_range": (15, 25), "effect": "A touch of death"},
        {"name": "Necrotic Wave", "damage_range": (10, 20), "effect": "A wave of necrotic energy"},
        {"name": "Chilling Reaper", "damage_range": (12, 22), "effect": "A reaper's chilling strike"}
    ]
}

# Additional attacks for attribute-battlefield interactions
ATTRIBUTE_INTERACTION_ATTACKS = {
    "Fire_Heat": [
        {"name": "Inferno Blast", "damage_range": (20, 30), "effect": "An intensified fiery blast"},
        {"name": "Scorching Wave", "damage_range": (15, 25), "effect": "A wave of scorching heat"},
        {"name": "Blazing Vortex", "damage_range": (17, 27), "effect": "A swirling vortex of flames"}
    ],
    "Water_Cold": [
        {"name": "Frost Jet", "damage_range": (15, 25), "effect": "A jet of freezing ice"},
        {"name": "Blizzard Burst", "damage_range": (10, 20), "effect": "A burst of icy wind"},
        {"name": "Glacial Spike", "damage_range": (12, 22), "effect": "A sharp spike of ice"}
    ],
    "Ice_Heat": [
        {"name": "Aqua Shot", "damage_range": (15, 25), "effect": "A precise water shot"},
        {"name": "Wave Crash", "damage_range": (10, 20), "effect": "A crashing wave"},
        {"name": "Hydro Blast", "damage_range": (12, 22), "effect": "A high-pressure blast"}
    ],
    "Light_Earth": [
        {"name": "Crystal Flash", "damage_range": (15, 25), "effect": "A flash of crystalline light"},
        {"name": "Prism Burst", "damage_range": (10, 20), "effect": "A burst of prismatic energy"},
        {"name": "Gem Shine", "damage_range": (12, 22), "effect": "A shining gem attack"}
    ],
    "Fire_Air": [
        {"name": "Blazing Wind", "damage_range": (15, 25), "effect": "A fiery gust of wind"},
        {"name": "Scorching Breeze", "damage_range": (10, 20), "effect": "A hot, burning breeze"},
        {"name": "Fire Tornado", "damage_range": (12, 22), "effect": "A tornado of flames"}
    ],
    "Earth_Nature": [
        {"name": "Vine Crush", "damage_range": (15, 25), "effect": "A crushing vine attack"},
        {"name": "Root Slam", "damage_range": (10, 20), "effect": "A slamming root strike"},
        {"name": "Petal Quake", "damage_range": (12, 22), "effect": "A quaking petal storm"}
    ],
    "Metal_Electric": [
        {"name": "Thunder Forge", "damage_range": (15, 25), "effect": "A forged electric strike"},
        {"name": "Shock Alloy", "damage_range": (10, 20), "effect": "A shocking metal attack"},
        {"name": "Volt Blade", "damage_range": (12, 22), "effect": "A blade charged with voltage"}
    ],
    "Shadow_Death": [
        {"name": "Grim Touch", "damage_range": (15, 25), "effect": "A touch of death"},
        {"name": "Necrotic Wave", "damage_range": (10, 20), "effect": "A wave of necrotic energy"},
        {"name": "Chilling Reaper", "damage_range": (12, 22), "effect": "A reaper's chilling strike"}
    ],
    "Life_Light": [
        {"name": "Holy Glow", "damage_range": (15, 25), "effect": "A glowing burst of light"},
        {"name": "Radiant Heal", "damage_range": (10, 20), "effect": "A healing radiant burst"},
        {"name": "Luminous Pulse", "damage_range": (12, 22), "effect": "A pulsing light attack"}
    ],
    "Water_Nature": [
        {"name": "Tidal Bloom", "damage_range": (15, 25), "effect": "A blooming tidal wave"},
        {"name": "Aqua Vine", "damage_range": (10, 20), "effect": "A vine infused with water"},
        {"name": "Petal Surge", "damage_range": (12, 22), "effect": "A surge of water and petals"}
    ],
    "Ice_Shadow": [
        {"name": "Frozen Shade", "damage_range": (15, 25), "effect": "A shadowy ice attack"},
        {"name": "Dark Frost", "damage_range": (10, 20), "effect": "A frosty dark strike"},
        {"name": "Icy Veil", "damage_range": (12, 22), "effect": "A veil of icy shadows"}
    ],
    "Electric_Air": [
        {"name": "Storm Surge", "damage_range": (15, 25), "effect": "A surging storm attack"},
        {"name": "Thunder Gust", "damage_range": (10, 20), "effect": "A gust charged with thunder"},
        {"name": "Lightning Wind", "damage_range": (12, 22), "effect": "A wind infused with lightning"}
    ],
    "Earth_Metal": [
        {"name": "Iron Quake", "damage_range": (15, 25), "effect": "A quaking iron strike"},
        {"name": "Steel Boulder", "damage_range": (10, 20), "effect": "A boulder of steel"},
        {"name": "Metal Crush", "damage_range": (12, 22), "effect": "A crushing metal attack"}
    ],
    "Nature_Life": [
        {"name": "Blooming Vitality", "damage_range": (15, 25), "effect": "A vital blooming strike"},
        {"name": "Life Sprout", "damage_range": (10, 20), "effect": "A sprouting life attack"},
        {"name": "Vital Blossom", "damage_range": (12, 22), "effect": "A blossoming vital strike"}
    ],
    "Metal_Fire": [
        {"name": "Molten Slash", "damage_range": (15, 25), "effect": "A slash of molten metal"},
        {"name": "Fiery Forge", "damage_range": (10, 20), "effect": "A forged fiery attack"},
        {"name": "Blazing Steel", "damage_range": (12, 22), "effect": "A steel attack with flames"}
    ],
    "Air_Light": [
        {"name": "Radiant Gust", "damage_range": (15, 25), "effect": "A gust of radiant light"},
        {"name": "Shining Breeze", "damage_range": (10, 20), "effect": "A breeze of shining light"},
        {"name": "Luminous Wind", "damage_range": (12, 22), "effect": "A wind infused with light"}
    ],
    "Shadow_Earth": [
        {"name": "Abyssal Quake", "damage_range": (15, 25), "effect": "A quaking abyssal strike"},
        {"name": "Dark Tremor", "damage_range": (10, 20), "effect": "A dark ground tremor"},
        {"name": "Shadow Boulder", "damage_range": (12, 22), "effect": "A boulder of shadows"}
    ],
    "Death_Ice": [
        {"name": "Chilling Reaper", "damage_range": (15, 25), "effect": "A reaper's chilling strike"},
        {"name": "Frozen Doom", "damage_range": (10, 20), "effect": "A frozen touch of doom"},
        {"name": "Icy Grave", "damage_range": (12, 22), "effect": "A grave of ice"}
    ],
    "Life_Water": [
        {"name": "Restorative Wave", "damage_range": (15, 25), "effect": "A wave of restorative energy"},
        {"name": "Vital Tide", "damage_range": (10, 20), "effect": "A tide of vital energy"},
        {"name": "Healing Surge", "damage_range": (12, 22), "effect": "A surge of healing water"}
    ],
    "Light_Fire": [
        {"name": "Solar Flare", "damage_range": (15, 25), "effect": "A flare of solar energy"},
        {"name": "Blazing Light", "damage_range": (10, 20), "effect": "A light infused with fire"},
        {"name": "Radiant Blaze", "damage_range": (12, 22), "effect": "A blazing radiant attack"}
    ]
}
