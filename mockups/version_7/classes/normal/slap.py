import random

import battlelib

class Slap(battlelib.MetaAbility):
    ability_name = "Slap"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        pass


class OpenPalmSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(
                owner=owner, ability_name="Open-Palm Slap", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_glancing(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)

    def use_normal(self, targets, battle):
        print("This ability isn't designed, yet!")

    def use_critical(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)


class SystemShock(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner=owner, ability_name="System Shock", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_glancing(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)

    def use_normal(self, targets, battle):
        print("This ability isn't designed, yet!")

    def use_critical(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)


class LightningShock(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(
                owner=owner, ability_name="Lightning Shock", tags=[])

    def linear_variate(self):
        pass

    def can_be_used_on(self, target):
        return True

    def use_glancing(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)

    def use_normal(self, targets, battle):
        print("This ability isn't designed, yet!")

    def use_critical(self, targets, battle):
        self.use_normal(targets=targets, battle=battle)

    def calculate_damage(self, targets, battle, effectiveness):


