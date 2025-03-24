# data/battlefields.py

BATTLEFIELD_MODIFIERS = {
    "Fire": {"Fire": {"type": "boost", "value": 1.2}, "Ice": {"type": "nerf", "value": 0.8}},
    "Water": {"Water": {"type": "boost", "value": 1.2}, "Electric": {"type": "nerf", "value": 0.8}},
    "Ice": {"Ice": {"type": "boost", "value": 1.2}, "Fire": {"type": "nerf", "value": 0.8}},
    "Electric": {"Electric": {"type": "boost", "value": 1.2}, "Earth": {"type": "nerf", "value": 0.8}},
    "Earth": {"Earth": {"type": "boost", "value": 1.2}, "Air": {"type": "nerf", "value": 0.8}},
    "Nature": {"Nature": {"type": "boost", "value": 1.2}, "Ice": {"type": "nerf", "value": 0.8}},
    "Metal": {"Metal": {"type": "boost", "value": 1.2}, "Fire": {"type": "nerf", "value": 0.8}},
    "Air": {"Air": {"type": "boost", "value": 1.2}, "Electric": {"type": "nerf", "value": 0.8}},
    "Light": {"Light": {"type": "boost", "value": 1.2}, "Shadow": {"type": "nerf", "value": 0.8}},
    "Shadow": {"Shadow": {"type": "boost", "value": 1.2}, "Light": {"type": "nerf", "value": 0.8}},
    "Life": {"Life": {"type": "boost", "value": 1.2}, "Death": {"type": "nerf", "value": 0.8}},
    "Death": {"Death": {"type": "boost", "value": 1.2}, "Life": {"type": "nerf", "value": 0.8}}
}

BATTLEFIELD_DESCRIPTIONS = {
    "Fire": "A blazing inferno where Fire attacks are stronger and Ice attacks are weaker.",
    "Water": "A vast ocean where Water attacks are stronger and Electric attacks are weaker.",
    "Ice": "A frozen tundra where Ice attacks are stronger and Fire attacks are weaker.",
    "Electric": "A stormy field where Electric attacks are stronger and Earth attacks are weaker.",
    "Earth": "A rocky terrain where Earth attacks are stronger and Air attacks are weaker.",
    "Nature": "A lush forest where Nature attacks are stronger and Ice attacks are weaker.",
    "Metal": "A metallic forge where Metal attacks are stronger and Fire attacks are weaker.",
    "Air": "A windy sky where Air attacks are stronger and Electric attacks are weaker.",
    "Light": "A radiant plain where Light attacks are stronger and Shadow attacks are weaker.",
    "Shadow": "A dark abyss where Shadow attacks are stronger and Light attacks are weaker.",
    "Life": "A vibrant meadow where Life attacks are stronger and Death attacks are weaker.",
    "Death": "A grim graveyard where Death attacks are stronger and Life attacks are weaker."
}
