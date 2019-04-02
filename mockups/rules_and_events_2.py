import dynamic_system

class Invincible(dynamic_system.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Invincible", "preemption")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if (
                not dynamic_event.prevented
                and dynamic_event.target is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        dynamic_event.prevented = True
        print(
                f"{dynamic_event.perpetrator.unit_name}'s attack "
                f"failed! {self.target_unit.unit_name} is protected by "
                "Invincible!")


class Rage(dynamic_system.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Rage", "reaction")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} got pissed off and "
                "became more powerful.")
        self.target_unit.atk.update(self.target_unit.atk.value + 1, self)


class Hench(dynamic_system.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Hench", "preemption")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if(
                dynamic_event.perpetrator is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"Look out, {dynamic_event.target.unit_name}! "
                f"{self.target_unit.unit_name} is Hench'd out!")
        if not dynamic_event.prevented:
            dynamic_event.prevented = True
            damage = dynamic_event.old_value - dynamic_event.new_value
            new_hp_value = dynamic_event.old_value - damage * 2
            dynamic_event.target.hp.update(
                    new_hp_value, dynamic_event.perpetrator)

    def _fail(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} failed to do damage, so "
                "no Hench for them!")


class ExtraDamage(dynamic_system.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Extra Damage", "preemption")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if(
                dynamic_event.perpetrator is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} gets extra damage!")
        if not dynamic_event.prevented:
            dynamic_event.prevented = True
            damage = dynamic_event.old_value - dynamic_event.new_value
            new_hp_value = dynamic_event.old_value - damage - 1
            dynamic_event.target.hp.update(
                    new_hp_value, dynamic_event.perpetrator)


class BloodLust(dynamic_system.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Bloodlust", "reaction")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if(
                dynamic_event.perpetrator is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} loves to attack! Blood "
                "Lust! Their ATK increased!")
        self.target_unit.atk.update(self.target_unit.atk.value + 1, self)


if __name__ == "__main__":
    party_a = dynamic_system.BattleParty("party_a")
    party_b = dynamic_system.BattleParty("party_b")
    vencabot = dynamic_system.BattleUnit("Vencabot")
    goodvibe = dynamic_system.BattleUnit("GoodVibe")
    our_battle = dynamic_system.Battle()

    party_a.append_unit(vencabot)
    party_b.append_unit(goodvibe)
    our_battle.append_party(party_a)
    our_battle.append_party(party_b)
    our_battle.append_rule(BloodLust(goodvibe))
    our_battle.append_rule(Invincible(vencabot))
    our_battle.append_rule(ExtraDamage(goodvibe))
    our_battle.append_rule(Hench(goodvibe))
    our_battle.append_rule(Rage(vencabot))
    print(f"Before the slap, Vencabot has {vencabot.hp.value} HP.")
    goodvibe.slap(vencabot)
    print(f"After the slap, Vencabot has {vencabot.hp.value} HP.")
