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

