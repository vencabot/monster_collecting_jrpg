import random

class EventTimeline:
    """Holds a list of previous mutations of a particular DynamicEvent.

    This mutable object is necessary so that all DynamicEvents in a single
    timeline can point toward the same EventTimeline even when the list at
    'some_timeline.events' is replaced.

    This allows for DynamicEvents to propose and report on changes to the
    timeline, itself.

    So, DynamicRules can run,

        some_battle.update_w_rules(dynamic_event.timeline, "events", ...)

    This will allow all events in the timeline to share a reference to that
    timeline, which wouldn't be possible with

        some_battle.update_w_rules(dynamic_event, "timeline", ...)

    because update_w_rules will replace a list with a list rather than
    mutate the original list.
    """

    def __init__(self, original_event):
        """The only attribute is a list of events in the timeline."""
        self.events = [original_event]

class DynamicEvent:
    """A proposal for and a report of state-changes in the game.
    
    When a DynamicRule, UnitAbility, or other actor wants to update any
    value in a given battle, that 'update' can trigger any number of other
    DynamicRules. This is the core gimmick of our Dynamic Rule System.

    For this to be possible, attribute updates are not made directly through
    Python's syntax. Instead, attribute updates are proposed using some
    Battle object's 'update_w_rules' method. This creates and processes
    DynamicEvents which describe the proposed attribute update.

    The attributes of a DynamicEvent are meant to provide as much
    information as any DynamicRule could possibly want to decide whether or
    not to trigger when a change is proposed or has occurred. These
    attributes include:

        target: the object whose attribute is being updated
        attr_name: the updated attribute's name as a target.__dict__ key
        new_value: the value being proposed to be held at target.attr_name
        old_value: used post-update to recall target.attr_name's old value
        by_ability: the UnitAbility proposing the update or 'None'
        at_effectiveness: the effectiveness of that ability or 'None'
        triggering_rule: the DynamicRule proposing the update or 'None'

    Sometimes, updates are proposed directly by a UnitAbility. Other times,
    updates are proposed by a triggered rule. Even other times, DynamicRules
    propose updates to an EXISTING DynamicEvent which was proposed, itself,
    by some UnitAbility or DynamicRule.

    For instance, if some UnitAbility 'Slap' is used, it may propose an HP
    change to some target Unit. In this case, the by_ability would be that
    Slap. It would record at_effectiveness, but triggering_rule would be
    None.

    If that HP change is altered by some DynamicEvent has been altered by
    some DynamicRule ("Hench") before it can take affect, the new
    DynamicEvent that's created as a result would have the Slap as
    by_ability and the Hench as triggering_rule.

    If the original proposed change was, for instance, HP damage as the
    result of a 'Poison' DynamicRule, then triggering_rule would be that
    Poison and by_ability would be 'None'.

    DynamicEvents are processed through the Battle's DynamicRules in two
    phases: a phase 'before' the proposed gamestate update is made, and a
    phase 'after' the finalized update is made. In this respect,
    DynamicEvents act as both PROPOSALS and REPORTS for gamestate changes.

    In the 'before' phase, DynamicEvents can be altered -- but not in the
    sense that their individual attributes are updated (DynamicEvents should
    be treated as immutable). Rather, a spin-off DynamicEvent is created and
    added to the first DynamicEvent's EventTimeline at the 'timeline'
    attribute. All spun-off DynamicEvents share the same EventTimeline,
    and, at the end of the 'before' phase, the most recent DynamicEvent in
    the EventTimeline is what defines the gamestate update. Some
    DynamicRules may look at the 'timeline' attribute to decide to trigger
    after some series of particular changes have been made to the proposal.

    In the 'after' phase, the EventTimeline is no longer altered. Rather,
    new, unrelated DynamicEvents might be proposed as a reaction to the
    gamestate update that was just finalized.
    """

    def __init__(
            self, target, attr_name, new_value, old_value, by_ability,
            at_effectiveness, triggering_rule, timeline=None):
        """Permanently-set attributes describing an in-game change."""
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.by_ability = by_ability
        self.at_effectiveness = at_effectiveness
        self.triggering_rule = triggering_rule
        if timeline is None:
            self.timeline = EventTimeline(self)
        else:
            self.timeline = timeline

    def replace_value(self, new_value, triggering_rule, battle):
        """Manipulate the event and add the change to the timeline."""
        new_event = DynamicEvent(
                self.target, self.attr_name, new_value, self.old_value,
                self.by_ability, self.at_effectiveness, triggering_rule,
                self.timeline)
        new_timeline_events = self.timeline.events.copy()
        new_timeline_events.append(new_event)
        battle.update_w_rules(
                self.timeline, "events", new_timeline_events, None, None,
                triggering_rule)

    def diagnostic_print(self):
        """Diagnostic method to make the event human-readable."""
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
    """An actor that's triggered by and which can alter DynamicEvents.
    
    The core gimmick of our game is that virtually any change to the 
    gamestate can result in rewards, penalties, and other affects for either
    party. This mechanism is managed by the processing of DynamicEvents by
    DynamicRules.

    The affect of some DynamicRule comes into play after it's 'triggered' by
    some DynamicEvent, and this can happen in one of two phases:

    In the 'before' phase, DynamicRules can see a proposed gamestate update
    before it happens, and they can make changes to that proposal. This
    allows for various gamestate updates to be AUGMENTED or NEUTRALIZED.

    In the 'after' phase, DynamicRules react to a gamestate change that was
    just finalized. They can no longer augment or neutralize that change,
    but they can propose their own, new changes to the gamestate based on
    that happenstance.

    DynamicRules can process any proposed update to an attribute using
    DynamicEvent objects as created during Battle.update_w_rules. This
    includes reacting to DynamicEvents which propose or report on changes to
    some other DynamicEvent's timeline. Processing a DynamicEvent and
    checking to see whether that event's 'target' is an EventTimeline can
    allow DynamicRules to trigger immediately after some other DynamicRule.

    Because DynamicRules are processed in the order that they're stored in
    some Ruleset's 'before_rules' or 'after_rules' list, ordering is
    significant.
    """

    def __init__(
            self, rule_name, check_phase, tags, severity, from_ability,
            from_effectiveness, from_targets):
        """Provide needed state and log the rule's origins for reference."""
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
        """Process a DynamicEvent and trigger if possible and necessary."""
        if self.recurrence_counter == self.recurrence_limit:
            self.at_limit(dynamic_event)
        elif self.will_trigger_on(dynamic_event, battle):
            self.recurrence_counter += 1
            self.trigger(dynamic_event, battle)
            battle.update_w_rules(
                    self, "triggered_counter", self.triggered_counter + 1,
                    dynamic_event.by_ability,
                    dynamic_event.at_effectiveness,
                    dynamic_event.triggering_rule)
        else:
            self.fail(dynamic_event)

    def will_trigger_on(self, dynamic_event, battle):
        """Override to return whether this rule triggers on some event."""
        return False

    def trigger(self, dynamic_event, battle):
        """Override this to define the rule's behavior when triggered."""
        pass

    def at_limit(self, dynamic_event):
        """Diagnostic method running at recurrence limit failure."""
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def fail(self, dynamic_event):
        """Runs when the rule fails due to the conditions of the event."""
        #print(f"{self.rule_name} failed to trigger.")
        pass


class RuleSet:
    """Contains two attributes holding lists of rules organized by phase.
    
    This container object is necessary so that DynamicRules can trigger
    when other DynamicRules are added or removed from the RuleSet.
    
    Because 'Battle.update_w_rules' will always REPLACE some value with a
    NEW value, it isn't effective for mutable objects such as lists.
    Therefore, in order to create a DynamicEvent which describes a change in
    a Ruleset, it's necessary that we wrap those lists of DynamicRules in
    another mutable object which the Battle can maintain a reference to.
    
    So, when proposing a change to a battle's rules, we do this:

        some_battle.update_w_rules(battle.ruleset, "before_rules", ...)

    If we did

        some_battle.update_w_rules(some_battle, "before_rules", ...)

    further processing in the same ruleset wouldn't take into account the
    changes to the list.
    """

    def __init__(self, before_rules=[], after_rules=[]):
        """Separate rules by phase."""
        self.before_rules = before_rules
        self.after_rules = after_rules

    def reset_recurrence_counters(self):
        """Reset the recurrence counters of all rules to '0'."""
        for dynamic_rule in self.before_rules + self.after_rules:
            dynamic_rule.recurrence_counter = 0


class Battle:
    """Manages the Dynamic Rule System by creating and processing events.
    
    'Battle.update_w_rules' is the method at the heart of the Dynamic Rule
    System. Under this sytem, rather than directly implementing gamestate
    changes using Python syntax, changes are proposed via this method so
    that those changes can be pre-emptively and posthumously examined and
    acted upon by DynamicRules.

    Outside of the context of the Battle object, none of these classes are
    especially dynamic -- which is important, because, outside of battle,
    these same classes can still be used to describe things such as Units,
    Leaders, UnitAbilities, etc.

    Within the context of a Battle object, these and other objects become
    'dynamic,' meaning that they become subject to DynamicRules.
    """

    def __init__(self):
        """Define and retain the persistent RuleSet for this battle."""
        self.ruleset = RuleSet()
        
    def update_w_rules(
            self, target, attr_name, new_value, by_ability,
            at_effectiveness, triggering_rule=None):
        """Take a proposed gamestate change and process it through rules."""
        old_value = target.__dict__[attr_name]
        dynamic_event = DynamicEvent(
                target, attr_name, new_value, old_value, by_ability,
                at_effectiveness, triggering_rule)
        self.run_through_before_rules(dynamic_event)
        new_value = dynamic_event.timeline.events[-1].new_value
        target.__dict__[attr_name] = new_value
        if (
                not isinstance(target, EventTimeline)
                and attr_name != "triggered_counter"):
            # DIAGNOSTIC!!!!!
            print(
                    f"    {attr_name} updated from {old_value} to "
                    f"{new_value}.")
        self.run_through_after_rules(dynamic_event.timeline.events[-1])

    def run_through_before_rules(self, dynamic_event):
        """In this phase, DynamicEvents can be manipulated / rejected."""
        for dynamic_rule in self.ruleset.before_rules.copy():
            dynamic_rule.react_to(dynamic_event, self)
            dynamic_event = dynamic_event.timeline.events[-1]

    def run_through_after_rules(self, dynamic_event):
        """In this phase, rules react to a change which just occurred."""
        for dynamic_rule in self.ruleset.after_rules.copy():
            dynamic_rule.react_to(dynamic_event, self)


class Leader:
    """Auxiliary unit managing a team of Units and team-wide resources."""

    def __init__(self, leader_name):
        self.leader_name = leader_name
        self.party = []
        self.point_unit = None
        self.max_ap = 10
        self.ap = self.max_ap


class Unit:
    """A team-member who uses abilities and shields the team when active."""

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


class MetaClass:
    class_name = "Default Class"


class UnitClass:
    def __init__(
            self, owner, metaclass, learned_abilities, equip_limit,
            equipped_abilities):
        self.owner = owner
        self.metaclass = metaclass
        self.learned_abilities = learned_abilities
        self.equip_limit = equip_limit
        self.equipped_abilities = equipped_abilities

    def learn(self, meta_ability):
        new_unit_ability = meta_ability.get_unit_ability_for(self)
        self.learned_abilities.append(new_unit_ability)


class MetaAbility:
    """Handles the semi-randomized processes for learning UnitAbilities."""
    ability_name = "Ability"

    @classmethod
    def get_unit_ability_for(cls, unit_class):
        return UnitAbility("Ability")


class UnitAbility:
    """An action which propels the battle toward completion."""

    def __init__(self, owner, ability_name):
        """Define ability necessities. Override to give additional state."""
        self.ability_name = ability_name
        self.owner = owner
        self.effectiveness_map = {
                "glancing": self.use_glancing, "normal": self.use_normal,
                "critical": self.use_critical}

    def roll_for_effectiveness(self, targets, battle):
        """Return effectiveness str. Override to customize crit chance."""
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_strs = ["glancing", "normal", "critical"]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        return random.choices(effectiveness_strs, effectiveness_weights)[0]
 
    def use_on(self, targets, battle):
        """Find 'effectiveness' and use the matching method on targets."""
        if not self.can_be_used_on(targets):
            # DIAGNOSTIC!!!!!!
            print(
                    f"    {self.ability_name} cannot be used this "
                    "way.")
            return
        effectiveness_str = self.roll_for_effectiveness(targets, battle)
        use_callable = self.effectiveness_map[effectiveness_str]
        use_callable(targets, battle)
        battle.ruleset.reset_recurrence_counters()

    def can_be_used_on(self, targets):
        """Override to warn player if this can be used on given targets."""
        return True

    def use_glancing(self, targets, battle):
        """Override to define ability 'low effectiveness' behavior."""
        self.use_normal(targets, battle)

    def use_normal(self, targets, battle):
        """Override to define default ability behavior."""
        pass

    def use_critical(self, targets, battle):
        """Override to define ability 'high effectiveness' behavior."""
        self.use_normal(targets, battle)


class RelationshipHelper:
    """Helper class to simplify reciprocal relationships.""" 

    @classmethod
    def create_unit_for(cls, leader, unit_type, unit_name):
        leader.party.append(unit_type(unit_name, leader))

    @classmethod
    def create_ability_for(cls, unit, ability_class):
        unit.abilities.append(ability_class(unit))
