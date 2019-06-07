import battlelib

class Rage(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Rage", "after", ["attack_increase"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        if self.severity < 3:
            attack_boost = 1
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting peeved!")
        elif self.severity < 8:
            attack_boost = 2
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting angry!")
        else:
            attack_boost = 3
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting mighty "
                    "pissed off!")
        print(trigger_message)
        battle.update_w_rules(
            self.target_unit, "atk", self.target_unit.atk + attack_boost,
            dynamic_event.by_ability, dynamic_event.at_effectiveness, self)


class Invincible(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness,
            from_targets, target_unit):
        super().__init__(
                "Invincible", "before", ["damage_decrease"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        if dynamic_event.by_ability is not None:
            attacker_name = dynamic_event.by_ability.owner.unit_name
        else:
            attacker_name = dynamic_event.triggering_rule.rule_name
        print(
                f"{self.target_unit.unit_name} is impervious to "
                f"{attacker_name}'s attack!")
        dynamic_event.replace_value(self.target_unit.hp, self)


class Hench(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Hench", "before", ["damage_increase"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and dynamic_event.timeline[0].triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"{self.target_unit.unit_name} is hench'd out! Their "
                "damage doubles!")
        old_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp_value = dynamic_event.target.hp - old_damage * 2
        dynamic_event.replace_value(new_hp_value, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.timeline[0]
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"{self.target_unit.unit_name} is hench'd out! But "
                    "they failed to do damage!")


class AndOne(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "And One", "before", ["damage_increase"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and dynamic_event.timeline[0].triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"And one! {self.target_unit.unit_name} gets extra damage!")
        dynamic_event.replace_value(dynamic_event.new_value - 1, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.timeline[0]
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"And- wha...? {self.target_unit.unit_name} failed to "
                    "do damage!")


class Persistence(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Persistence", "after", ["attack_increase"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        original_event = dynamic_event.timeline[0]
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"{self.target_unit.unit_name} failed to do damage, but "
                f"they won't give up! {self.target_unit.unit_name} gained "
                "extra attack power!")
        battle.update_w_rules(
                self.target_unit, "atk", self.target_unit.atk + 1,
                dynamic_event.by_ability, dynamic_event.at_effectiveness,
                self)


class OldManGenes(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_leader):
        super().__init__(
                "Old Man Genes", "after", ["attack_decrease"], severity,
                from_ability, from_effectiveness, from_targets)
        self.target_leader = target_leader

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_leader
                and dynamic_event.attr_name == "ap"
                and dynamic_event.old_value >= 5
                and dynamic_event.new_value < 5):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"{self.target_leader.leader_name}'s entire party has the "
                "old man genes! They're all drowsy. Attack power down! T_T")
        for battle_unit in self.target_leader.party:
            battle.update_w_rules(
                    battle_unit, "atk", battle_unit.atk - 1,
                    dynamic_event.by_ability,
                    dynamic_event.at_effectiveness, self)


class Poison(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_unit):
        super().__init__(
                "Poison", "after", ["hp_damage"], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.by_ability is not None
                and dynamic_event.by_ability.owner is self.target_unit
                and not dynamic_event.triggering_rule):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(
                f"{self.target_unit.unit_name} suffered the effects of "
                f"Poison! They're taking {self.severity} damage!")
        battle.update_w_rules(
                self.target_unit, "hp",
                self.target_unit.hp - self.severity,
                self.from_ability, "normal", self)


#class SealRule(battlelib.DynamicRule):
#    def __init__(
#            self, from_ability, from_effectiveness, from_targets,
#            target_rule):
#        super().__init__(
#                "Seal Rule", "before", [], 10, from_ability,
#                from_effectiveness, from_targets)
#        self.target_rule = target_rule
#
#    def will_trigger_on(self, dynamic_event, battle):
#        if (
#                dynamic_event.triggering_rule is self.target_rule):
#            return True
#        return False

#    def trigger(self, dynamic_event, battle):
#        rolled_back_event = dynamic_event
        # I want to UNDO the event that was
#        while (
#                rolled_back_event.replaces
#                and (
#                    rolled_back_event.replaces.triggering_rule
#                    is self.target_rule)):
#            rolled_back_event = rolled_back_event.replaces
#        dynamic_event.replace_value(rolled_back_event.old_value, self)
#        print(f"The effect of {self.target_rule.rule_name} was sealed!")


class RuleFade(battlelib.DynamicRule):
    def __init__(
            self, severity, from_ability, from_effectiveness, from_targets,
            target_rule):
        super().__init__(
                "Rule Fade", "after", [], severity, from_ability,
                from_effectiveness, from_targets)
        self.target_rule = target_rule

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_rule
                and dynamic_event.attr_name == "triggered_counter"
                and dynamic_event.new_value > dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        print(f"{self.target_rule.rule_name} has faded slightly!")
        battle.update_w_rules(
                self, "severity", self.severity - 1, self.from_ability,
                "normal", self)
        if self.severity == 0:
            print(f"{self.target_rule.rule_name} has faded completely!")
            if self.target_rule.check_phase == "before":
                new_rules = battle.ruleset.before_rules.copy()
                new_rules.remove(self.target_rule)
                battle.update_w_rules(
                        battle.ruleset, "before_rules", new_rules,
                        self.from_ability, "normal", self)
            elif self.target_rule.check_phase == "after":
                new_rules = battle.ruleset.after_rules.copy()
                new_rules.remove(self.target_rule)
                battle.update_w_rules(
                        battle.ruleset, "after_rules", new_rules,
                        self.from_ability, "normal", self)
            new_rules = battle.ruleset.after_rules.copy()
            new_rules.remove(self)
            battle.update_w_rules(
                    battle.ruleset, "after_rules", new_rules,
                    self.from_ability, "normal", self)

