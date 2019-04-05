import dynamic_system_3

class Invincible(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Invincible", "before")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        dynamic_event.replace_value(self.target_unit.hp.value, self)
        original_event = dynamic_event.get_original_event()
        perpetrator = original_event.perpetrated_by
        if isinstance(perpetrator, dynamic_system_3.UnitAbility):
            attacker_name = perpetrator.owner.unit_name
        elif isinstance(perpetrator, dynamic_system_3.DynamicRule):
            attacker_name = perpetrator.rule_name
        print(
                f"{attacker_name}'s attack failed! "
                f"{self.target_unit.unit_name} is protected by "
                "Invincible!")


class Rage(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Rage", "after")
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


class Hench(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Hench", "before")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        if(
                original_event.perpetrated_by.owner is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"Look out, {dynamic_event.target.unit_name}! "
                f"{self.target_unit.unit_name} is Hench'd out!")
        old_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp_value = dynamic_event.old_value - old_damage * 2
        dynamic_event.replace_value(new_hp_value, self)

    def _fail(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} failed to do damage, so "
                "no Hench for them!")


class ExtraDamage(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Extra Damage", "before")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        if(
                original_event.perpetrated_by.owner is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} gets extra damage!")
        old_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp_value = dynamic_event.old_value - old_damage - 1
        dynamic_event.replace_value(new_hp_value, self)


class BloodLust(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Bloodlust", "after")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        perp_is_ability = isinstance(
                original_event.perpetrated_by,
                dynamic_system_3.UnitAbility)
        if (
                perp_is_ability
                and original_event.perpetrated_by.owner is self.target_unit
                and dynamic_event.attr_name is "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} loves to attack! Blood "
                "Lust! Their ATK increased!")
        self.target_unit.atk.update(self.target_unit.atk.value + 1, self)


class Persistence(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Persistence", "after")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        perp_is_ability = isinstance(
                original_event.perpetrated_by,
                dynamic_system_3.UnitAbility)
        if (
                perp_is_ability
                and original_event.perpetrated_by.owner is self.target_unit
                and dynamic_event.attr_name is "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} has Persistence! They're "
                "just gonna hit harder!")
        self.target_unit.atk.update(self.target_unit.atk.value + 1, self)


class MagicMan(dynamic_system_3.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Magic Man", "after")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name is "mp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} is a Magic Man! Their HP "
                "will be restored by the amount of MP they lost!")
        mp_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp = self.target_unit.hp.value + mp_damage
        self.target_unit.hp.update(new_hp, self)

if __name__ == "__main__":
    party_a = dynamic_system_3.BattleParty("party_a")
    party_b = dynamic_system_3.BattleParty("party_b")
    vencabot = dynamic_system_3.BattleUnit("Vencabot")
    goodvibe = dynamic_system_3.BattleUnit("GoodVibe")
    our_battle = dynamic_system_3.Battle()

    goodvibe.learn_ability(dynamic_system_3.Slap)

    party_a.append_unit(vencabot)
    party_b.append_unit(goodvibe)
    our_battle.append_party(party_a)
    our_battle.append_party(party_b)
    our_battle.append_rule(BloodLust(goodvibe))
    our_battle.append_rule(Hench(goodvibe))
    our_battle.append_rule(ExtraDamage(goodvibe))
    our_battle.append_rule(Rage(vencabot))
    our_battle.append_rule(Persistence(goodvibe))
    our_battle.append_rule(Invincible(vencabot))
    our_battle.append_rule(MagicMan(goodvibe))

    goodvibe.abilities["Slap"][0].use([vencabot])
