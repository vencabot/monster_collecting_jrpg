import code

import battle
import test_abilities
import test_rules

test_battle = battle.Battle()

a_leader = battle.Leader("Tosmith84")
battle.RelationshipHelper.create_unit_for(a_leader, "signopt200")
battle.RelationshipHelper.create_unit_for(
        a_leader, "rageagstthearcademachine")
battle.RelationshipHelper.create_unit_for(a_leader, "KReichJr")
a_leader.point_unit = a_leader.party[0]

b_leader = battle.Leader("dixxucker")
battle.RelationshipHelper.create_unit_for(b_leader, "goodvibecity")
battle.RelationshipHelper.create_unit_for(b_leader, "Zanzhu")
battle.RelationshipHelper.create_unit_for(b_leader, "NydusTemplar")
b_leader.point_unit = b_leader.party[0]

for unit in a_leader.party + b_leader.party:
    battle.RelationshipHelper.create_ability_for(unit, test_abilities.Slap)

rage = test_rules.Rage(8, a_leader.party[0])
test_battle.ruleset.after_rules.append(rage)

b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)

#code.interact(local=locals())
