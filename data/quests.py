# data/quests.py
import random
from data.classes import CLASS_STATS
from data.attributes import PRIMARY_ATTRIBUTES

def generate_daily_quests():
    quests = {}
    # Class quests
    for class_name in CLASS_STATS.keys():
        if class_name != "Omega Fury":
            quest_type = f"Class: {class_name}"
            opponent = random.choice([c for c in CLASS_STATS.keys() if c != class_name and c != "Omega Fury"])
            quests[quest_type] = {"description": f"Defeat a {opponent}", "type": "class", "target": opponent}
    # Attribute quests
    for attr in PRIMARY_ATTRIBUTES:
        quest_type = f"Attribute: {attr}"
        if random.random() < 0.5:
            opponent = random.choice([a for a in PRIMARY_ATTRIBUTES if a != attr])
            quests[quest_type] = {"description": f"Defeat a {opponent} type", "type": "attribute", "target": opponent}
        else:
            damage = random.randint(50, 150)
            opponent = random.choice([a for a in PRIMARY_ATTRIBUTES if a != attr])
            quests[quest_type] = {"description": f"Deal {damage} damage to a {opponent} type", "type": "attribute", "target": opponent, "damage": damage}
    return quests
