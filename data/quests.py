# data/quests.py
import random
from data.classes import CLASS_STATS
from data.attributes import PRIMARY_ATTRIBUTES
from data.battlefields import BATTLEFIELD_MODIFIERS

def generate_daily_quests():
    quests = {}
    # Class quests
    for class_name in CLASS_STATS.keys():
        if class_name != "Omega Fury":
            quest_type = f"Class: {class_name}"
            quest_choice = random.choice([
                "defeat", "damage", "battlefield", "attack", "combo", "low_hp", "bot"
            ])
            if quest_choice == "defeat":
                opponent = random.choice([c for c in CLASS_STATS.keys() if c != class_name and c != "Omega Fury"])
                quests[quest_type] = {"description": f"Defeat a {opponent}", "type": "class", "target": opponent, "quest_type": "defeat"}
            elif quest_choice == "damage":
                damage = random.randint(50, 150)
                opponent = random.choice([c for c in CLASS_STATS.keys() if c != class_name and c != "Omega Fury"])
                quests[quest_type] = {"description": f"Deal {damage} damage to a {opponent}", "type": "class", "target": opponent, "damage": damage, "quest_type": "damage"}
            elif quest_choice == "battlefield":
                battlefield = random.choice(list(BATTLEFIELD_MODIFIERS.keys()))
                quests[quest_type] = {"description": f"Win a battle in the {battlefield} battlefield", "type": "class", "battlefield": battlefield, "quest_type": "battlefield"}
            elif quest_choice == "attack":
                attack_count = random.randint(2, 5)
                quests[quest_type] = {"description": f"Use a {class_name} class attack {attack_count} times", "type": "class", "attack_count": attack_count, "quest_type": "attack"}
            elif quest_choice == "combo":
                quests[quest_type] = {"description": f"Perform a combo attack with {class_name}", "type": "class", "quest_type": "combo"}
            elif quest_choice == "low_hp":
                quests[quest_type] = {"description": f"Win a battle with less than 10% HP remaining as a {class_name}", "type": "class", "quest_type": "low_hp"}
            elif quest_choice == "bot":
                quests[quest_type] = {"description": f"Defeat a bot opponent as a {class_name}", "type": "class", "quest_type": "bot"}

    # Attribute quests
    for attr in PRIMARY_ATTRIBUTES:
        quest_type = f"Attribute: {attr}"
        quest_choice = random.choice([
            "defeat", "damage", "battlefield", "attack", "combo", "low_hp", "bot"
        ])
        if quest_choice == "defeat":
            opponent = random.choice([a for a in PRIMARY_ATTRIBUTES if a != attr])
            quests[quest_type] = {"description": f"Defeat a {opponent} type", "type": "attribute", "target": opponent, "quest_type": "defeat"}
        elif quest_choice == "damage":
            damage = random.randint(50, 150)
            opponent = random.choice([a for a in PRIMARY_ATTRIBUTES if a != attr])
            quests[quest_type] = {"description": f"Deal {damage} damage to a {opponent} type", "type": "attribute", "target": opponent, "damage": damage, "quest_type": "damage"}
        elif quest_choice == "battlefield":
            battlefield = random.choice(list(BATTLEFIELD_MODIFIERS.keys()))
            quests[quest_type] = {"description": f"Win a battle in the {battlefield} battlefield using {attr}", "type": "attribute", "battlefield": battlefield, "quest_type": "battlefield"}
        elif quest_choice == "attack":
            attack_count = random.randint(2, 5)
            quests[quest_type] = {"description": f"Use a {attr} attack {attack_count} times", "type": "attribute", "attack_count": attack_count, "quest_type": "attack"}
        elif quest_choice == "combo":
            second_attr = random.choice([a for a in PRIMARY_ATTRIBUTES if a != attr])
            quests[quest_type] = {"description": f"Perform a {attr}-{second_attr} combo attack", "type": "attribute", "second_attr": second_attr, "quest_type": "combo"}
        elif quest_choice == "low_hp":
            quests[quest_type] = {"description": f"Win a battle with less than 10% HP remaining using {attr}", "type": "attribute", "quest_type": "low_hp"}
        elif quest_choice == "bot":
            quests[quest_type] = {"description": f"Defeat a bot opponent using {attr}", "type": "attribute", "quest_type": "bot"}

    return quests

