import battlelib
import test_abilities
import test_rules
import test_units

test_battle = battlelib.Battle()

a_leader = battlelib.Leader("Dixxucker Prime Alpha")
battlelib.RelationshipHelper.create_unit_for(
        a_leader, test_units.Dixxucker, "Son of Dixxucker")
a_leader.point_unit = a_leader.party[0]

b_leader = battlelib.Leader("Dixxucker Prime Best")
battlelib.RelationshipHelper.create_unit_for(
        b_leader, test_units.Dixxucker, "Other Son of Dixxucker")
b_leader.point_unit = b_leader.party[0]

print(a_leader.point_unit.unit_name)
print(a_leader.point_unit.cur_hp)
print(a_leader.point_unit.primary_class.metaclass.class_name)
