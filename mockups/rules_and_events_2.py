def limited_recurrence(rule_check):
    def limited_method(
            self, target, attr_name, new_value, old_value, updater):
        if self.recurrence_counter < self._recurrence_limit:
            if rule_check(
                    self, target, attr_name, new_value, old_value,
                    updater):
                self.recurrence_counter += 1
                self._trigger(
                    target, attr_name, new_value, old_value, updater)
                return True
            return False
    return limited_method

class DynamicAttribute:
    def __init__(self, owner, attr_name, value):
        self.owner = owner
        self.attr_name = attr_name
        self.value = value

    def update(self, new_value, updater):
        old_value = self.value
        event_tuple = (
                self.owner, self.attr_name, new_value, old_value,
                updater)
        if new_value == old_value:
            return
        for dynamic_rule in self.owner.party.battle.dynamic_rules:
            if dynamic_rule.on_preemption(*event_tuple):
                prevented = True
                break
        else:
            prevented = False
        if prevented:
            for dynamic_rule in self.owner.party.battle.dynamic_rules:
                # It doesn't matter if this was triggered or not.
                # You can never prevent a prevention.
                dynamic_rule.on_prevented(*event_tuple)
            return
        self.value = new_value
        for dynamic_rule in self.owner.party.battle.dynamic_rules:
            dynamic_rule.on_reaction(*event_tuple)


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
    def on_preemption(
            self, target, attr_name, new_value, old_value, updater):
        return self._preemption_check(
                target, attr_name, new_value, old_value, updater)

    @limited_recurrence
    def on_prevented(
            self, target, attr_name, new_value, old_value, updater):
        return self._prevented_check(
                target, attr_name, new_value, old_value, updater)

    @limited_recurrence
    def on_reaction(
            self, target, attr_name, new_value, old_value, updater):
        return self._reaction_check(
                target, attr_name, new_value, old_value, updater)

    def _preemption_check(
            self, target, attr_name, new_value, old_value, updater):
        return False

    def _prevented_check(
            self, target, attr_name, new_value, old_value, updater):
        return False

    def _reaction_check(
            self, target, attr_name, new_value, old_value, updater):
        return False

    def _trigger(
            self, target, attr_name, new_value, old_value, updater):
        pass


class Invincible(DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Invincible")
        self.target_unit = target_unit

    def _preemption_check(
            self, target, attr_name, new_value, old_value, updater):
        if (
                target is self.target_unit
                and attr_name is "hp"
                and new_value < old_value):
            return True
        return False

    def _trigger(
            self, target, attr_name, new_value, old_value, updater):
        print(
                f"{updater.unit_name}'s attack failed! "
                f"{target.unit_name} is protected by Invincible!")


class Rage(DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Rage")
        self.target_unit = target_unit

    def _reaction_check(
            self, target, attr_name, new_value, old_value, updater):
        if (
                target is self.target_unit
                and attr_name is "hp"
                and new_value < old_value):
            return True
        return False

    def _trigger(
            self, target, attr_name, new_value, old_value, updater):
        print(
                f"{target.unit_name} got pissed off and became more "
                "powerful.")


class Hench(DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Hench")
        self.target_unit = target_unit

    def _preemption_check(
            self, target, attr_name, new_value, old_value, updater):
        if(
                updater is self.target_unit
                and attr_name is "hp"
                and new_value < old_value):
            return True
        return False

    def _trigger(
            self, target, attr_name, new_value, old_value, updater):
        print(
                f"Look out, {target.unit_name}! {updater.unit_name} "
                "is Hench'd out!")
        damage = old_value - new_value
        target.hp.update(old_value - damage * 2, updater)


if __name__ == "__main__":
    party_a = BattleParty("party_a")
    party_b = BattleParty("party_b")
    vencabot = BattleUnit("Vencabot")
    goodvibe = BattleUnit("GoodVibe")
    party_a.append_unit(vencabot)
    party_b.append_unit(goodvibe)
    our_battle = Battle()
    our_battle.append_party(party_a)
    our_battle.append_party(party_b)
    our_battle.dynamic_rules.append(Hench(goodvibe))
#    our_battle.dynamic_rules.append(Invincible(vencabot))
    our_battle.dynamic_rules.append(Rage(vencabot))
    print(f"Before the slap, Vencabot has {vencabot.hp.value} HP.")
    goodvibe.slap(vencabot)
    print(f"After the slap, Vencabot has {vencabot.hp.value} HP.")
