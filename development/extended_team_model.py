"""
extended_team_model.py
~~~~~~~~~~~~~~~~~~~~~~

This module extends the basic team modelling framework defined in
``team_model.py`` by incorporating additional concepts that are
commonly used in football analytics and simulations.  The goal of
these extensions is to provide a richer set of tools for simulating
matches rather than just evaluating a team on paper.  Key additions
include:

* **Elo ratings.**  Each team can be assigned an Elo rating that
  changes based on match outcomes.  The Elo system is widely used
  across sports and games to estimate relative team strength.  After a
  match, both teams' ratings are updated according to a simple formula
  based on the difference between the expected result (derived from
  the rating gap) and the actual result.

* **Poisson expected goals.**  When forecasting match scores, a
  common approach is to model the number of goals scored by each team
  as a Poisson random variable.  The scoring rate (λ) is derived
  from the attacking strength of the team and the defensive strength
  of the opponent.  In our implementation, ``expected_goals`` uses
  this idea to compute a mean goal value based on the ratio of attack
  to defence and the teams' directional flows【3620690256260†L92-L100】.

* **Hattrick‑style flows.**  The Hattrick match engine first
  determines which team controls midfield and then compares attack and
  defence on the left, centre and right flanks【311899566078715†L116-L134】.  We
  generalise this concept by computing separate left, centre and
  right flows for each team (already available via
  ``Team.compute_team_ratings()``) and incorporating them into the
  expected goals calculation.  Zones with higher relative flow and
  better attack vs defence ratios contribute more to the expected goal
  total.

* **Tactical styles.**  Teams often adopt different tactical
  approaches (e.g. attacking, defensive, playing wide, playing
  centrally).  We represent these tactics with simple multipliers
  applied to a team’s aggregated ratings.  For example, an attacking
  style boosts the attack contribution while a defensive style boosts
  defence and reduces attack.

The classes and functions defined here are designed to be used
alongside those in ``team_model.py``.  They reuse the ``Team`` class
via inheritance and extend it with additional properties and methods.

Note: This model is deliberately simplified.  It does not simulate
random match events but instead computes expected goal values and
updates ratings deterministically.  You can integrate stochastic
elements (e.g. sampling from a Poisson distribution) if you wish to
generate varied match outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import exp
from typing import Tuple

from team_model import Player, Position, Team


class TacticalStyle(Enum):
    """Enumeration of simple tactical styles.

    These styles adjust how a team's aggregated ratings contribute to
    expected goals and Elo calculations.  The multipliers are
    heuristically chosen; you can adjust them to better match your
    perception of how a style influences play.
    """

    BALANCED = (1.0, 1.0, 1.0)  # (attack_mult, defence_mult, midfield_mult)
    ATTACKING = (1.2, 0.9, 1.0)
    DEFENSIVE = (0.8, 1.2, 1.0)
    WIDE = (1.0, 1.0, 1.1)  # emphasises side flows (see expected_goals)
    CENTRAL = (1.0, 1.0, 0.9)  # emphasises central play

    def multipliers(self) -> Tuple[float, float, float]:
        return self.value


@dataclass
class ExtendedTeam(Team):
    """An extended team that includes Elo rating and tactical style.

    In addition to the attributes provided by :class:`team_model.Team`
    (``name`` and ``formation``), this dataclass adds fields for an
    Elo rating, a tactical style and momentum tracking.  Because
    :class:`Team` implements its own ``__init__``, the dataclass
    ``__post_init__`` method calls ``super().__init__`` to set up the
    base class.
    """

    # Inherit ``name`` and ``formation`` from Team by explicitly
    # defining them as dataclass fields.  These fields are passed to
    # Team.__init__ via __post_init__.
    name: str = ""
    formation: str = ""
    elo_rating: float = 1500.0
    style: TacticalStyle = TacticalStyle.BALANCED
    # Track consecutive wins (positive) or losses (negative).  Draws reset the
    # streak to zero.  This field is updated automatically by ``update_elo``.
    streak_count: int = 0
    # Momentum parameters: once the absolute streak_count exceeds
    # ``momentum_threshold``, we apply a multiplier to the Elo update.  The
    # effect grows linearly with further wins/losses up to a cap.
    momentum_threshold: int = 3
    momentum_increment: float = 0.1
    momentum_cap: float = 0.3

    # Base multiplier controlling the expected number of goals per
    # scoring opportunity.  A value around 1.0 yields roughly one
    # expected goal per team when two equally matched teams play.  You can
    # tune this to reflect leagues with higher or lower average goals.
    base_goal_factor: float = 1.0

    def __post_init__(self) -> None:
        # Initialise the base Team with name and formation; this sets up
        # the players dictionary.  Without this call, the inherited
        # Team fields would not be initialised properly because
        # dataclass does not automatically call the parent init.
        super().__init__(self.name, self.formation)

    def expected_goals(self, opponent: "ExtendedTeam") -> float:
        """Compute an expected goal value against the given opponent.

        The expected goals function uses a combination of attack and
        defence ratings, directional flows and tactical multipliers to
        estimate how many goals this team should score on average.

        * We start by aggregating the base ratings using
          ``Team.compute_team_ratings()``.
        * Tactical multipliers from ``self.style`` scale the attack,
          defence and midfield ratings.  For example, an attacking
          style boosts attack but reduces defence.
        * For each channel (left, centre, right) we compute a
          contribution: ``mid_share * att_advantage * base_factor``.
        * ``mid_share`` is the ratio of this team’s midfield rating
          along that channel (e.g. left_flow) to the total of both
          teams’ midfield ratings for that channel.  This reflects
          which team is more likely to gain the ball in that zone
          (inspired by the Hattrick engine【311899566078715†L116-L134】).
        * ``att_advantage`` is the ratio of this team’s attack rating
          (scaled by its tactical multipliers) to the sum of its attack
          and the opponent’s defence rating (scaled by the opponent’s
          multipliers).  This represents how likely an attack will be
          converted into a goal when a chance arises.
        * ``base_factor`` is a constant (0.5) controlling the typical
          number of goals in a match.  You can tune this to produce
          higher or lower scoring games.

        The final expected goal tally is the sum of contributions from
        all three channels.
        """
        # Aggregate ratings for both teams
        ours = self.compute_team_ratings()
        theirs = opponent.compute_team_ratings()

        # Extract multipliers
        att_mult, def_mult, mid_mult = self.style.multipliers()
        opp_att_mult, opp_def_mult, opp_mid_mult = opponent.style.multipliers()

        # Scale relevant ratings according to tactical style
        our_attack = ours["attack"] * att_mult
        our_defence = ours["defence"] * def_mult
        our_mid = ours["midfield"] * mid_mult
        our_left = ours["left_flow"] * mid_mult
        our_right = ours["right_flow"] * mid_mult
        our_centre = ours["center_flow"] * mid_mult

        opp_attack = theirs["attack"] * opp_att_mult
        opp_defence = theirs["defence"] * opp_def_mult
        opp_mid = theirs["midfield"] * opp_mid_mult
        opp_left = theirs["left_flow"] * opp_mid_mult
        opp_right = theirs["right_flow"] * opp_mid_mult
        opp_centre = theirs["center_flow"] * opp_mid_mult

        # Compute zone-specific contributions
        #
        # We accumulate expected goals from each channel (left, centre, right).
        # A base goal factor controls the typical goals scored when two
        # evenly matched teams meet.  If both teams have identical ratings,
        # ``mid_share`` will be 0.5 and ``att_advantage`` will be 0.5, so
        # each zone contributes ``base_goal_factor * 0.5 * 0.5``.  With a
        # default ``base_goal_factor`` of 1.0 this yields 0.25 per zone and
        # 0.75 overall, which implies roughly one goal per team on average.
        expected_goals = 0.0
        for zone_our, zone_opp in [
            (our_left, opp_left), (our_centre, opp_centre), (our_right, opp_right)
        ]:
            # Chance of controlling midfield in this zone
            if zone_our + zone_opp > 0:
                mid_share = zone_our / (zone_our + zone_opp)
            else:
                mid_share = 0.5  # if both zero, split equally
            # Attack advantage ratio; ensure denominator > 0 to avoid division by zero
            if (our_attack + opp_defence) > 0:
                att_advantage = our_attack / (our_attack + opp_defence)
            else:
                att_advantage = 0.5
            # Accumulate contribution scaled by base_goal_factor
            expected_goals += self.base_goal_factor * mid_share * att_advantage

        return expected_goals

    def simulate_match(self, opponent: "ExtendedTeam", stochastic: bool = True) -> Tuple[int, int]:
        """Simulate a match and return a plausible scoreline.

        By default this method samples actual goals from a Poisson
        distribution whose mean is given by ``expected_goals``.  This
        introduces randomness so that matches between equally rated
        teams do not always end in a 0‑0 draw.  If ``stochastic`` is
        set to ``False`` the expected goals are rounded to the nearest
        integer instead.  You can adjust the ``base_goal_factor`` on
        each team to increase or decrease typical scoring rates.
        """
        # Compute expected goals for both teams
        home_expected = self.expected_goals(opponent)
        away_expected = opponent.expected_goals(self)
        if stochastic:
            try:
                import numpy as np  # Import here to avoid mandatory dependency when stochastic=False
                home_goals = int(np.random.poisson(home_expected))
                away_goals = int(np.random.poisson(away_expected))
            except Exception:
                # Fallback to deterministic rounding if numpy is unavailable
                home_goals = int(round(home_expected))
                away_goals = int(round(away_expected))
        else:
            # Deterministic rounding
            home_goals = int(round(home_expected))
            away_goals = int(round(away_expected))
        return home_goals, away_goals

    def update_elo(
        self,
        opponent: "ExtendedTeam",
        result: Tuple[int, int],
        k: float = 20.0,
        use_momentum: bool = True,
    ) -> None:
        """Update the Elo ratings of this team and its opponent.

        Elo updates are based on the outcome of a match compared with
        expectations derived from the rating difference.  The expected
        score is calculated using the standard Elo formula:

        ``expected_home = 1 / (1 + 10 ** ((opp_rating - our_rating) / 400))``.

        The actual score is 1 for a win, 0.5 for a draw and 0 for a loss.
        Both teams' ratings are adjusted by ``k * (actual - expected)``.
        A larger ``k`` will make ratings change more rapidly; 20 is a
        commonly used value.  After the update the opponent's rating is
        adjusted in the opposite direction.
        """
        """Update Elo ratings with momentum adjustments.

        In addition to the standard Elo update, this method modifies the
        update magnitude when the team or its opponent is on a winning or
        losing streak longer than ``momentum_threshold``.  Positive
        streaks increase the effective K factor, while negative streaks
        decrease it, with the magnitude limited by ``momentum_cap``.
        After applying the update, the teams' ``streak_count`` values are
        updated.  A draw resets both streak counts to zero.
        """
        # Determine expected result based on rating difference
        expected_home = 1 / (1 + 10 ** ((opponent.elo_rating - self.elo_rating) / 400))
        # Actual result (1=win, 0.5=draw, 0=loss)
        if result[0] > result[1]:
            actual_home = 1.0
        elif result[0] < result[1]:
            actual_home = 0.0
        else:
            actual_home = 0.5

        if use_momentum:
            # Compute momentum multipliers for both teams based on streaks
            def compute_momentum_factor(streak: int, threshold: int, inc: float, cap: float) -> float:
                # Only apply momentum if streak exceeds threshold
                if abs(streak) <= threshold:
                    return 0.0
                raw = (abs(streak) - threshold) * inc
                return min(raw, cap) * (1.0 if streak > 0 else -1.0)

            # Momentum effect for this team and opponent
            our_momentum = compute_momentum_factor(
                self.streak_count,
                self.momentum_threshold,
                self.momentum_increment,
                self.momentum_cap,
            )
            opp_momentum = compute_momentum_factor(
                opponent.streak_count,
                opponent.momentum_threshold,
                opponent.momentum_increment,
                opponent.momentum_cap,
            )
        else:
            # No momentum effect
            our_momentum = 0.0
            opp_momentum = 0.0

        # Base delta from expected vs actual
        base_delta = actual_home - expected_home
        # Adjustments: apply momentum multipliers to K for both teams
        delta_self = k * base_delta * (1.0 + our_momentum)
        delta_opp = -k * base_delta * (1.0 + opp_momentum)
        self.elo_rating += delta_self
        opponent.elo_rating += delta_opp

        # Update streak counts based on the outcome
        if actual_home == 1.0:
            # Home team won
            self.streak_count = self.streak_count + 1 if self.streak_count >= 0 else 1
            opponent.streak_count = opponent.streak_count - 1 if opponent.streak_count <= 0 else -1
        elif actual_home == 0.0:
            # Home team lost
            self.streak_count = self.streak_count - 1 if self.streak_count <= 0 else -1
            opponent.streak_count = opponent.streak_count + 1 if opponent.streak_count >= 0 else 1
        else:
            # Draw resets streaks
            self.streak_count = 0
            opponent.streak_count = 0


def simulate_and_update(
    team_a: ExtendedTeam,
    team_b: ExtendedTeam,
    k: float = 20.0,
    use_momentum: bool = True,
) -> Tuple[int, int]:
    """Run a match simulation between two extended teams and update Elo ratings.

    This convenience function performs three steps:

    1. Calls ``simulate_match`` on ``team_a`` to obtain a deterministic
       scoreline (goals for both teams).
    2. Updates the Elo ratings of both teams using ``update_elo``.
    3. Returns the tuple ``(home_goals, away_goals)`` for convenience.

    Note that ``team_a`` is treated as the home team for Elo
    calculation purposes; you could invert this if the venue is
    different.  Ratings are updated in place.
    """
    # Simulate match between team_a (home) and team_b (away).  The
    # Poisson‐based simulation includes randomness by default.  You can
    # override stochastic behaviour by passing ``stochastic=False`` to
    # ``simulate_match`` if desired.
    score = team_a.simulate_match(team_b)
    # Update Elo ratings, optionally applying momentum adjustments
    team_a.update_elo(team_b, score, k=k, use_momentum=use_momentum)
    return score