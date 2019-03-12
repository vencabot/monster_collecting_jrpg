class PartyUnit:
    def __init__(self, unit_name, hp_current):
        self.unit_name = unit_name
        self.hp_current = hp_current


class Rule:
    def __init__(self, rule_name, battle, recurrence_limit):
        self.rule_name = rule_name
        self.battle = battle
        self.recurrence_limit = recurrence_limit

    def trigger_with(self, triggering_event):
        return self._trigger_with(triggering_event)

    def _trigger_with(self, triggering_event):
        return True


class BloodForBlood(Rule):
    def __init__(self, battle, ally_team, enemy_team):
        super().__init__("Blood for Blood", battle, 1)
        self.ally_team = ally_team
        self.enemy_team = enemy_team
        self.triggered_by = [UnitTakesDamage]

    def _trigger_with(self, triggering_event):
        if (
                triggering_event.damaged_unit not in self.ally_team
                or triggering_event.damaging_unit not in self.enemy_team):
            return False
        damage_amount = triggering_event.damage_amount / 4
        for enemy_unit in self.enemy_team:
            damage_event = UnitTakesDamage(enemy_unit, self, damage_amount)
            self.battle.events.append(damage_event)
        return True


class SacredProtection(Rule):
    def __init__(self, battle, party_unit):
        super().__init__("Sacred Protection", battle, 1)
        self.party_unit = party_unit
        self.triggered_by = [UnitTakesDamage]

    def _trigger_with(self, triggering_event):
        if (
                triggering_event.damaged_unit is not self.party_unit
                or not isinstance(triggering_event.damaging_unit, Rule)):
            return False
        neutralized_index = battle.events.index(triggering_event)
        self.battle.events.insert(
                neutralized_index,
                RuleNeutralized(triggering_event, self))
        return True


class RuleEvent:
    def __init__(self, event_name):
        # The Event which results in this Event not executing successfully.
        self.neutralized_by = None
        self.event_name = event_name

    def follow_through(self):
        pass


class UnitTakesDamage(RuleEvent):
    def __init__(self, damaged_unit, damaging_unit, damage_amount):
        super().__init__("Unit Takes Damage")
        self.damaged_unit = damaged_unit
        self.damaging_unit = damaging_unit
        self.damage_amount = damage_amount

    def follow_through(self):
        self.damaged_unit.hp_current -= self.damage_amount
        if isinstance(self.damaging_unit, PartyUnit):
            damager_name = self.damaging_unit.unit_name
        elif isinstance(self.damaging_unit, Rule):
            damager_name = self.damaging_unit.rule_name
        print(
                f"{self.damaged_unit.unit_name} took {self.damage_amount} "
                f"damage from {damager_name}!")


class RuleNeutralized(RuleEvent):
    def __init__(self, neutralized_rule_event, neutralizing_rule):
        super().__init__("Rule Neutralized")
        self.neutralized_rule_event = neutralized_rule_event
        self.neutralizing_rule = neutralizing_rule

    def follow_through(self):
        self.neutralized_rule_event.neutralized_by = self.neutralizing_rule
        print(
                f"{self.neutralized_rule_event.damaging_unit.rule_name} "
                f"has been neutralized by "
                f"{self.neutralizing_rule.rule_name}!")


class Battle:
    def __init__(self, team_a, team_b, rules):
        self.team_a = team_a
        self.team_b = team_b
        self.rules = rules
        self.in_ring = (team_a[0], team_b[0])
        self.events = []

    def close_phase(self):
        triggered_events = {}
        current_events = []
        while not current_events == self.events:
            current_events = self.events.copy()
            triggered_this_cycle = []
            for rule_event in current_events:
                for rule in self.rules:
                    if rule not in triggered_events:
                        triggered_events[rule] = 0
                    if (
                            type(rule_event) in rule.triggered_by and
                            triggered_events[rule] < rule.recurrence_limit):
                        if (
                                rule.trigger_with(rule_event)
                                and rule not in triggered_this_cycle):
                            triggered_this_cycle.append(rule)
            for rule in triggered_this_cycle:
                triggered_events[rule] += 1
        for rule_event in self.events:
            if rule_event.neutralized_by is None:
                rule_event.follow_through()


team_a = [
        PartyUnit("Vencabot", 10), PartyUnit("HereGoesNothing9", 10),
        PartyUnit("Zanzhu", 10), PartyUnit("Overlord Steve", 10)]

team_b = [
        PartyUnit("KReichJr", 10), PartyUnit("dixxucker", 10),
        PartyUnit("ph1ll1p_c", 10), PartyUnit("Kyoto3s", 10)]

battle = Battle(team_a, team_b, [])
battle.rules.append(BloodForBlood(battle, team_a, team_b))
battle.rules.append(SacredProtection(battle, team_b[1]))
battle.events.append(UnitTakesDamage(team_a[0], team_b[0], 4))
battle.close_phase()
print(team_b[1].unit_name, team_b[1].hp_current)
