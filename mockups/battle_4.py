import random

import dynamic_system_4

class Battle:
    def __init__(self):
        self.parties = []
        self.rule_phases = {"before": [], "after": []}
        self.active_party = dynamic_system_4.DynamicAttribute(
                self, "active_party", None)

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self

    def append_rule(self, rule):
        self.dynamic_rules[rule.check_phase].append(rule)

    def reset_dynamic_recurrence(self):
        rules = (
                self.dynamic_rules["before"]
                + self.dynamic_rules["after"])
        for dynamic_rule in rules:
            dynamic_rule.recurrence_counter = 0
        print("DIAGNOSTIC: dynamic recurrence counters have been reset")

    def next_turn(self):
        # This will only work if we're limited to two parties per battle.
        for party in self.parties:
            if party is not self.active_party.value:
                self.active_party.value.leader.ap.update(
                    self.active_party.value.leader.max_ap.value, self)
                self.active_party.update(party, self.active_party.value)
                break


class BattleParty:
    def __init__(self, party_name):
        self.party_name = party_name
        self.units = []
        self.leader = None
        self.point_unit = dynamic_system_4.DynamicAttribute(
                self, "point_unit", None)
        self.battle = None

    def append_unit(self, party_unit):
        self.units.append(party_unit)
        party_unit.party = self

    def append_leader(self, party_leader):
        self.leader = party_leader
        party_leader.party = self


class BattleLeader:
    def __init__(self, leader_name):
        self.leader_name = leader_name
        self.party = None
        self.max_ap = dynamic_system_4.DynamicAttribute(
                self, "max_ap", 10)
        self.ap = dynamic_system_4.DynamicAttribute(
                self, "ap", self.max_ap.value)


class BattleUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.hp = dynamic_system_4.DynamicAttribute(self, "hp", 10)
        self.atk = dynamic_system_4.DynamicAttribute(self, "atk", 5)
        self.mp = dynamic_system_4.DynamicAttribute(self, "mp", 5)
        self.abilities = {}
        self.party = None

    def learn_ability(self, ability_class):
        new_ability = ability_class(self)
        if new_ability.ability_name not in self.abilities:
            self.abilities[new_ability.ability_name] = []
        self.abilities[new_ability.ability_name].append(new_ability)


class UnitAbility:
    def __init__(self, ability_name, owner):
        self.ability_name = ability_name
        self.owner = owner

    def use(self, targets):
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_list = [
            self._use_glancing, self._use_normal, self._use_critical]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        use_callables = random.choices(
                effectiveness_list, effectiveness_weights)
        if use_callables[0] == self._use_glancing:
            print(f"DIAGNOSTIC: {self.ability_name} was glancing.")
        elif use_callables[0] == self._use_critical:
            print(f"DIAGNOSTIC: {self.ability_name} was critical.")
        use_callables[0](targets)
        self.owner.party.battle.reset_dynamic_recurrence()
        
    def _use_glancing(self, targets):
        self._use_normal(targets)

    def _use_normal(self, targets):
        pass

    def _use_critical(self, targets):
        self._use_normal(targets)
