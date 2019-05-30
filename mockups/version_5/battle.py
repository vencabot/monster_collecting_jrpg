import random

class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value, by_ability,
            at_effectiveness, triggering_rule, timeline=None):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.by_ability = by_ability
        self.at_effectiveness = at_effectiveness
        self.triggering_rule = triggering_rule
        self.timeline = [self] if timeline is None else timeline

    def replace_value(self, new_value, triggering_rule):
        new_event = DynamicEvent(
                self.target, self.attr_name, new_value, self.old_value,
                self.by_ability, self.at_effectiveness, triggering_rule)
        self.timeline.append(new_event)


class DynamicObject:
    def __init__(self, ruleset):
        self.ruleset = ruleset
        
    def update_w_rules(
            self, attr_name, new_value, by_ability, at_effectiveness,
            triggering_rule=None):
        old_value = self.__dict__[attr_name]

        if isinstance(self, Unit):
            owner_name = self.unit_name
        elif isinstance(self, Leader):
            owner_name = self.leader_name
        elif isinstance(self, DynamicRule):
            owner_name = self.rule_name
        print(
                f"DIAGNOSTIC: Before the event, {owner_name}'s {attr_name} "
                f"is {old_value}.")
        dynamic_event = DynamicEvent(
                self, attr_name, new_value, old_value, by_ability,
                at_effectiveness, triggering_rule)
        self.run_through_before_rules(dynamic_event)
        self.__dict__[attr_name] = dynamic_event.timeline[-1].new_value
        self.run_through_after_rules(dynamic_event.timeline[-1])
        print(
                f"DIAGNOSTIC: After the event, {owner_name}'s {attr_name} "
                f"is {self.__dict__[attr_name]}.")
        print()

    def run_through_before_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.before_rules:
            dynamic_rule.react_to(dynamic_event)
            dynamic_event = dynamic_event.timeline[-1]

    def run_through_after_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.after_rules:
            dynamic_rule.react_to(dynamic_event)


class DynamicRule(DynamicObject):
    def __init__(
            self, ruleset, rule_name, check_phase, tags, severity,
            from_ability, from_effectiveness, from_targets):
        super().__init__(ruleset)
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self.recurrence_limit = 1
        self.check_phase = check_phase
        self.tags = tags
        self.severity = severity
        self.from_ability = from_ability
        self.from_effectiveness = from_effectiveness
        self.from_targets = from_targets
        self.triggered_counter = 0

    def react_to(self, dynamic_event):
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event)
        elif self.will_trigger_on(dynamic_event):
            self.recurrence_counter += 1
            self.trigger(dynamic_event)
            self.update_w_rules(
                    "triggered_counter", self.triggered_counter + 1,
                    dynamic_event.by_ability,
                    dynamic_event.at_effectiveness,
                    dynamic_event.triggering_rule)
        else:
            self.fail(dynamic_event)

    def will_trigger_on(self, dynamic_event):
        return False

    def trigger(self, dynamic_event):
        pass

    def at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def fail(self, dynamic_event):
        #print(f"{self.rule_name} failed to trigger.")
        pass


class RuleSet(DynamicObject):
    def __init__(self, before_rules=[], after_rules=[]):
        super().__init__(self)
        self.before_rules = before_rules
        self.after_rules = after_rules

    def reset_recurrence_counters(self):
        for dynamic_rule in self.before_rules + self.after_rules:
            dynamic_rule.recurrence_counter = 0
        print("DIAGNOSTIC: dynamic recurrence counters have been reset")


class Leader(DynamicObject):
    def __init__(self, ruleset, leader_name):
        super().__init__(ruleset)
        self.leader_name = leader_name
        self.party = []
        self.point_unit = None
        self.max_ap = 10
        self.ap = self.max_ap


class Unit(DynamicObject):
    def __init__(self, ruleset, unit_name, leader):
        super().__init__(ruleset)
        self.unit_name = unit_name
        self.leader = leader
        self.hp = 10
        self.atk = 5
        self.mp = 5
        self.abilities = []


class UnitAbility(DynamicObject):
    def __init__(self, ruleset, ability_name, owner):
        super().__init__(ruleset)
        self.ability_name = ability_name
        self.owner = owner

    def use_on(self, targets):
        if not self.can_be_used_on(targets):
            return
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_list = [
            self.use_glancing, self.use_normal, self.use_critical]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        use_callables = random.choices(
                effectiveness_list, effectiveness_weights)
        if use_callables[0] == self.use_glancing:
            print(f"DIAGNOSTIC: {self.ability_name} was glancing.")
        elif use_callables[0] == self.use_critical:
            print(f"DIAGNOSTIC: {self.ability_name} was critical.")
        use_callables[0](targets)
        self.ruleset.reset_recurrence_counters()

    def can_be_used_on(self, targets):
        return True

    def use_glancing(self, targets):
        self.use_normal(targets)

    def use_normal(self, targets):
        pass

    def use_critical(self, targets):
        self.use_normal(targets)


class RelationshipHelper:
    pass
