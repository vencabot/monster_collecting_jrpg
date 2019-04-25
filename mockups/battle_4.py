import random

import dynamic_system_4

class Battle:
    def __init__(self):
        self.ruleset = dynamic_system_4.Ruleset()


class BattleLeader(dynamic_system_4.DynamicObject):
    def __init__(self, ruleset, leader_name):
        super().__init__(ruleset)
        self.leader_name = leader_name
        self.party = []
        self.max_ap = 10
        self.ap = self.max_ap


class BattleUnit(dynamic_system_4.DynamicObject):
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
