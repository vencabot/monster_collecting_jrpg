import random
import statistics

class EventTimeline:
    def __init__(self, original_event):
        self.events = [original_event]

class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value, by_ability,
            at_effectiveness, triggering_rule, timeline=None):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.by_ability = by_ability
        self.at_effectiveness = at_effectiveness
        self.triggering_rule = triggering_rule
        if timeline is None:
            self.timeline = EventTimeline(original_event=self)
        else:
            self.timeline = timeline

    def replace_value(self, new_value, triggering_rule, battle):
        new_event = DynamicEvent(
                target=self.target,
                attr_name=self.attr_name,
                new_value=new_value,
                old_value=self.old_value,
                by_ability=self.by_ability,
                at_effectiveness=self.at_effectiveness,
                triggering_rule=triggering_rule,
                timeline=self.timeline)
        new_timeline_events = self.timeline.events.copy()
        new_timeline_events.append(new_event)
        battle.update_w_rules(
                target=self.timeline,
                attr_name="events",
                new_value=new_timeline_events,
                by_ability=None,
                at_effectiveness=None,
                triggering_rule=triggering_rule)

    def diagnostic_print(self):
        if self.by_ability:
            ability_name = self.by_ability.ability_name
        else:
            ability_name = "None"
        if self.triggering_rule:
            rule_name = self.triggering_rule.rule_name
        else:
            rule_name = "None"
        print(
            "Event Status:\n"
            f"    target: {self.target}\n"
            f"    attr_name: {self.attr_name}\n"
            f"    new_value: {self.new_value}\n"
            f"    old_value: {self.old_value}\n"
            f"    by_ability: {ability_name}\n"
            f"    at_effectiveness: {self.at_effectiveness}\n"
            f"    triggering_rule: {rule_name}")


class DynamicRule:
    def __init__(
            self, rule_name, check_phase, tags, severity, from_ability,
            from_effectiveness, from_targets):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self.recurrence_limit = 1
        self.check_phase = check_phase
        self.tags = tags
        self.severity = severity
        self.from_ability = from_ability
        self.from_effectiveness = from_effectiveness
        self.from_targets = from_targets
        self.triggered_counter = 0

    def react_to(self, dynamic_event, battle):
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event=dynamic_event)
        elif self.will_trigger_on(
                dynamic_event=dynamic_event, battle=battle):
            self.recurrence_counter += 1
            self.trigger(dynamic_event=dynamic_event, battle=battle)
            battle.update_w_rules(
                    target=self,
                    attr_name="triggered_counter",
                    new_value=self.triggered_counter + 1,
                    by_ability=dynamic_event.by_ability,
                    at_effectiveness=dynamic_event.at_effectiveness,
                    triggering_rule=dynamic_event.triggering_rule)
        else:
            self.fail(dynamic_event=dynamic_event)

    def will_trigger_on(self, dynamic_event, battle):
        return False

    def trigger(self, dynamic_event, battle):
        pass

    def at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def fail(self, dynamic_event):
        #print(f"{self.rule_name} failed to trigger.")
        pass


class RuleSet:
    def __init__(self, before_rules=[], after_rules=[]):
        self.before_rules = before_rules
        self.after_rules = after_rules

    def reset_recurrence_counters(self):
        for dynamic_rule in self.before_rules + self.after_rules:
            dynamic_rule.recurrence_counter = 0


class Battle:
    def __init__(self):
        self.leader_a = None
        self.leader_b = None
        self.ruleset = RuleSet()
        
    def update_w_rules(
            self, target, attr_name, new_value, by_ability,
            at_effectiveness, triggering_rule=None):
        old_value = target.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                target=target,
                attr_name=attr_name,
                new_value=new_value,
                old_value=old_value,
                by_ability=by_ability,
                at_effectiveness=at_effectiveness,
                triggering_rule=triggering_rule)
        self.run_through_before_rules(dynamic_event=dynamic_event)
        new_value = dynamic_event.timeline.events[-1].new_value
        target.__dict__[attr_name] = new_value
        if (
                not isinstance(target, EventTimeline)
                and attr_name != "triggered_counter"):
            # DIAGNOSTIC!!!!!
            print(
                    f"    {attr_name} updated from {old_value} to "
                    f"{new_value}.")
        self.run_through_after_rules(
                dynamic_event=dynamic_event.timeline.events[-1])

    def run_through_before_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.before_rules.copy():
            dynamic_rule.react_to(dynamic_event=dynamic_event, battle=self)
            dynamic_event = dynamic_event.timeline.events[-1]

    def run_through_after_rules(self, dynamic_event):
        for dynamic_rule in self.ruleset.after_rules.copy():
            dynamic_rule.react_to(dynamic_event=dynamic_event, battle=self)


class Leader:
    def __init__(self, leader_name):
        self.leader_name = leader_name
        self.party = []
        self.point_unit = None
        self.max_ap = 10
        self.ap = self.max_ap


class Unit:
    def __init__(
            self, unit_name, leader, hp, lp, mp, atk, defense, skl, pry,
            tags, primary_class, secondary_class, tertiary_class):
        self.unit_name = unit_name
        self.leader = leader

        self.base_max_hp = hp
        self.base_max_lp = lp
        self.base_max_mp = mp
        self.base_atk = atk
        self.base_def = defense
        self.base_skl = skl
        self.base_pry = pry
        self.base_tags = tags

        self.aug_max_hp = hp
        self.aug_max_lp = lp
        self.aug_max_mp = mp
        self.aug_atk = atk
        self.aug_def = defense
        self.aug_skl = skl
        self.aug_pry = pry
        self.aug_tags = tags.copy()

        self.cur_hp = hp
        self.cur_lp = lp
        self.cur_mp = mp

        self.primary_class = primary_class
        self.secondary_class = secondary_class
        self.tertiary_class = tertiary_class


class MetaAbility:
    ability_name = "Ability"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        return UnitAbility(ability_name="Ability")


class MetaClass:
    class_name = "Default Class"
    abilities_map = {"Ability": MetaAbility}

    @classmethod
    def get_unit_class_for(cls, unit):
        return UnitClass(owner=unit, meta_class=cls)


class UnitClass:
    def __init__(
            self, owner, meta_class, abilities_map=None, equip_limit=2,
            equipped_map=None):
        self.owner = owner
        self.meta_class = meta_class
        if abilities_map:
            self.abilities_map = abilities_map
        else:
            self.abilities_map = {}
        self.equip_limit = equip_limit
        if equipped_map:
            self.equipped_map = equipped_abilities
        else:
            self.equipped_map = {}

    def learn_ability(self, meta_ability):
        new_ability = meta_ability.get_unit_ability_for(unit_class=self)
        if new_ability.ability_name not in self.abilities_map:
            self.abilities_map[new_ability.ability_name] = []
        self.abilities_map[new_ability.ability_name].append(new_ability)
        return new_ability.ability_name

    def equip_ability(self, unit_ability):
        learned_abilities = []
        for ability_list in self.abilities_map.values():
            for ability in ability_list:
                learned_abilities.append(ability)
        if unit_ability not in learned_abilities:
            raise Exception("Cannot equip un-learned ability.")
        elif len(self.equipped_map) >= self.equip_limit:
            raise Exception("Cannot equip ability: already at equip-limit.")
        else:
            self.equipped_map[unit_ability.ability_name] = unit_ability

    def unequip_ability(self, unit_ability):
        del self.equipped_map[unit_ability.ability_name]


class UnitAbility:
    def __init__(self, owner, ability_name, tags):
        self.owner = owner
        self.ability_name = ability_name
        self.tags = tags
        self.linear_variate()

    def linear_variate(self):
        pass

    def get_mean_pry_enemy_party(self, battle):
        if self.owner not in battle.leader_a.party:
            enemy_party = battle.leader_a.party
        else:
            enemy_party = battle.leader_b.party
        return statistics.mean([unit.aug_pry for unit in enemy_party])

    def get_mean_pry_targets(self, targets):
        return statistics.mean([target.aug_pry for target in targets])

    def roll_for_effectiveness_against_pry(self, mean_pry):
        crit_delta = self.owner.aug_skl / mean_pry
        if crit_delta > 1:
            glance_multiplier = 0
            crit_multiplier = min(crit_delta - 1, 1)
        else:
            crit_multiplier = 0
            glance_multiplier = min(1 / crit_delta - 1, 1)
        glance_chance = glance_multiplier * 55 + 15
        crit_chance = crit_multiplier * 55 + 15
        normal_chance = 100 - glance_chance - critical_chance
        effectiveness_strs = ["glancing", "normal", "critical"]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        return random.choices(effectiveness_strs, effectiveness_weights)[0]

    def roll_for_effectiveness(self, targets, battle):
        mean_pry = self.get_mean_pry_targets(targets)
        return self.roll_for_effectiveness_against_pry(mean_pry)

    def calculate_total_damage(self, target, base_damage):
        damage_scale = self.owner.aug_atk / target.aug_def
        scaled_damage = base_damage * damage_scale
        base_penetration = damage_scale - 1
        penetration_scale_bonus = 1
        penetration_scale = damage_scale + penetration_scale_bonus
        scaled_penetration = base_penetration * penetration_scale
        return scaled_damage + scaled_penetration
 
    def use_on(self, targets, battle):
        if not self.can_be_used_on(targets):
            # DIAGNOSTIC!!!!!!
            print(
                    f"    {self.ability_name} cannot be used this "
                    "way.")
            return
        effectiveness_str = self.roll_for_effectiveness(
                targets=targets, battle=battle)
        self.use_with_effectiveness(
                targets=targets,
                battle=battle,
                effectiveness=effectiveness_str)
        battle.ruleset.reset_recurrence_counters()

    def can_be_used_on(self, targets):
        return True

    def use_with_effectiveness(self, targets, battle, effectiveness):
        print(f"{self.ability_name}'s behavior is not defined, yet!")

