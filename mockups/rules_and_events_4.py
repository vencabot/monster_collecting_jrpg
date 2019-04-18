import battle_4
import dynamic_system_4

class Invincible(dynamic_system_4.DynamicRule):
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
        if isinstance(perpetrator, battle_4.UnitAbility):
            attacker_name = perpetrator.owner.unit_name
        elif isinstance(perpetrator, dynamic_system_4.DynamicRule):
            attacker_name = perpetrator.rule_name
        print(
                f"{attacker_name}'s attack failed! "
                f"{self.target_unit.unit_name} is protected by "
                "Invincible!")


class Rage(dynamic_system_4.DynamicRule):
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


class Hench(dynamic_system_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Hench", "before")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        if (
                isinstance(original_event.perpetrated_by, battle_4.BattleUnit)
                and original_event.perpetrated_by.owner is self.target_unit
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


class ExtraDamage(dynamic_system_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Extra Damage", "before")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        if(
                isinstance(original_event.perpetrated_by, battle_4.BattleUnit)
                and original_event.perpetrated_by.owner is self.target_unit
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


class BloodLust(dynamic_system_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Bloodlust", "after")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        perp_is_ability = isinstance(
                original_event.perpetrated_by,
                battle_4.UnitAbility)
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


class Persistence(dynamic_system_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Persistence", "after")
        self.target_unit = target_unit

    def _check(self, dynamic_event):
        original_event = dynamic_event.get_original_event()
        perp_is_ability = isinstance(
                original_event.perpetrated_by,
                battle_4.UnitAbility)
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


class MagicMan(dynamic_system_4.DynamicRule):
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


class OldManGenes(dynamic_system_4.DynamicRule):
    def __init__(self, target_leader):
        super().__init__("Old Man Genes", "after")
        self.target_leader = target_leader
        self.is_active = False

    def _check(self, dynamic_event):
        if (
                not self.is_active
                and dynamic_event.target is self.target_leader
                and dynamic_event.attr_name is "ap"
                and dynamic_event.new_value < 5):
            return True
        return False

    def _trigger(self, dynamic_event):
        print(
                f"{self.target_leader.leader_name}'s whole party has "
                "the old man genes! They need a nap!")
        for battle_unit in self.target_leader.party.units:
            battle_unit.atk.update(battle_unit.atk.value * .7, self)
        self.is_active = True


class Slap(battle_4.UnitAbility):
    def __init__(self, owner):
        super().__init__("Slap", owner)

    def _use_glancing(self, targets):
        leader = self.owner.party.leader
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 1, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)
        leader.ap.update(leader.ap.value - 2, self)

    def _use_normal(self, targets):
        leader = self.owner.party.leader
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 2, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)
        leader.ap.update(leader.ap.value - 2, self)

    def _use_critical(self, targets):
        leader = self.owner.party.leader
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 4, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)
        leader.ap.update(leader.ap.value - 2, self)

if __name__ == "__main__":
    our_battle = battle_4.Battle()

    party_a = battle_4.BattleParty("party_a")
    our_battle.append_party(party_a)
    vencabot = battle_4.BattleLeader("Vencabot")
    kd_alpha = battle_4.BattleUnit("KD_Alpha")
    mexi = battle_4.BattleUnit("Mexi")
    party_a.append_leader(vencabot)
    party_a.append_unit(kd_alpha)
    party_a.append_unit(mexi)
    party_a.point_unit.update(kd_alpha, vencabot)

    party_b = battle_4.BattleParty("party_b")
    our_battle.append_party(party_b)
    kreichjr = battle_4.BattleLeader("KReichJr")
    goodvibe = battle_4.BattleUnit("GoodVibe")
    slade = battle_4.BattleUnit("zxxsladexxz")
    party_b.append_leader(kreichjr)
    party_b.append_unit(goodvibe)
    party_b.append_unit(slade)
    party_b.point_unit.update(goodvibe, kreichjr)
    goodvibe.learn_ability(Slap)

    our_battle.append_rule(BloodLust(goodvibe))
    our_battle.append_rule(Hench(goodvibe))
    our_battle.append_rule(ExtraDamage(goodvibe))
    our_battle.append_rule(Rage(kd_alpha))
    our_battle.append_rule(Persistence(goodvibe))
    our_battle.append_rule(Invincible(kd_alpha))
    our_battle.append_rule(MagicMan(goodvibe))
    our_battle.append_rule(OldManGenes(kreichjr))

    our_battle.active_party.update(party_a, our_battle)
    our_battle.next_turn()

    party_b.point_unit.value.abilities["Slap"][0].use([kd_alpha])
    print()
    party_b.point_unit.value.abilities["Slap"][0].use([kd_alpha])
    print()
    party_b.point_unit.value.abilities["Slap"][0].use([kd_alpha])
    print()
    party_b.point_unit.value.abilities["Slap"][0].use([kd_alpha])
