import random

import battlelib

class MetaSlap(battlelib.MetaAbility):
    ability_name = "Slap"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        pass


class Slap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Slap", tags=[])

    def linear_variate(self):
        self.damage_multiplier = random.random() * .5 + .75
        pass

    def can_be_used_on(self, target):
        if self.owner.leader.ap >= 3:
            return True
        return False

    def use_with_effectiveness(self, targets, battle, effectiveness):
        if effectiveness == "glancing":
            print(
                    f"{self.owner.unit_name} slaps "
                    f"{targets[0].unit_name}, but they've got the baby-"
                    "hands!")
            effectiveness_multiplier = .5
        elif effectiveness == "normal":
            print(
                    f"{self.owner.unit_name} slaps {targets[0].unit_name}!")
            effectiveness_multiplier = 1
        else:
            print(
                    f"{self.owner.unit_name} really slaps the taste out of "
                    f"{targets[0].unit_name}'s mouth!")
            effectiveness_multiplier = 2
        raw_damage = self.owner.aug_atk * self.damage_multiplier
        effectiveness_damage = raw_damage * effectiveness_multiplier
        total_damage = effectiveness_damage - targets[0].aug_def
        if filtered_damage < 0:
            total_damage = 0
        battle.update_w_rules(
                target=targets[0],
                attr_name="hp",
                new_value=targets[0].hp - total_damage,
                by_ability=self,
                at_effectiveness=effectiveness,
                triggering_rule=None)
        battle.update_w_rules(
                target=self.owner.leader,
                attr_name="ap",
                new_value=self.owner.leader.ap - 3,
                by_ability=self,
                at_effectiveness=effectiveness,
                triggering_rule=None)


class DoubleSlap(Slap):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Double Slap", tags=[])

    def use_with_effectiveness(self, targets, battle, effectiveness):
        if effectiveness == "glancing":
            print(
                    f"{self.owner.unit_name} slaps "
                    f"{targets[0].unit_name}, but they've got the baby-"
                    "hands!")
            effectiveness_multiplier = .5
        elif effectiveness == "normal":
            print(
                    f"{self.owner.unit_name} slaps {targets[0].unit_name}!")
            effectiveness_multiplier = 1
        else:
            print(
                    f"{self.owner.unit_name} really slaps the taste out of "
                    f"{targets[0].unit_name}'s mouth!")
            effectiveness_multiplier = 2
        raw_damage = self.owner.aug_atk * self.damage_multiplier
        effectiveness_damage = raw_damage * effectiveness_multiplier
        total_damage = effectiveness_damage - targets[0].aug_def
        if filtered_damage < 0:
            total_damage = 0
        battle.update_w_rules(
                target=targets[0],
                attr_name="hp",
                new_value=targets[0].hp - total_damage,
                by_ability=self,
                at_effectiveness=effectiveness,
                triggering_rule=None)
        battle.update_w_rules(
                target=self.owner.leader,
                attr_name="ap",
                new_value=self.owner.leader.ap - 3,
                by_ability=self,
                at_effectiveness=effectiveness,
                triggering_rule=None)


class DickSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Dick Slap", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_with_effectiveness(self, targets, battle, effectiveness):
        print("This ability isn't designed, yet!")


