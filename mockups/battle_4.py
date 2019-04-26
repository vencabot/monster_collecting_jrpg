import random

class DynamicObject:
    def __init__(self, ruleset):
        self.ruleset = ruleset
        
    def update_w_rules(
            self, attr_name, new_value, perpetrated_by=None,
            w_ability=None, w_rule=None):
        old_value = self.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                self, attr_name, new_value, old_value, perpetrated_by,
                w_ability, w_rule)
        if new_value == old_value:
            return
        final_event = self.ruleset.run_through_before_phase(
                dynamic_event)
        self.__dict__[attr_name] = final_event.new_value
        self.ruleset.run_after_phase_for(final_event)


class DynamicRule:
    def __init__(self, rule_name, check_phase, initiator, w_ability):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self.recurrence_limit = 1
        self.check_phase = check_phase
        self.initiator = initiator
        self.w_ability = w_ability

    def react_to(self, dynamic_event):
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event)
        elif self.will_trigger_on(dynamic_event):
            self.recurrence_counter += 1
            self.trigger(dynamic_event)

    def will_trigger_on(self, dynamic_event):
        return False

    def trigger(self, dynamic_event):
        pass

    def at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def fail(self, dynamic_event):
        print(f"{self.rule_name} failed to trigger.")


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

# FIX THIS TODAY
class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value,
            perpetrated_by, w_ability=None, w_rule=None, replaces=None):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.perpetrated_by = perpetrated_by
        self.w_ability = w_ability
        self.w_rule = w_rule
        self.replaces = replaces
        self.replaced_by = None

    def replace_value(self, new_value, perpetrated_by):
        self.replaced_by = DynamicEvent(
                self.target, self.attr_name, new_value, self.old_value,
                perpetrated_by, self.ability, self)

    def get_original_event(self):
        original_event = self
        while original_event.replaces is not None:
            original_event = original_event.replaces
        return original_event

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

    def use(self, ability_class, targets, battle):
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
