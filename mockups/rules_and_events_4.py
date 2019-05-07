import battle_4
import test_rules_4

class Slap(battle_4.UnitAbility):
    ability_name = "Slap"

    @classmethod
    def deal_some_damage(
            cls, perpetrator, target, battle, damage, effectiveness):
        for leader in battle.leaders:
            if perpetrator in leader.party:
                perp_leader = leader
                break
        print(f"{perpetrator.unit_name} slapped {target.unit_name}!")
        target.update_w_rules(
                "hp", target.hp - damage, perpetrator, cls, effectiveness)
        perpetrator.update_w_rules(
                "mp", perpetrator.mp - 1, perpetrator, cls, effectiveness)
        perp_leader.update_w_rules(
                "ap", perp_leader.ap - 2, perpetrator, cls, effectiveness)

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 1, "glancing")

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 2, "normal")

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        cls.deal_some_damage(perpetrator, targets[0], battle, 4, "critical")


class BloodSong(battle_4.UnitAbility):
    ability_name = "Blood Song"

    @classmethod
    def increase_attack_rules_severity_by(
            cls, perpetrator, effectiveness, dynamic_rules, severity_boost):
        attack_increase_rules = []
        for dynamic_rule in dynamic_rules:
            if "attack_increase" in dynamic_rule.tags:
                attack_increase_rules.append(dynamic_rule)
        for dynamic_rule in attack_increase_rules:
            if dynamic_rule.severity == 10:
                continue
            print(f"{dynamic_rule.rule_name} becomes more severe!")
            new_severity = dynamic_rule.severity + severity_boost
            if new_severity > 10:
                new_severity = 10
            dynamic_rule.update_w_rules(
                    "severity", new_severity, perpetrator, cls,
                    effectiveness)

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} performs the Blood Song! All "
                "attack-increasing rules become slightly more severe!")
        cls.increase_attack_rules_severity_by(
                perpetrator, "glancing", battle.ruleset.rules, 1)

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} performs the Blood Song! All "
                "attack-increasing rules become more severe!")
        cls.increase_attack_rules_severity_by(
                perpetrator, "normal", battle.ruleset.rules, 2)

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} performs the Blood Song! All "
                "attack-increasing rules become much more severe!")
        cls.increase_attack_rules_severity_by(
                perpetrator, "critical", battle.ruleset.rules, 3)


class SealRule(battle_4.UnitAbility):
    ability_name = "Seal Rule"

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} has sealed the rule "
                f"'{targets[0].rule_name}'!")
        seal_rule = test_rules_4.SealRule(
                battle.ruleset, perpetrator, cls, targets[0])
        fade_rule = test_rules_4.RuleFade(
                battle.ruleset, 1, perpetrator, cls, seal_rule) 
        battle.ruleset.update_w_rules(
                "rules", battle.ruleset.rules + [seal_rule, fade_rule],
                perpetrator, cls, "glancing")

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} has sealed the rule "
                f"'{targets[0].rule_name}'!")
        seal_rule = test_rules_4.SealRule(
                battle.ruleset, perpetrator, cls, targets[0])
        fade_rule = test_rules_4.RuleFade(
                battle.ruleset, 3, perpetrator, cls, seal_rule) 
        battle.ruleset.update_w_rules(
                "rules", battle.ruleset.rules + [seal_rule, fade_rule],
                perpetrator, cls, "normal")

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        print(
                f"{perpetrator.unit_name} has sealed the rule "
                f"'{targets[0].rule_name}'!")
        seal_rule = test_rules_4.SealRule(
                battle.ruleset, perpetrator, cls, targets[0])
        fade_rule = test_rules_4.RuleFade(
                battle.ruleset, 5, perpetrator, cls, seal_rule) 
        battle.ruleset.update_w_rules(
                "rules", battle.ruleset.rules + [seal_rule, fade_rule],
                perpetrator, cls, "critical")


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

    poison = test_rules_4.Poison(our_battle.ruleset, 3, vencabot)
    our_battle.ruleset.rules.append(poison)

    print("Vencabot's HP is at ", vencabot.hp)
    print()
    vencabot.use_ability(Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(SealRule, [poison], our_battle)
    print()
    vencabot.use_ability(Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(Slap, [kreichjr], our_battle)
    print()
    print("Vencabot's HP is at ", vencabot.hp)

    for dynamic_rule in our_battle.ruleset.rules:
        print(dynamic_rule.rule_name)
