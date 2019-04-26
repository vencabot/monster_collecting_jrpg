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
            dynamic_event.perpetrated_by, dynamic_event.w_ability, self)


if __name__ == "__main__":
    our_battle = battle_4.Battle()

    goodvibe = battle_4.BattleLeader(our_battle.ruleset, "GoodVibe")
    vencabot = battle_4.BattleUnit(our_battle.ruleset, "Vencabot")
    goodvibe.party.append(vencabot)
    our_battle.leaders.append(goodvibe)

    penguinpowered = battle_4.BattleLeader(
            our_battle.ruleset, "PenguinPowered")
    kreichjr = battle_4.BattleUnit(our_battle.ruleset, "KReichJr")
    penguinpowered.party.append(kreichjr)
    our_battle.leaders.append(penguinpowered)

    our_battle.ruleset.update_w_rules(
            "rules", our_battle.ruleset.rules + [Rage(kreichjr)])

    print(f"KReich's HP is at {kreichjr.hp}.")
    print(f"KReich's ATK is at {kreichjr.atk}.")
    vencabot.use(Slap, [kreichjr], our_battle)
    print(f"KReich's HP is at {kreichjr.hp}.")
    print(f"KReich's ATK is at {kreichjr.atk}.")
