class RegistrationError(Exception):
    pass

class DynamicObject:
    pass


class DynamicRule:
    pass


class RuleSet:
    pass


class DynamicEvent:
    pass


class BattleField:
    pass


class Leader:
    pass


class Unit:
    pass


class UnitAbility:
    pass


class BattleRegistry:
    """A database allowing battle participants to reference each other."""

    def __init__(self):
        self.leaders = []
        self.units = []
        self.unit_abilities = []
        self.leaders_by_unit = {}
        self.units_by_leader = {}
        self.unit_abilities_by_unit = {}
        self.unit_by_unit_ability = {}
        self.ruleset = None

    def register_leader(self, leader):
        if leader in self.leaders:
            raise RegistrationError(
                    f"Leader {leader.leader_name} already registered.")
            return
        self.leaders.append(leader)
        self.units_by_leader[leader] = []

    def register_unit(self, unit, leader):
        if unit in self.units:
            raise RegistrationError(
                    f"Unit {unit.unit_name} already registered.")
            return
        if leader not in self.leaders:
            raise RegistrationError(
                    f"Leader {leader.leader_name} isn't registered yet.")
            return
        self.units.append(unit)
        self.units_by_leader[leader].append(unit)
        self.leaders_by_unit[unit] = leader
        self.unit_abilities_by_unit[unit] = []

    def register_unit_ability(self, unit_ability, unit):
        if unit_ability in self.unit_abilities:
            raise RegistrationError(
                    f"Ability {unit_ability.ability_name} already "
                    "registered.")
            return
        if unit not in self.units:
            raise RegistrationError(
                    f"Unit {unit.unit_name} isn't registered yet.")
        self.unit_abilities.append(unit_ability)
        self.unit_abilities_by_unit[unit].append(unit_ability)
        self.unit_by_unit_ability[unit_ability] = unit

