import battle_4

class Rage(battle_4.DynamicRule):
    def __init__(self, ruleset, target_unit, severity):
        super().__init__(
                ruleset, "Rage", "after", ["attack_increase"], severity,
                None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
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
        self.target_unit.update_w_rules(
            "atk", self.target_unit.atk + attack_boost,
            dynamic_event.perpetrated_by, dynamic_event.with_ability,
            dynamic_event.at_effectiveness, self)


class Invincible(battle_4.DynamicRule):
    def __init__(self, ruleset, target_unit, severity):
        super().__init__(
                ruleset, "Invincible", "before", ["damage_decrease"],
                severity, None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} is impervious to "
                f"{dynamic_event.perpetrated_by.unit_name}'s attack!")
        dynamic_event.replace_value(self.target_unit.hp, self)


class Hench(battle_4.DynamicRule):
    def __init__(self, ruleset, target_unit, severity):
        super().__init__(
                ruleset, "Hench", "before", ["damage_increase"], severity,
                None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} is hench'd out! Their "
                "damage doubles!")
        old_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp_value = dynamic_event.target.hp - old_damage * 2
        dynamic_event.replace_value(new_hp_value, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"{self.target_unit.unit_name} is hench'd out! But "
                    "they failed to do damage!")


class AndOne(battle_4.DynamicRule):
    def __init__(self, ruleset, target_unit, severity):
        super().__init__(
                ruleset, "And One", "before", ["damage_increase"],
                severity, None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"And one! {self.target_unit.unit_name} gets extra damage!")
        dynamic_event.replace_value(dynamic_event.new_value - 1, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"And- wha...? {self.target_unit.unit_name} failed to "
                    "do damage!")


class Persistence(battle_4.DynamicRule):
    def __init__(self, ruleset, target_unit, severity):
        super().__init__(
                ruleset, "Persistence", "after", ["attack_increase"],
                severity, None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} failed to do damage, but "
                f"they won't give up! {self.target_unit.unit_name} gained "
                "extra attack power!")
        self.target_unit.update_w_rules(
                "atk", self.target_unit.atk + 1, self.target_unit,
                dynamic_event.with_ability, dynamic_event.at_effectiveness,
                self)


class OldManGenes(battle_4.DynamicRule):
    def __init__(self, ruleset, target_leader, severity):
        super().__init__(
                ruleset, "Old Man Genes", "after", ["attack_decrease"],
                severity, None, None)
        self.target_leader = target_leader

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_leader
                and dynamic_event.attr_name == "ap"
                and dynamic_event.old_value >= 5
                and dynamic_event.new_value < 5):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_leader.leader_name}'s entire party has the "
                "old man genes! They're all drowsy. Attack power down! T_T")
        for battle_unit in self.target_leader.party:
            battle_unit.update_w_rules(
                    "atk", battle_unit.atk - 1,
                    dynamic_event.perpetrated_by,
                    dynamic_event.with_ability,
                    dynamic_event.at_effectiveness, self)


class Poison(battle_4.DynamicRule):
    def __init__(self, ruleset, severity, target_unit):
        super().__init__(
                ruleset, "Poison", "after", ["hp_damage"], severity, None,
                None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and not dynamic_event.triggering_rule
                and dynamic_event.with_ability):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} suffered the effects of "
                f"Poison! They're taking {self.severity} damage!")
        self.target_unit.update_w_rules(
                "hp", self.target_unit.hp - self.severity, self.target_unit,
                dynamic_event.with_ability, dynamic_event.at_effectiveness,
                self)


class SealRule(battle_4.DynamicRule):
    def __init__(
            self, ruleset, initiated_by, with_ability, target_rule):
        super().__init__(
                ruleset, "Seal Rule", "before", [], 10, initiated_by,
                with_ability)
        self.target_rule = target_rule

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.triggering_rule is self.target_rule):
            return True
        return False

    def trigger(self, dynamic_event):
        rolled_back_event = dynamic_event
        while (
                rolled_back_event.replaces
                and (
                    rolled_back_event.replaces.triggering_rule
                    is self.target_rule)):
            rolled_back_event = rolled_back_event.replaces
        dynamic_event.replace_value(rolled_back_event.old_value, self)
        print(f"The effect of {self.target_rule.rule_name} was sealed!")


class RuleFade(battle_4.DynamicRule):
    def __init__(
            self, ruleset, severity, initiated_by, with_ability,
            target_rule):
        super().__init__(
                ruleset, "Rule Fade", "after", [], severity, initiated_by,
                with_ability)
        self.target_rule = target_rule

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.triggering_rule is self.target_rule):
            return True
        return False

    def trigger(self, dynamic_event):
        print(f"{self.target_rule.rule_name} has faded slightly!")
        self.update_w_rules(
                "severity", self.severity - 1, self.initiated_by,
                self.with_ability, "normal", self)
        if self.severity == 0:
            print(f"{self.target_rule.rule_name} has faded completely!")
            new_rules = self.ruleset.rules.copy()
            new_rules.remove(self.target_rule)
            self.ruleset.update_w_rules(
                    "rules", new_rules.copy(), self.initiated_by,
                    self.with_ability, "normal", self)
            new_rules.remove(self)
            self.ruleset.update_w_rules(
                    "rules", new_rules.copy(), self.initiated_by,
                    self.with_ability, "normal", self)
