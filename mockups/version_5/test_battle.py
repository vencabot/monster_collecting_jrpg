import code

import battlelib
import test_abilities
import test_rules

test_battle = battlelib.Battle()

a_leader = battlelib.Leader("Tosmith84")
battlelib.RelationshipHelper.create_unit_for(a_leader, "signopt200")
battlelib.RelationshipHelper.create_unit_for(
        a_leader, "rageagstthearcademachine")
battlelib.RelationshipHelper.create_unit_for(a_leader, "KReichJr")
a_leader.point_unit = a_leader.party[0]

b_leader = battlelib.Leader("dixxucker")
battlelib.RelationshipHelper.create_unit_for(b_leader, "goodvibecity")
battlelib.RelationshipHelper.create_unit_for(b_leader, "Zanzhu")
battlelib.RelationshipHelper.create_unit_for(b_leader, "NydusTemplar")
b_leader.point_unit = b_leader.party[0]

for unit in a_leader.party + b_leader.party:
    battlelib.RelationshipHelper.create_ability_for(unit, test_abilities.Slap)

rage = test_rules.Rage(8, None, None, None, a_leader.party[0])
test_battle.ruleset.after_rules.append(rage)

invincible = test_rules.Invincible(5, None, None, None, a_leader.party[0])
test_battle.ruleset.before_rules.append(invincible)

hench = test_rules.Hench(5, None, None, None, b_leader.party[0])
test_battle.ruleset.before_rules.append(hench)

persistence = test_rules.Persistence(5, None, None, None, b_leader.party[0])
test_battle.ruleset.after_rules.append(persistence)

old_man_genes = test_rules.OldManGenes(5, None, None, None, b_leader)
test_battle.ruleset.after_rules.append(old_man_genes)

poison = test_rules.Poison(3, None, None, None, a_leader.party[0])
test_battle.ruleset.after_rules.append(poison)

poison_fade = test_rules.RuleFade(2, None, None, None, poison)
test_battle.ruleset.after_rules.append(poison_fade)

b_leader.point_unit.mp = 20

print(f"Signopt's HP: {a_leader.point_unit.hp}")
print(f"Signopt's ATK: {a_leader.point_unit.atk}")
print()
print(f"GoodVibe's HP: {b_leader.point_unit.hp}")
print(f"GoodVibe's ATK: {b_leader.point_unit.atk}")
print(f"Zanzhu's ATK: {b_leader.party[1].atk}")
print(f"Templar's ATK: {b_leader.party[2].atk}")
print()
b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)
print()
a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
print()
b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)
print()
a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
print()
print(f"Signopt's HP: {a_leader.point_unit.hp}")
print(f"Signopt's ATK: {a_leader.point_unit.atk}")
print()
print(f"GoodVibe's HP: {b_leader.point_unit.hp}")
print(f"GoodVibe's ATK: {b_leader.point_unit.atk}")
print(f"Zanzhu's ATK: {b_leader.party[1].atk}")
print(f"Templar's ATK: {b_leader.party[2].atk}")
#code.interact(local=locals())
