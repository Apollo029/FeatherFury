# data/classes.py

# Define class statistics with emoji, stats, and description
CLASS_STATS = {
    "Winged Creature": {
        "emoji": "🕊️",
        "hp": 80,
        "attack": 20,
        "defense": 15,
        "speed": 25,
        "description": "A swift and agile creature of the skies."
    },
    "Aquatic Creature": {
        "emoji": "🐙",
        "hp": 90,
        "attack": 18,
        "defense": 20,
        "speed": 15,
        "description": "A resilient creature from the depths."
    },
    "Ground Creature": {
        "emoji": "🦁",
        "hp": 100,
        "attack": 22,
        "defense": 18,
        "speed": 12,
        "description": "A sturdy creature of the earth."
    },
    "Omega Fury": {  # Special class for FeatherFury
        "emoji": "🔥",
        "hp": 150,
        "attack": 50,
        "defense": 40,
        "speed": 30,
        "description": "An unstoppable force of nature, embodying all elements."
    }
}

# Define announcements for class selection
CLASS_ANNOUNCEMENTS = {
    "Winged Creature": [
        "Behold! {player} has ascended as a {class_name}!",
        "{player} soars into battle as a {class_name}!",
        "The skies welcome {player} as a {class_name}!"
    ],
    "Aquatic Creature": [
        "Dive in! {player} emerges as a {class_name}!",
        "{player} makes waves as a {class_name}!",
        "The depths embrace {player} as a {class_name}!"
    ],
    "Ground Creature": [
        "Feel the earth shake! {player} stands as a {class_name}!",
        "{player} roars into battle as a {class_name}!",
        "The ground trembles as {player} becomes a {class_name}!"
    ],
    "Omega Fury": [
        "The ultimate power awakens! {player} is the {class_name}!",
        "{player} unleashes chaos as the {class_name}!",
        "All tremble before {player}, the {class_name}!"
    ]
}

# Define class-specific attacks
CLASS_ATTACKS = {
    "Winged Creature": [
        {"name": "Aerial Slash", "damage_range": (15, 25), "effect": "A swift strike from above"},
        {"name": "Wind Gust", "damage_range": (10, 20), "effect": "A powerful gust of wind"},
        {"name": "Feather Storm", "damage_range": (12, 22), "effect": "A flurry of sharp feathers"}
    ],
    "Aquatic Creature": [
        {"name": "Tentacle Whip", "damage_range": (15, 25), "effect": "A lashing strike with tentacles"},
        {"name": "Ink Cloud", "damage_range": (10, 20), "effect": "A blinding cloud of ink"},
        {"name": "Tidal Slam", "damage_range": (12, 22), "effect": "A crushing wave of water"}
    ],
    "Ground Creature": [
        {"name": "Earth Roar", "damage_range": (15, 25), "effect": "A powerful roar that shakes the ground"},
        {"name": "Claw Swipe", "damage_range": (10, 20), "effect": "A swift claw attack"},
        {"name": "Boulder Charge", "damage_range": (12, 22), "effect": "A charging attack with earth force"}
    ],
    "Omega Fury": [
        {"name": "Omega Strike", "damage_range": (50, 75), "effect": "A devastating all-encompassing attack"},
        {"name": "Eternal Flame", "damage_range": (40, 60), "effect": "A fiery blast that burns all"},
        {"name": "Cataclysmic Surge", "damage_range": (45, 65), "effect": "A surge of pure omega energy"}
    ]
}
