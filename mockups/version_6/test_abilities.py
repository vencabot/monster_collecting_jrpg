import random
import math

import battlelib

class Slap(battlelib.MetaAbility):
    ability_name = "Slap"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        return NormalSlap(unit_class.owner)

class NormalSlap(battlelib.UnitAbility):
    def __init__(self, owner):
        super().__init__(owner, "Slap")
        self.damage_multiplier = 1.5 * random.random() + 0.5
        self.mp_cost = random.randint(1, 3) 
        self.ap_cost = random.randint(1, 3)
        print("DIAGNOSTIC: NEW SLAP")
        print(f"    damage_multiplier: {self.damage_multiplier}")
        print(f"    mp_cost: {self.mp_cost}")
        print(f"    ap_cost: {self.ap_cost}")

    def can_be_used_on(self, target):
        if self.owner.cur_mp >= 2:
            return True
        return False

    def deal_some_damage(self, target, damage, effectiveness, battle):
        battle.update_w_rules(
                target, "cur_hp", target.cur_hp - damage, self,
                effectiveness)
        battle.update_w_rules(
                self.owner, "cur_mp", self.owner.cur_mp - self.mp_cost,
                self, effectiveness)
        battle.update_w_rules(
                self.owner.leader, "ap",
                self.owner.leader.ap - self.ap_cost, self, effectiveness)

    def use_glancing(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        print(f"But {self.owner.unit_name}'s got the baby-hands! T_T")
        base_damage = self.owner.aug_atk * self.damage_multiplier
        real_damage = round(base_damage * 0.5)
        self.deal_some_damage(targets[0], real_damage, "glancing", battle)

    def use_normal(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        base_damage = self.owner.aug_atk * self.damage_multiplier
        real_damage = round(base_damage)
        self.deal_some_damage(targets[0], real_damage, "normal", battle)

    def use_critical(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        print(f"{self.owner.unit_name} really put their weight into it!")
        base_damage = self.owner.aug_atk * self.damage_multiplier
        real_damage = round(base_damage * 2)
        self.deal_some_damage(targets[0], real_damage, "critical", battle)

