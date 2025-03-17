# data/dialogue.py

COMMENTARY_TEMPLATES = [
    "{attacker} taunts {target} with a fierce strike!",
    "{attacker} roars as they attack {target}!",
    "{attacker} lands a critical blow on {target}!"
]

LEVEL_UP_DIALOGUE = {
    "Winged Creature": [
        "The crowd cheers as {player} soars to level {level}!",
        "{player} spreads their wings, rising to level {level}!"
    ],
    "Ground Creature": [
        "The earth shakes as {player} reaches level {level}!",
        "{player} stands tall at level {level}!"
    ],
    "Aquatic Creature": [
        "The waves surge as {player} advances to level {level}!",
        "{player} dives deeper, reaching level {level}!"
    ],
    "Fire": ["Flames roar as {player} ascends to level {level}!"],
    "Water": ["A tidal wave heralds {player}'s rise to level {level}!"],
    "Ice": ["A frosty wind blows as {player} reaches level {level}!"],
    "Electric": ["Sparks fly as {player} surges to level {level}!"],
    "Earth": ["The ground rumbles as {player} grows to level {level}!"],
    "Nature": ["Nature blooms as {player} advances to level {level}!"],
    "Metal": ["Steel clangs as {player} forges ahead to level {level}!"],
    "Air": ["A gust of wind lifts {player} to level {level}!"],
    "Light": ["A radiant light shines as {player} reaches level {level}!"],
    "Shadow": ["Shadows deepen as {player} rises to level {level}!"],
    "Life": ["Life energy surges as {player} grows to level {level}!"],
    "Death": ["A dark aura surrounds {player} at level {level}!"]
}

FLAIR = ["Epic!", "Legendary!", "Fierce!", "Mighty!"]

CLASS_ANNOUNCEMENTS = {
    "Winged Creature": [
        "{player} takes to the skies as a {class_name}, ready to soar above all foes!",
        "{player} spreads their wings, embracing the power of a {class_name}!",
        "With a mighty flap, {player} becomes a {class_name} of the heavens!"
    ],
    "Ground Creature": [
        "{player} stands firm as a {class_name}, a true force of the earth!",
        "The ground trembles as {player} claims the mantle of a {class_name}!",
        "{player} roars into battle, now a formidable {class_name}!"
    ],
    "Aquatic Creature": [
        "{player} dives into the depths as a {class_name}, master of the seas!",
        "The waves part for {player}, now a powerful {class_name}!",
        "{player} emerges from the ocean as a {class_name}, ready to conquer!"
    ]
}

ATTRIBUTE_ANNOUNCEMENTS = {
    "Fire": [
        "{player} ignites their spirit with the blazing power of {attribute}!",
        "A fiery aura surrounds {player} as they harness {attribute}!",
        "{player} sets the battlefield aflame with the might of {attribute}!"
    ],
    "Water": [
        "{player} commands the tides with the flowing strength of {attribute}!",
        "The waves obey {player} as they embrace {attribute}!",
        "{player} surges forward with the power of {attribute}!"
    ],
    "Ice": [
        "{player} chills the air with the frosty might of {attribute}!",
        "A frozen wind heralds {player}'s mastery of {attribute}!",
        "{player} freezes their path to victory with {attribute}!"
    ],
    "Electric": [
        "{player} crackles with the electrifying force of {attribute}!",
        "Sparks fly as {player} channels the power of {attribute}!",
        "{player} shocks the battlefield with {attribute}!"
    ],
    "Earth": [
        "{player} stands unyielding with the grounded power of {attribute}!",
        "The earth trembles as {player} claims {attribute}!",
        "{player} shapes the battlefield with the strength of {attribute}!"
    ],
    "Nature": [
        "{player} blooms with the wild energy of {attribute}!",
        "Nature bends to {player}'s will with {attribute}!",
        "{player} entwines their fate with the power of {attribute}!"
    ],
    "Metal": [
        "{player} forges their destiny with the steely resolve of {attribute}!",
        "A metallic sheen surrounds {player} as they wield {attribute}!",
        "{player} strikes with the unyielding force of {attribute}!"
    ],
    "Air": [
        "{player} soars with the swift currents of {attribute}!",
        "A gust of wind empowers {player} with {attribute}!",
        "{player} dances through the battlefield with {attribute}!"
    ],
    "Light": [
        "{player} radiates brilliance with the power of {attribute}!",
        "A holy light shines upon {player} as they harness {attribute}!",
        "{player} illuminates their path with {attribute}!"
    ],
    "Shadow": [
        "{player} cloaks themselves in darkness with {attribute}!",
        "Shadows deepen as {player} masters {attribute}!",
        "{player} strikes from the unseen with {attribute}!"
    ],
    "Life": [
        "{player} pulses with vitality through the power of {attribute}!",
        "Life blooms around {player} as they embrace {attribute}!",
        "{player} renews their strength with {attribute}!"
    ],
    "Death": [
        "{player} wields the chill of the grave with {attribute}!",
        "A dark aura surrounds {player} as they channel {attribute}!",
        "{player} commands the power of {attribute} to conquer!"
    ]
}

