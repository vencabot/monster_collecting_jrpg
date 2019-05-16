import battle_4
import test_rules_4
import test_abilities_4

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

    print("Vencabot's HP is at ", vencabot.hp)
    print()
    kreichjr.use_ability(
            test_abilities_4.PoisonDart, [vencabot], our_battle)
    print()
    vencabot.use_ability(test_abilities_4.Slap, [kreichjr], our_battle)
    print()
    for dynamic_rule in our_battle.ruleset.rules:
        if isinstance(dynamic_rule, test_rules_4.Poison):
            target_rule = dynamic_rule
    vencabot.use_ability(
            test_abilities_4.SealRule, [target_rule], our_battle)
    print()
    vencabot.use_ability(test_abilities_4.Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(test_abilities_4.Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(test_abilities_4.Slap, [kreichjr], our_battle)
    print()
    vencabot.use_ability(test_abilities_4.Slap, [kreichjr], our_battle)
    print()
    print("Vencabot's HP is at ", vencabot.hp)

    for dynamic_rule in our_battle.ruleset.rules:
        print(dynamic_rule.rule_name)
