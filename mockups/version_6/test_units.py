import battlelib

class DickSucker(battlelib.MetaClass):
    class_name = "Dick Sucker"


class BrainSurgeon(battlelib.MetaClass):
    class_name = "Brain Surgeon"


class SnakeCharmer(battlelib.MetaClass):
    class_name = "Snake Charmer"


class Dixxucker(battlelib.Unit):
    def __init__(self, unit_name, leader):
        primary_class = battlelib.UnitClass(
                owner=self, metaclass=DickSucker, learned_abilities=[],
                equip_limit=2, equipped_abilities=[])
        secondary_class = battlelib.UnitClass(
                owner=self, metaclass=BrainSurgeon, learned_abilities=[],
                equip_limit=2, equipped_abilities=[])
        tertiary_class = battlelib.UnitClass(
                owner=self, metaclass=SnakeCharmer, learned_abilities=[],
                equip_limit=2, equipped_abilities=[])
        super().__init__(
                unit_name=unit_name, leader=leader, hp=10, lp=3, mp=10,
                atk=3, defense=3, skl=10, pry=10, tags=[],
                primary_class=primary_class,
                secondary_class=secondary_class,
                tertiary_class=tertiary_class)
