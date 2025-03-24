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

# Attribute-specific attacks
ATTRIBUTE_ATTACKS = {
    "Fire": [
        {"name": "Fireball", "damage_range": (15, 25), "effect": "A blazing fireball"},
        {"name": "Flame Burst", "damage_range": (10, 20), "effect": "A burst of flames"},
        {"name": "Inferno Strike", "damage_range": (12, 22), "effect": "A fiery slash"}
    ],
    "Water": [
        {"name": "Aqua Shot", "damage_range": (15, 25), "effect": "A precise water shot"},
        {"name": "Wave Crash", "damage_range": (10, 20), "effect": "A crashing wave"},
        {"name": "Hydro Blast", "damage_range": (12, 22), "effect": "A high-pressure blast"}
    ],
    "Air": [
        {"name": "Wind Slash", "damage_range": (15, 25), "effect": "A cutting wind blade"},
        {"name": "Gale Force", "damage_range": (10, 20), "effect": "A forceful gust"},
        {"name": "Air Vortex", "damage_range": (12, 22), "effect": "A spinning air attack"}
    ],
    "Life": [
        {"name": "Healing Pulse", "damage_range": (15, 25), "effect": "A life-infused strike"},
        {"name": "Vital Strike", "damage_range": (10, 20), "effect": "A vitality boost attack"},
        {"name": "Regen Slash", "damage_range": (12, 22), "effect": "A regenerating cut"}
    ]
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
