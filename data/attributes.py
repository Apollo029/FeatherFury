# data/attributes.py

PRIMARY_ATTRIBUTES = [
    "Fire", "Water", "Ice", "Electric", "Earth", "Nature",
    "Metal", "Air", "Light", "Shadow", "Life", "Death"
]

attribute_emojis = {
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

attribute_emoji_fallbacks = {
    "Fire": "fire",
    "Water": "droplet",
    "Ice": "snowflake",
    "Electric": "zap",
    "Earth": "earth_africa",
    "Nature": "herb",
    "Metal": "nut_and_bolt",
    "Air": "dash",
    "Light": "sparkles",
    "Shadow": "new_moon",
    "Life": "sparkling_heart",
    "Death": "skull"
}

ATTRIBUTE_ATTACKS = {
    "Fire": [
        {"name": "Fire Blast", "damage_range": (15, 25), "effect": "Set your enemies ablaze and dominate the battlefield with this heated firepower!"},
        {"name": "Inferno Sweep", "damage_range": (10, 20), "effect": "Unleash a searing wave to scorch your foes and claim victory through flames!"},
        {"name": "Blazing Strike", "damage_range": (12, 22), "effect": "Ignite the skies with a fiery assault that overwhelms your adversaries!"}
    ],
    "Water": [
        {"name": "Tidal Wave", "damage_range": (12, 22), "effect": "Command the tides to overwhelm your enemies with the power of the deep!"},
        {"name": "Aqua Jet", "damage_range": (10, 20), "effect": "Ride the currents with swift precision to outmaneuver your rivals!"},
        {"name": "Hydro Burst", "damage_range": (15, 25), "effect": "Flood the battlefield with a torrent that bends nature to your will!"}
    ],
    "Ice": [
        {"name": "Frostbite Slash", "damage_range": (10, 20), "effect": "Freeze your foes in their tracks with the chilling might of ice!"},
        {"name": "Glacial Spike", "damage_range": (15, 25), "effect": "Pierce the heart of battle with a frozen lance of icy power!"},
        {"name": "Blizzard Blast", "damage_range": (12, 22), "effect": "Summon a storm of frost to paralyze your enemies with cold fury!"}
    ],
    "Electric": [
        {"name": "Thunderbolt", "damage_range": (15, 25), "effect": "Strike with the fury of a storm and electrify the battlefield!"},
        {"name": "Shock Pulse", "damage_range": (10, 20), "effect": "Channel a surge of energy to outpace and outlast your foes!"},
        {"name": "Lightning Strike", "damage_range": (12, 22), "effect": "Unleash a bolt from the heavens to command the skies in combat!"}
    ],
    "Earth": [
        {"name": "Quake Slam", "damage_range": (12, 22), "effect": "Shake the ground and assert dominance with the strength of the earth!"},
        {"name": "Boulder Toss", "damage_range": (15, 25), "effect": "Hurl the weight of mountains to crush your enemies with raw power!"},
        {"name": "Stone Surge", "damage_range": (10, 20), "effect": "Rise like a titan with the unyielding force of the land!"}
    ],
    "Nature": [
        {"name": "Vine Whip", "damage_range": (10, 20), "effect": "Entwine your foes with the wild embrace of nature’s wrath!"},
        {"name": "Petal Storm", "damage_range": (12, 22), "effect": "Unleash a whirlwind of blossoms to dazzle and conquer your rivals!"},
        {"name": "Thorn Barrage", "damage_range": (15, 25), "effect": "Pierce the battlefield with nature’s thorns and claim your victory!"}
    ],
    "Metal": [
        {"name": "Steel Slash", "damage_range": (15, 25), "effect": "Forge a path to glory with the unyielding edge of steel!"},
        {"name": "Iron Bash", "damage_range": (12, 22), "effect": "Smash through defenses with the might of forged iron!"},
        {"name": "Alloy Burst", "damage_range": (10, 20), "effect": "Explode with metallic fury to overwhelm your adversaries!"}
    ],
    "Air": [
        {"name": "Gale Force", "damage_range": (12, 22), "effect": "Ride the winds to strike with unmatched speed and grace!"},
        {"name": "Tornado Spin", "damage_range": (15, 25), "effect": "Whirl through the battlefield with a tempest of power!"},
        {"name": "Wind Slash", "damage_range": (10, 20), "effect": "Slice through the air to dominate with aerial mastery!"}
    ],
    "Light": [
        {"name": "Divine Light", "damage_range": (15, 25), "effect": "Radiate with holy brilliance to blind and conquer your foes!"},
        {"name": "Radiant Beam", "damage_range": (12, 22), "effect": "Channel a beam of light to inspire victory on the battlefield!"},
        {"name": "Luminous Pulse", "damage_range": (10, 20), "effect": "Illuminate the fight with a surge of radiant power!"}
    ],
    "Shadow": [
        {"name": "Dark Pulse", "damage_range": (15, 25), "effect": "Weave shadows to weaken your enemies with eerie precision!"},
        {"name": "Night Slash", "damage_range": (12, 22), "effect": "Strike from the darkness with a blade of night!"},
        {"name": "Umbral Strike", "damage_range": (10, 20), "effect": "Embrace the shadows to outmaneuver and overpower your rivals!"}
    ],
    "Life": [
        {"name": "Healing Touch", "damage_range": (5, 15), "effect": "Infuse the battlefield with vitality and renew your strength!"},
        {"name": "Vital Surge", "damage_range": (10, 20), "effect": "Awaken a surge of life to bolster your defenses!"},
        {"name": "Bloom Burst", "damage_range": (12, 22), "effect": "Blossom with life energy to turn the tide of battle!"}
    ],
    "Death": [
        {"name": "Necrotic Grasp", "damage_range": (15, 25), "effect": "Harness the chill of death to command the battlefield!"},
        {"name": "Grave Chill", "damage_range": (12, 22), "effect": "Spread a cold shadow to sap the will of your foes!"},
        {"name": "Deathly Strike", "damage_range": (10, 20), "effect": "Strike with the inevitability of death to claim victory!"}
    ]
}

