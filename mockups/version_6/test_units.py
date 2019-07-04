import battlelib
import test_abilities

class DickSucker(battlelib.MetaClass):
    class_name = "Dick Sucker"
    abilities_map = {"Slap": test_abilities.Slap}


class BrainSurgeon(battlelib.MetaClass):
    class_name = "Brain Surgeon"
    abilities_map = {}


class SnakeCharmer(battlelib.MetaClass):
    class_name = "Snake Charmer"
    abilities_map = {}


class Dixxucker(battlelib.Unit):
    def __init__(self, unit_name, leader):
        super().__init__(
                unit_name=unit_name, leader=leader, hp=10, lp=3, mp=10,
                atk=3, defense=3, skl=10, pry=10, tags=[],
                primary_class=DickSucker.get_unit_class_for(self),
                secondary_class=BrainSurgeon.get_unit_class_for(self),
                tertiary_class=SnakeCharmer.get_unit_class_for(self))
        meta_slap = self.primary_class.meta_class.abilities_map["Slap"]
        slap_name = self.primary_class.learn_ability(meta_slap)
        learned_slap = self.primary_class.abilities_map[slap_name][-1]
        self.primary_class.equip_ability(learned_slap)


class Electric(battlelib.MetaClass):
    class_name = "Electric"
    meta_abilities_map = {}


class Speedy(battlelib.MetaClass):
    class_name = "Speedy"
    meta_abilities_map = {}


class Normal(battlelib.MetaClass):
    class_name = "Normal"
    meta_abilities_map = {}


class Pikachu(battlelib.Unit):
    # Speedy attacker
    # Electricity
    # Speed
    # Normal
    def __init__(self, unit_name, leader):
        super().__init__(
                unit_name=unit_name, leader=leader, hp=10, lp=3, mp=10,
                atk=3, defense=3, skl=10, pry=10, tags=[],
                primary_class=Electric.get_unit_class_for(self),
                secondary_class=Speedy.get_unit_class_for(self),
                tertiary_class=Normal.get_unit_class_for(self))
        meta_slap = primary_class.meta_class.abilities_map["Slap"]
        slap_name = primary_class.learn_ability(meta_slap)
        learned_slap = primary_class.abilities_map[slap_name][-1]
        primary_class.equip_ability(learned_slap)


class Chansey(battlelib.Unit):
    # Healer
    # Healer
    # Defense
    # Normal
    pass


class Raticate(battlelib.Unit):
    # Normal attacker
    # Normal (combo-based abilities)
    # Speed
    # Inflicter
    pass


class Butterfree(battlelib.Unit):
    # Inflicter
    # Inflicter
    # Normal
    # Healer
    pass


class Vaporeon(battlelib.Unit):
    # Semi-magical attacker
    # Water attacker
    # Magic-attacker
    # Normal
    pass


class Golem(battlelib.Unit):
    # Defensive
    # Defensive
    # Heavy attacker (hurt him in return) (charge-time)
    # Normal
    pass


class Kadabra(battlelib.Unit):
    # Magic-attacker
    # Magic attacker
    # Enchanter
    # Inflicter
    pass


class Gengar(battlelib.Unit):
    # Can't be hit by normals
    # Magic-attacker
    # Taunter
    # Inflict
    pass
