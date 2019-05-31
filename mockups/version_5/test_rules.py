import battle

class Rage(battle.DynamicRule):
    def __init__(self, severity, target_unit):
        super().__init__(
                "Rage", "after", ["attack_increase"], severity, None, None,
                None)
        self.target_unit = target_unit

    def will_trigger_on(self, dynamic_event, battle):
        if (
                dynamic_event.target is self.target_unit
                and dynamic_event.attr_name == "hp"
                and dynamic_event.new_value < dynamic_event.old_value):
            return True
        return False

    def trigger(self, dynamic_event, battle):
        if self.severity < 3:
            attack_boost = 1
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting peeved!")
        elif self.severity < 8:
            attack_boost = 2
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting angry!")
        else:
            attack_boost = 3
            trigger_message = (
                    f"{self.target_unit.unit_name} is getting mighty "
                    "pissed off!")
        print(trigger_message)
        battle.update_w_rules(
            self.target_unit, "atk", self.target_unit.atk + attack_boost,
            dynamic_event.by_ability, dynamic_event.at_effectiveness, self)

