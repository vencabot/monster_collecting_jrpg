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

#invincible = test_rules.Invincible(5, None, None, None, a_leader.party[0])
#test_battle.ruleset.before_rules.append(invincible)

hench = test_rules.Hench(5, None, None, None, b_leader.party[0])
test_battle.ruleset.before_rules.append(hench)

seal_hench = test_rules.SealRule(5, None, None, None, hench)
test_battle.ruleset.after_rules.append(seal_hench)

fade_seal = test_rules.RuleFade(1, None, None, None, seal_hench)
test_battle.ruleset.after_rules.append(fade_seal)

#persistence = test_rules.Persistence(5, None, None, None, b_leader.party[0])
#test_battle.ruleset.after_rules.append(persistence)

#old_man_genes = test_rules.OldManGenes(5, None, None, None, b_leader)
#test_battle.ruleset.after_rules.append(old_man_genes)

#poison = test_rules.Poison(3, None, None, None, a_leader.party[0])
#test_battle.ruleset.after_rules.append(poison)

#poison_fade = test_rules.RuleFade(2, None, None, None, poison)
#test_battle.ruleset.after_rules.append(poison_fade)

growing_pains = test_rules.GrowingPains(
        5, None, None, None, b_leader.party[0])
test_battle.ruleset.after_rules.append(growing_pains)

b_leader.point_unit.mp = 20

b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)
print()
a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
print()
b_leader.point_unit.abilities[0].use_on([a_leader.point_unit], test_battle)
print()
a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
print()
#code.interact(local=locals())
