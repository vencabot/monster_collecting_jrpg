import battle_4

class Slap(battle_4.UnitAbility):
    ability_name = "Slap"

    @classmethod
    def deal_some_damage(cls, perpetrator, target, battle, damage):
        for leader in battle.leaders:
            if perpetrator in leader.party:
                perp_leader = leader
                break
        print(f"{perpetrator.unit_name} slapped {target.unit_name}!")
        target.update_w_rules(
                "hp", target.hp - damage, perpetrator, cls)
        perpetrator.update_w_rules(
                "mp", perpetrator.mp - 1, perpetrator, cls)
        perp_leader.update_w_rules(
                "ap", perp_leader.ap - 2, perpetrator, cls)

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 1)

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 2)

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 4)


class Rage(battle_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Rage", "after", None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} didn't like that very "
                "much! >:O")
        self.target_unit.update_w_rules(
            "atk", self.target_unit.atk + 1,
            dynamic_event.perpetrated_by, dynamic_event.with_ability, self)


class Invincible(battle_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Invincible", "before", None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} is impervious to "
                f"{dynamic_event.perpetrated_by.unit_name}'s attack!")
        dynamic_event.replace_value(self.target_unit.hp, self)


class Hench(battle_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Hench", "before", None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} is hench'd out! Their "
                "damage doubles!")
        old_damage = dynamic_event.old_value - dynamic_event.new_value
        new_hp_value = dynamic_event.target.hp - old_damage * 2
        dynamic_event.replace_value(new_hp_value, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"{self.target_unit.unit_name} is hench'd out! But "
                    "they failed to do damage!")


class AndOne(battle_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("And One", "before", None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"And one! {self.target_unit.unit_name} gets extra damage!")
        dynamic_event.replace_value(dynamic_event.new_value - 1, self)

    def fail(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            print(
                    f"And- wha...? {self.target_unit.unit_name} failed to "
                    "do damage!")


class Persistence(battle_4.DynamicRule):
    def __init__(self, target_unit):
        super().__init__("Persistence", "after", None, None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event):
        original_event = dynamic_event.original_event
        if (
                dynamic_event.perpetrated_by is self.target_unit
                and original_event.triggering_rule is None
                and dynamic_event.attr_name == "hp"
                and original_event.new_value < original_event.old_value
                and dynamic_event.new_value >= dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_unit.unit_name} failed to do damage, but "
                f"they won't give up! {self.target_unit.unit_name} gained "
                "extra attack power!")
        self.target_unit.update_w_rules(
                "atk", self.target_unit.atk + 1, self.target_unit,
                dynamic_event.with_ability, self)


class OldManGenes(battle_4.DynamicRule):
    def __init__(self, target_leader):
        super().__init__("Old Man Genes", "after", None, None)
        self.target_leader = target_leader

    def will_trigger_on(self, dynamic_event):
        if (
                dynamic_event.target is self.target_leader
                and dynamic_event.attr_name == "ap"
                and dynamic_event.old_value >= 5
                and dynamic_event.new_value < 5):
            return True
        return False

    def trigger(self, dynamic_event):
        print(
                f"{self.target_leader.leader_name}'s entire party has the "
                "old man genes! They're all drowsy. Attack power down! T_T")
        for battle_unit in self.target_leader.party:
            battle_unit.update_w_rules(
                    "atk", battle_unit.atk - 1,
                    dynamic_event.perpetrated_by,
                    dynamic_event.with_ability, self)


if __name__ == "__main__":
    our_battle = battle_4.Battle()

    goodvibe = battle_4.BattleLeader(our_battle.ruleset, "GoodVibe")
    vencabot = battle_4.BattleUnit(our_battle.ruleset, "Vencabot")
    panders = battle_4.BattleUnit(our_battle.ruleset, "redpandersbear")
    zanzhu = battle_4.BattleUnit(our_battle.ruleset, "Zanzhu")
    goodvibe.party.append(vencabot)
    goodvibe.party.append(panders)
    goodvibe.party.append(zanzhu)
    our_battle.leaders.append(goodvibe)

    penguinpowered = battle_4.BattleLeader(
            our_battle.ruleset, "PenguinPowered")
    kreichjr = battle_4.BattleUnit(our_battle.ruleset, "KReichJr")
    penguinpowered.party.append(kreichjr)
    our_battle.leaders.append(penguinpowered)

#    our_battle.ruleset.add_rule(Rage(kreichjr))
#    our_battle.ruleset.add_rule(Persistence(vencabot))
    #our_battle.ruleset.add_rule(Invincible(kreichjr))
#    our_battle.ruleset.add_rule(Hench(vencabot))
#    our_battle.ruleset.add_rule(AndOne(vencabot))
    our_battle.ruleset.add_rule(OldManGenes(goodvibe))

    print(f"KReich's HP is at {kreichjr.hp}.")
    print(f"KReich's ATK is at {kreichjr.atk}.")
    print(f"GoodVibe's AP is at {goodvibe.ap}.")
    print(f"Vencabot's ATK is at {vencabot.atk}.")
    print()
    vencabot.use(Slap, [kreichjr], our_battle)
    print()
    vencabot.use(Slap, [kreichjr], our_battle)
    print()
    vencabot.use(Slap, [kreichjr], our_battle)
    print()
    vencabot.use(Slap, [kreichjr], our_battle)
    print()
    print(f"KReich's HP is at {kreichjr.hp}.")
    print(f"KReich's ATK is at {kreichjr.atk}.")
    print(f"GoodVibe's AP is at {goodvibe.ap}.")
    print(f"Vencabot's ATK is at {vencabot.atk}.")
