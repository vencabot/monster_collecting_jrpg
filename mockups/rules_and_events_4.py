import battle_4
import dynamic_system_4

class Slap(battle_4.UnitAbility):
    ability_name = "Slap"

    @classmethod
    def use_glancing(cls, perpetrator, targets, battle):
        for leader in battle.leaders:
            if perpetrator in leader.units:
                perp_leader = leader
                break
        print(f"{perpetrator.unit_name} slapped {targets[0].unit_name}!")
        targets[0].update_w_rules("hp", targets[0].hp - 1, cls)
        perpetrator.update_w_rules("mp", perpetrator.mp - 1, cls)
        perp_leader.update_w_rules("ap", perp_leader.ap - 2, cls)

    @classmethod
    def use_normal(cls, perpetrator, targets, battle):
        leader = self.owner.party.leader
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 2, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)
        leader.ap.update(leader.ap.value - 2, self)

    @classmethod
    def use_critical(cls, perpetrator, targets, battle):
        leader = self.owner.party.leader
        print(f"{self.owner.unit_name} slapped {targets[0].unit_name}!")
        targets[0].hp.update(targets[0].hp.value - 4, self)
        self.owner.mp.update(self.owner.mp.value - 1, self)
        leader.ap.update(leader.ap.value - 2, self)



if __name__ == "__main__":
    our_ruleset = dynamic_system_4.Ruleset()
    vencabot = battle_4.BattleUnit(our_ruleset, "Vencabot")
    kreichjr = battle_4.BattleUnit(our_ruleset, "KReichJr")
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
