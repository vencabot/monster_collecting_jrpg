def limited_recurrence(rule_check):
    def limited_method(self, dynamic_event):
        if self.recurrence_counter < self._recurrence_limit:
            if rule_check(self, dynamic_event):
                self.recurrence_counter += 1
                self._trigger(dynamic_event)
                return True
            return False
    return limited_method

class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value, perpetrator):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.perpetrator = perpetrator
        self.prevented = False

class DynamicAttribute:
    def __init__(self, owner, attr_name, value):
        self.owner = owner
        self.attr_name = attr_name
        self.value = value

    def update(self, new_value, perpetrator):
        old_value = self.value
        dynamic_event = DynamicEvent(
                self.owner, self.attr_name, new_value, old_value,
                perpetrator)
        print(f"DIAGNOSTIC: Proposed value change to {new_value}.")
        if new_value == old_value:
            return
        for dynamic_rule in self.owner.party.battle.dynamic_rules:
            dynamic_rule.on_preemption(dynamic_event)
        if dynamic_event.prevented:
            for dynamic_rule in self.owner.party.battle.dynamic_rules:
                # It doesn't matter if this was triggered or not.
                # You can never prevent a prevention.
                dynamic_rule.on_prevented(dynamic_event)
            return
        self.value = new_value
        for dynamic_rule in self.owner.party.battle.dynamic_rules:
            dynamic_rule.on_reaction(dynamic_event)


class BattleUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.hp = DynamicAttribute(self, "hp", 10)
        self.atk = DynamicAttribute(self, "atk", 5)
        self.party = None

    def slap(self, target_unit):
        print(f"{self.unit_name} slapped {target_unit.unit_name}!")
        new_hp = target_unit.hp.value - 2
        target_unit.hp.update(new_hp, self)


class BattleParty:
    def __init__(self, party_name):
        self.party_name = party_name
        self.units = []
        self.battle = None

    def append_unit(self, party_unit):
        self.units.append(party_unit)
        party_unit.party = self


class Battle:
    def __init__(self):
        self.parties = []
        self.dynamic_rules = []

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self


class DynamicRule:
    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self._recurrence_limit = 1

    @limited_recurrence
    def on_preemption(self, dynamic_event):
        return self._preemption_check(dynamic_event)

    @limited_recurrence
    def on_prevented(self, dynamic_event):
        return self._prevented_check(dynamic_event)

    @limited_recurrence
    def on_reaction(self, dynamic_event):
        return self._reaction_check(dynamic_event)

    def _preemption_check(self, dynamic_event):
        return False

    def _prevented_check(self, dynamic_event):
        return False

    def _reaction_check(self, dynamic_event):
        return False

    def _trigger(self, dynamic_event):
        pass
