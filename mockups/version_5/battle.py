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


class DynamicRule:
    def __init__(
            self, rule_name, check_phase, tags, severity, from_ability,
            from_effectiveness, from_targets):
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

    def react_to(self, dynamic_event, battle):
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event)
        elif self.will_trigger_on(dynamic_event, battle):
            self.recurrence_counter += 1
            self.trigger(dynamic_event, battle)
            battle.update_w_rules(
                    self, "triggered_counter", self.triggered_counter + 1,
                    dynamic_event.by_ability,
                    dynamic_event.at_effectiveness,
                    dynamic_event.triggering_rule)
        else:
            self.fail(dynamic_event)

    def will_trigger_on(self, dynamic_event, battle):
        return False

    def trigger(self, dynamic_event, battle):
        pass

    def at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def fail(self, dynamic_event):
        #print(f"{self.rule_name} failed to trigger.")
        pass


class RuleSet:
    def __init__(self, before_rules=[], after_rules=[]):
        self.before_rules = before_rules
        self.after_rules = after_rules

    def reset_recurrence_counters(self):
        for dynamic_rule in self.before_rules + self.after_rules:
            dynamic_rule.recurrence_counter = 0


class Battle:
    def __init__(self):
        self.ruleset = RuleSet()
        
    def update_w_rules(
            self, target, attr_name, new_value, by_ability,
            at_effectiveness, triggering_rule=None):
        old_value = target.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                target, attr_name, new_value, old_value, by_ability,
                at_effectiveness, triggering_rule)
        self.run_through_before_rules(dynamic_event)
        target.__dict__[attr_name] = dynamic_event.timeline[-1].new_value
        self.run_through_after_rules(dynamic_event.timeline[-1])

    def run_through_before_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.before_rules:
            dynamic_rule.react_to(dynamic_event, self)
            dynamic_event = dynamic_event.timeline[-1]

    def run_through_after_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.after_rules:
            dynamic_rule.react_to(dynamic_event, self)


class Leader:
    def __init__(self, leader_name):
        self.leader_name = leader_name
        self.party = []
        self.point_unit = None
        self.max_ap = 10
        self.ap = self.max_ap


class Unit:
    def __init__(self, unit_name, leader):
        self.unit_name = unit_name
        self.leader = leader
        self.hp = 10
        self.atk = 5
        self.mp = 5
        self.abilities = []


class UnitAbility:
    def __init__(self, owner, ability_name="Ability"):
        self.ability_name = ability_name
        self.owner = owner
        self.effectiveness_methods = [
                self.use_glancing, self.use_normal, self.use_critical]

    def use_on(self, targets, battle):
        if not self.can_be_used_on(targets):
            print(
                    f"DIAGNOSTIC: {self.ability_name} cannot be used this "
                    "way.")
            return
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        use_callables = random.choices(
                self.effectiveness_methods, effectiveness_weights)
        use_callables[0](targets, battle)
        battle.ruleset.reset_recurrence_counters()

    def can_be_used_on(self, targets):
        return True

    def use_glancing(self, targets, battle):
        self.use_normal(targets, battle)

    def use_normal(self, targets, battle):
        pass

    def use_critical(self, targets, battle):
        self.use_normal(targets, battle)


class RelationshipHelper:
    @classmethod
    def create_unit_for(cls, leader, unit_name):
        leader.party.append(Unit(unit_name, leader))

    @classmethod
    def create_ability_for(cls, unit, ability_class):
        unit.abilities.append(ability_class(unit))
