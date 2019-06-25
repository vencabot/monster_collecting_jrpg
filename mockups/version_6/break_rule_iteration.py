import code

import battlelib
import test_abilities
import test_rules

class BreakPhase1(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            persons_name_for_some_reason):
        super().__init__(
                "Break (Phase 1)", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.persons_name_for_some_reason = persons_name_for_some_reason

    def will_trigger_on(self, dynamic_event, battle):
        if dynamic_event.attr_name != "triggered_counter":
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"BreakPhase1 triggered! Thanks, {self.persons_name_for_some_reason}")
        print()


class BreakPhase2(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_rule):
        super().__init__(
                "Break (Phase 2)", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_rule = target_rule

    def will_trigger_on(self, dynamic_event, battle):
        if dynamic_event.attr_name != "triggered_counter":
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print("BreakPhase2 triggered!")
        print()
        try:
            battle.ruleset.after_rules.remove(self.target_rule)
        except ValueError:
            print("Target rule no longer in rule list!")
            print()


class Salty(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Salty", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print("You FUCKER.")
        print(f"{self.target_unit.unit_name} is now salty!")
        new_rule = SaltPower(10, None, None, None, self.target_unit)
        new_after_rules = battle.ruleset.after_rules.copy()
        new_after_rules.append(new_rule)
        battle.update_w_rules(
                battle.ruleset, "after_rules", new_after_rules, None, None,
                None)


class SaltPower(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Salt Power", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(f"{self.target_unit.unit_name} gains power from the salt!")
        battle.update_w_rules(
                self.target_unit, "atk", self.target_unit.atk + 1, None,
                None, None)


class Pessimism(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Pessimism", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(f"{self.target_unit.unit_name} took damage. That sucks!")
        print("For some reason, because it sucks, they hurt themselves even more!")
        battle.update_w_rules(
                self.target_unit, "hp", self.target_unit.hp - 1, None, None,
                None)




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

salty = Salty(10, None, None, None, b_leader.point_unit)
pessimism = Pessimism(10, None, None, None, b_leader.point_unit)

test_battle.ruleset.after_rules = [salty, pessimism]

for unit in a_leader.party + b_leader.party:
    battlelib.RelationshipHelper.create_ability_for(unit, test_abilities.Slap)

a_leader.point_unit.mp = 1000

a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
print()
#a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
#print()
#a_leader.point_unit.abilities[0].use_on([b_leader.point_unit], test_battle)
