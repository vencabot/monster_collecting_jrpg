import battle_4

class DynamicObject:
    def __init__(self, ruleset):
        self.ruleset = ruleset
        
    def update_w_rules(self, attr_name, new_value, perpetrated_by):
        old_value = self.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                self, attr_name, new_value, old_value, perpetrated_by)
        if new_value == old_value:
            return
        final_event = self.ruleset.run_through_before_phase(
                dynamic_event)
        self.__dict__[attr_name] = final_event.new_value
        self.ruleset.run_after_phase_for(final_event)


class DynamicRule:
    def __init__(self, rule_name, check_phase):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self.recurrence_limit = 1
        self.check_phase = check_phase

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
        for dynamic_rule in self.after:
            dynamic_rule.react_to(dynamic_event)

    def reset_recurrence_counters(self):
        for dynamic_rule in self.rules:
            dynamic_rule.recurrence_counter = 0
        print("DIAGNOSTIC: dynamic recurrence counters have been reset")



class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value,
            perpetrated_by, replaces=None):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.perpetrated_by = perpetrated_by
        self.replaces = replaces
        self.replaced_by = None

    def replace_value(self, new_value, perpetrated_by):
        self.replaced_by = DynamicEvent(
                self.target, self.attr_name, new_value, self.old_value,
                perpetrated_by, self)

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
