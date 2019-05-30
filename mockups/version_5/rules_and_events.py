import battle

class Slap(battle.UnitAbility):
    def __init__(self, ruleset, owner):
        super().__init__(ruleset, "Slap", owner)

    def can_be_used_on(self, target):
        if self.owner.mp >= 2:
            return True
        return False

    def deal_some_damage(self, target, damage, effectiveness):
        print(f"{self.owner.unit_name} slapped {target.unit_name}!")
        target.update_w_rules("hp", target.hp - damage, self, effectiveness)
        self.owner.update_w_rules(
                "mp", self.owner.mp - 2, self, effectiveness)
        self.owner.leader.update_w_rules(
                "ap", self.owner.leader.ap - 2, self, effectiveness)

    def use_glancing(self, targets):
        self.deal_some_damage(targets[0], 1, "glancing")

    def use_normal(self, targets):
        self.deal_some_damage(targets[0], 2, "normal")

    def use_critical(self, targets):
        self.deal_some_damage(targets[0], 4, "critical")


class Rage(battle.DynamicRule):
    def __init__(self, ruleset, severity, target_unit):
        super().__init__(
                ruleset, "Rage", "after", ["attack_increase"], severity,
                None, None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        if self.severity < 3:
            attack_boost = 1
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting peeved!")
        elif self.severity < 8:
            attack_boost = 2
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting angry!")
        else:
            attack_boost = 3
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting mighty "
                    "pissed off!")
        print(trigger_message)
        self.target_unit.update_w_rules(
            "atk", self.target_unit.atk + attack_boost,
            dynamic_event.by_ability, dynamic_event.at_effectiveness, self)


ruleset = battle.RuleSet()

a_leader = battle.Leader(ruleset, "Tosmith84")
a_unit1 = battle.Unit(ruleset, "signopt200", a_leader)
a_unit1.abilities.append(Slap(ruleset, a_unit1))
a_unit2 = battle.Unit(ruleset, "rageagstthearcademachine", a_leader)
a_unit2.abilities.append(Slap(ruleset, a_unit2))
a_unit3 = battle.Unit(ruleset, "KReichJr", a_leader)
a_unit3.abilities.append(Slap(ruleset, a_unit3))
a_leader.party = [a_unit1, a_unit2, a_unit3]
a_leader.point_unit = a_unit1

b_leader = battle.Leader(ruleset, "dixxucker")
b_unit1 = battle.Unit(ruleset, "goodvibecity", b_leader)
b_unit1.abilities.append(Slap(ruleset, b_unit1))
b_unit2 = battle.Unit(ruleset, "Zanzhu", b_leader)
b_unit2.abilities.append(Slap(ruleset, b_unit2))
b_unit3 = battle.Unit(ruleset, "NydusTemplar", b_leader)
b_unit3.abilities.append(Slap(ruleset, b_unit3))
b_leader.party = [b_unit1, b_unit2, b_unit3]
b_leader.point_unit = b_unit1

ruleset.after_rules.append(Rage(ruleset, 8, a_unit1))
b_unit1.abilities[0].use_on([a_unit1])
