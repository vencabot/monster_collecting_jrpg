import battle

class Slap(battle.UnitAbility):
    def __init__(self, owner):
        super().__init__("Slap", owner)

    def can_be_used_on(self, target):
        if self.owner.mp >= 2:
            return True
        return False

    def deal_some_damage(self, target, damage, effectiveness, battle):
        battle.update_w_rules(
                target, "hp", target.hp - damage, self, effectiveness)
        battle.update_w_rules(
                self.owner, "mp", self.owner.mp - 2, self, effectiveness)
        battle.update_w_rules(
                self.owner.leader, "ap", self.owner.leader.ap - 2, self,
                effectiveness)

    def use_glancing(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        print(f"But {self.owner.unit_name}'s got the baby-hands! T_T")
        self.deal_some_damage(targets[0], 1, "glancing", battle)

    def use_normal(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        self.deal_some_damage(targets[0], 2, "normal", battle)

    def use_critical(self, targets, battle):
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        print(f"{self.owner.unit_name} really put their weight into it!")
        self.deal_some_damage(targets[0], 4, "critical", battle)

