import random

import battlelib

class MetaSlap(battlelib.MetaAbility):
    ability_name = "Slap"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        pass


class DireSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Slap", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

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
        damage = self.owner.aug_atk * effectiveness_multiplier
        battle.update_w_rules(
                target=targets[0],
                attr_name="hp",
                new_value=targets[0].hp - damage,
                by_ability=self,
                at_effectiveness=effectiveness,
                triggering_rule=None)
        battle.update_w_rules(
                target=self.owner.leader,
                attr_name="ap",
                new_value=self.owner.leader.ap - 


class DoubleSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Double Slap", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_with_effectiveness(self, targets, battle, effectiveness):
        print("This ability isn't designed, yet!")


class DickSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="Dick Slap", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_with_effectiveness(self, targets, battle, effectiveness):
        print("This ability isn't designed, yet!")


