import battle_4

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


class DynamicObject:
    def __setattr__(self, name, new_value

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
        #print(f"DIAGNOSTIC: Proposed value change to {new_value}.")
        if new_value == old_value:
            return
        if isinstance(self.owner, battle_4.BattleUnit):
            battle = self.owner.party.battle
            owner_name = self.owner.unit_name
        elif isinstance(self.owner, battle_4.BattleParty):
            battle = self.owner.battle
            owner_name = f"{self.owner.leader.leader_name}'s party"
        elif isinstance(self.owner, battle_4.BattleLeader):
            battle = self.owner.party.battle
            owner_name = self.owner.leader_name
        elif isinstance(self.owner, battle_4.Battle):
            battle = self.owner
            owner_name = "da battle"
        rules = battle.dynamic_rules
        for dynamic_rule in rules["before"]:
            dynamic_rule.check(dynamic_event)
            while dynamic_event.replaced_by is not None:
                dynamic_event = dynamic_event.replaced_by
        final_value = dynamic_event.new_value
        print(
                f"DIAGNOSTIC: {owner_name}'s {self.attr_name} changed "
                f"from {self.value} to {final_value}.")
        self.value = final_value
        for dynamic_rule in rules["after"]:
            dynamic_rule.check(dynamic_event)


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
