import random

class DynamicObject:
    def __init__(self, ruleset):
        self.ruleset = ruleset
        
    def update_w_rules(
            self, attr_name, new_value, perpetrated_by=None,
            with_ability=None, at_effectiveness=None, triggering_rule=None):
        old_value = self.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                self, attr_name, new_value, old_value, perpetrated_by,
                with_ability, at_effectiveness, triggering_rule)
        if new_value == old_value:
            return
        final_event = self.ruleset.run_through_before_phase(
                dynamic_event)
        self.__dict__[attr_name] = final_event.new_value
        self.ruleset.run_after_phase_for(final_event)


class DynamicRule(DynamicObject):
    def __init__(
            self, ruleset, rule_name, check_phase, tags, severity,
            initiated_by, with_ability):
        super().__init__(ruleset)
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self.recurrence_limit = 1
        self.check_phase = check_phase
        self.tags = tags
        self.severity = severity
        self.initiated_by = initiated_by
        self.with_ability = with_ability
        self.is_active = True
        self.triggered_counter = 0

    def get_description(self):
        return f"{self.rule_name}: A rule."

    def react_to(self, dynamic_event):
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event)
        elif self.will_trigger_on(dynamic_event):
            self.recurrence_counter += 1
            self.trigger(dynamic_event)
            self.update_w_rules(
                    "triggered_counter", self.triggered_counter + 1,
                    dynamic_event.perpetrated_by,
                    dynamic_event.with_ability,
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


class Ruleset(DynamicObject):
    def __init__(self, before_rules=[], after_rules=[]):
        super().__init__(self)
        self.rules = before_rules + after_rules

    def run_through_before_phase(self, dynamic_event):
        before_rules = []
        for dynamic_rule in self.rules:
            if dynamic_rule.check_phase == "before":
                before_rules.append(dynamic_rule)
        for dynamic_rule in before_rules:
            dynamic_rule.react_to(dynamic_event)
            dynamic_event = dynamic_event.get_newest_event()
        return dynamic_event

    def run_after_phase_for(self, dynamic_event):
        after_rules = []
        for dynamic_rule in self.rules:
            if dynamic_rule.check_phase == "after":
                after_rules.append(dynamic_rule)
        for dynamic_rule in after_rules:
            dynamic_rule.react_to(dynamic_event)

    def reset_recurrence_counters(self):
        for dynamic_rule in self.rules:
            dynamic_rule.recurrence_counter = 0
        print("DIAGNOSTIC: dynamic recurrence counters have been reset")

    def add_rule(self, dynamic_rule):
        self.update_w_rules("rules", self.rules + [dynamic_rule])

class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value,
            perpetrated_by, with_ability, at_effectiveness, triggering_rule,
            original_event=None, replaces=None):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.perpetrated_by = perpetrated_by
        self.with_ability = with_ability
        self.at_effectiveness = at_effectiveness
        self.triggering_rule = triggering_rule
        if original_event is not None:
            self.original_event = original_event
        else:
            self.original_event = self
        self.replaces = replaces
        self.replaced_by = None

    def replace_value(self, new_value, triggering_rule):
        self.replaced_by = DynamicEvent(
                self.target, self.attr_name, new_value, self.old_value,
                self.perpetrated_by, self.with_ability, triggering_rule,
                self.original_event, self)

    def get_newest_event(self):
        newest_event = self
        while newest_event.replaced_by is not None:
            newest_event = newest_event.replaced_by
        return newest_event


class Battle:
    def __init__(self):
        self.ruleset = Ruleset()
        self.leaders = []


class BattleLeader(DynamicObject):
    def __init__(self, ruleset, leader_name):
        super().__init__(ruleset)
        self.leader_name = leader_name
        self.party = []
        self.max_ap = 10
        self.ap = self.max_ap


class BattleUnit(DynamicObject):
    def __init__(self, ruleset, unit_name):
        super().__init__(ruleset)
        self.unit_name = unit_name
        self.hp = 10
        self.atk = 5
        self.mp = 5
        self.abilities = []

    def use_ability(self, ability_class, targets, battle):
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_list = [
            ability_class.use_glancing, ability_class.use_normal,
            ability_class.use_critical]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        use_callables = random.choices(
                effectiveness_list, effectiveness_weights)
        if use_callables[0] == ability_class.use_glancing:
            print(f"DIAGNOSTIC: {ability_class.ability_name} was glancing.")
        elif use_callables[0] == ability_class.use_critical:
            print(f"DIAGNOSTIC: {ability_class.ability_name} was critical.")
        use_callables[0](self, targets, battle)
        self.ruleset.reset_recurrence_counters()


class UnitAbility:
    abiilty_name = "generic ability"

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        cls.use_normal(perpetrator, targets, battle)

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        pass

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        cls.use_normal(perpetrator, targets, battle)
