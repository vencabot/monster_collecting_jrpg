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

class DynamicAttribute:
    def __init__(self, owner, attr_name, value):
        self.owner = owner
        self.attr_name = attr_name
        self.value = value

    def update(self, new_value, perpetrated_by):
        old_value = self.value
        dynamic_event = DynamicEvent(
                self.owner, self.attr_name, new_value, old_value,
                perpetrated_by)
        print(f"DIAGNOSTIC: Proposed value change to {new_value}.")
        if new_value == old_value:
            return
        rules = self.owner.party.battle.dynamic_rules
        for dynamic_rule in rules["before"]:
            dynamic_rule.check(dynamic_event)
            while dynamic_event.replaced_by is not None:
                dynamic_event = dynamic_event.replaced_by
        final_value = dynamic_event.new_value
        print(
                f"DIAGNOSTIC: {self.owner.unit_name}'s {self.attr_name} "
                f"changed from {self.value} to {final_value}.")
        self.value = final_value
        for dynamic_rule in rules["after"]:
            dynamic_rule.check(dynamic_event)


class UnitAbility:
    def __init__(self, ability_name, owner):
        self.ability_name = ability_name
        self.owner = owner

    def use(self, targets):
        pass


class Slap(UnitAbility):
    def __init__(self, owner):
        super().__init__("Slap", owner)

    def use(self, targets):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 2, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)


class BattleUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.hp = DynamicAttribute(self, "hp", 10)
        self.atk = DynamicAttribute(self, "atk", 5)
        self.mp = DynamicAttribute(self, "mp", 5)
        self.abilities = {}
        self.party = None

    def learn_ability(self, ability_class):
        new_ability = ability_class(self)
        if new_ability.ability_name not in self.abilities:
            self.abilities[new_ability.ability_name] = []
        self.abilities[new_ability.ability_name].append(new_ability)


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
        self.dynamic_rules = {"before": [], "after": []}

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self

    def append_rule(self, rule):
        self.dynamic_rules[rule.check_phase].append(rule)


class DynamicRule:
    def __init__(
            self, rule_name, check_phase, event_not_prevented=True,
            event_prevented=False):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self._recurrence_limit = 1
        self.check_phase = check_phase

    def check(self, dynamic_event):
        if self.recurrence_counter >= self._recurrence_limit:
            self._at_limit(dynamic_event)
            return False
        elif self._check(dynamic_event):
            self.recurrence_counter += 1
            self._trigger(dynamic_event)
            return True

    def _check(self, dynamic_event):
        return False

    def _trigger(self, dynamic_event):
        pass

    def _at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def _fail(self, dynamic_event):
        print(f"{self.rule_name} failed to trigger.")
