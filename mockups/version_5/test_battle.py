import code

import battle
import test_abilities
import test_rules

test_battle = battle.Battle()

a_leader = battle.Leader("Tosmith84")
a_unit1 = battle.Unit("signopt200", a_leader)
a_unit2 = battle.Unit("rageagstthearcademachine", a_leader)
a_unit3 = battle.Unit("KReichJr", a_leader)
a_leader.party = [a_unit1, a_unit2, a_unit3]
a_leader.point_unit = a_unit1

b_leader = battle.Leader("dixxucker")
b_unit1 = battle.Unit("goodvibecity", b_leader)
b_unit2 = battle.Unit("Zanzhu", b_leader)
b_unit3 = battle.Unit("NydusTemplar", b_leader)
b_leader.party = [b_unit1, b_unit2, b_unit3]
b_leader.point_unit = b_unit1

for unit in a_leader.party + b_leader.party:
    unit.abilities.append(test_abilities.Slap(unit))

rage = test_rules.Rage(8, a_unit1)
test_battle.ruleset.after_rules.append(rage)

code.interact(local=locals())
