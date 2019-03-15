class Party:
    def __init__(self, party_name):
        self.party_name = party_name
        self.units = []
        self.battle = None

    def append(self, party_unit):
        self.units.append(party_unit)
        party_unit.party = self


class PartyUnit:
    def __init__(self, unit_name, hp_current):
        self.unit_name = unit_name
        self.hp_current = hp_current
        self.party = None

    def slap(self, target_unit):
        damage_event = UnitTakesDamage(target_unit, self, 8)
        self.party.battle.events.append(damage_event)
        self.party.battle.close_phase()


class DynamicRule:
    def __init__(self, rule_name, recurrence_limit):
        self.rule_name = rule_name
        self.listen_for = []
        self.recurrence_limit = recurrence_limit
        self.recurrence_counter = 0

    def check_event(self, checked_event):
        if type(checked_event) in self.listen_for:
            if self.recurrence_counter < self.recurrence_limit:
                if self._check_event(checked_event):
                    self.recurrence_counter += 1

    def _check_event(self, checked_event):
        return True

    def limit_reached(self):
        if self.recurrence_counter >= self.recurrence_limit:
            return True
        return False


class BloodForBlood(DynamicRule):
    """If an ally unit takes damage, all non-ally units take 1/4 damage."""
    def __init__(self, ally_team):
        super().__init__("Blood for Blood", 1)
        self.ally_team = ally_team
        self.listen_for.append(UnitTakesDamage)

    def _check_event(self, checked_event):
        if (
                checked_event.damaged_unit not in self.ally_team.units
                or not isinstance(checked_event.damaging_unit, PartyUnit)):
            return False
        damage_amount = checked_event.damage_amount / 4
        for enemy_unit in checked_event.damaging_unit.party.units:
            damage_event = UnitTakesDamage(enemy_unit, self, damage_amount)
            self.ally_team.battle.events.append(damage_event)
        return True


class SacredProtection(DynamicRule):
    """Prevents a single unit from taking damage from a DynamicRule."""
    def __init__(self, party_unit):
        super().__init__("Sacred Protection", 1)
        self.party_unit = party_unit
        self.listen_for.append(UnitTakesDamage)

    def _check_event(self, checked_event):
        if (
                checked_event.damaged_unit is not self.party_unit or
                not isinstance(checked_event.damaging_unit, DynamicRule)):
            return False
        neutralized_index = battle.events.index(checked_event)
        self.party_unit.party.battle.events.insert(
                neutralized_index,
                EventNeutralized(checked_event, self))
        return True


class BattleEvent:
    def __init__(self):
        self.neutralized_by = None

    def follow_through(self):
        pass


class UnitTakesDamage(BattleEvent):
    def __init__(self, damaged_unit, damaging_unit, damage_amount):
        super().__init__()
        self.damaged_unit = damaged_unit
        self.damaging_unit = damaging_unit
        self.damage_amount = damage_amount

    def follow_through(self):
        self.damaged_unit.hp_current -= self.damage_amount
        if isinstance(self.damaging_unit, PartyUnit):
            damager_name = self.damaging_unit.unit_name
        elif isinstance(self.damaging_unit, DynamicRule):
            damager_name = self.damaging_unit.rule_name
        print(
                f"{self.damaged_unit.unit_name} took {self.damage_amount} "
                f"damage from {damager_name}!")


class EventNeutralized(BattleEvent):
    def __init__(self, neutralized_event, neutralizing_rule):
        super().__init__()
        self.neutralized_event = neutralized_event
        self.neutralizing_rule = neutralizing_rule

    def follow_through(self):
        self.neutralized_event.neutralized_by = self.neutralizing_rule
        print(
                f"{self.neutralized_event.damaging_unit.rule_name} "
                f"has been neutralized by "
                f"{self.neutralizing_rule.rule_name}!")


class Battle:
    def __init__(self):
        self.parties = []
        self.rules = []
        self.events = []

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self

    def close_phase(self):
        self._trigger_rules()
        self._reset_recurrence_counters()
        self._follow_through()

    def _trigger_rules(self):
        cycle_events = []
        while not cycle_events == self.events:
            cycle_events = self.events.copy()
            for battle_event in cycle_events:
                for rule in self.rules:
                    rule.check_event(battle_event)

    def _reset_recurrence_counters(self):
        for rule in self.rules:
            rule.recurrence_counter = 0

    def _follow_through(self):
        for battle_event in self.events:
            if battle_event.neutralized_by is None:
                battle_event.follow_through()


if __name__ == "__main__":
    vencabot = PartyUnit("Vencabot", 10)
    heregoesnothing9 = PartyUnit("HereGoesNothing9", 10)
    zanzhu = PartyUnit("Zanzhu", 10)
    overlord_steve = PartyUnit("Overlord Steve", 10)
    kreichjr = PartyUnit("KReichJr", 10)
    dixxucker = PartyUnit("dixxucker", 10)
    ph1ll1p_c = PartyUnit("ph1ll1p_c", 10)
    kyoto3s = PartyUnit("Kyoto3s", 10)

    team_a = Party("team_a")
    team_a_units = [vencabot, heregoesnothing9, zanzhu, overlord_steve]
    for party_unit in team_a_units:
        team_a.append(party_unit)

    team_b = Party("team_b")
    team_b_units = [kreichjr, dixxucker, ph1ll1p_c, kyoto3s]
    for party_unit in team_b_units:
        team_b.append(party_unit)

    battle = Battle()
    battle.append_party(team_a)
    battle.append_party(team_b)
    battle.rules.append(BloodForBlood(team_a))
    battle.rules.append(SacredProtection(dixxucker))

    dixxucker.slap(vencabot)
    print(dixxucker.unit_name, dixxucker.hp_current)
