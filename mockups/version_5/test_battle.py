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
invincible = test_rules.Invincible(5, None, None, None, a_leader.party[0])
hench = test_rules.Hench(5, None, None, None, b_leader.party[0])
test_battle.ruleset.after_rules.append(rage)
test_battle.ruleset.before_rules.append(invincible)
test_battle.ruleset.before_rules.append(hench)

print(f"Signopt's HP: {a_leader.point_unit.hp}")
print(f"Signopt's ATK: {a_leader.point_unit.atk}")

b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)

print(f"Signopt's HP: {a_leader.point_unit.hp}")
print(f"Signopt's ATK: {a_leader.point_unit.atk}")
#code.interact(local=locals())
