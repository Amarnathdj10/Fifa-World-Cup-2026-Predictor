"""
FIFA World Cup 2026 — Official Tournament Monte Carlo Simulation
================================================================
Simulates the remaining fixtures of the official FIFA 2026 tournament.

Tournament state as of 2026-07-05:
  - Group Stage   : COMPLETE  (all 32 R32 qualifiers known)
  - Round of 32   : COMPLETE  (all 16 R16 qualifiers known)
  - Round of 16   : IN PROGRESS (Morocco & France through; 6 matches remain)
  - QF / SF / Final : NOT YET PLAYED

Model preserved from original:
  - Hybrid Strength Rating : Strength = Elo_Rating + Predicted_Stage × 50
  - Poisson goal model     : goals ~ Poisson(λ), λ adjusted by strength diff
  - Elo-based penalty win  : P = 1 / (1 + 10^(-Δ/400))
"""

import pandas as pd
import numpy as np
import os
import random

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_PATH = r"d:\Fifa-World-Cup-2026-Predictor"
PREDICTIONS_PATH = os.path.join(BASE_PATH, "finalmodel", "final_predictions_2026.csv")

# ---------------------------------------------------------------------------
# Official FIFA 2026 Groups (from the December 5, 2025 Draw)
# Keys match team names exactly as they appear in final_predictions_2026.csv
# ---------------------------------------------------------------------------
OFFICIAL_GROUPS = {
    'A': ['Mexico', 'South Africa', 'Korea Republic', 'Czech Republic'],
    'B': ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'],
    'C': ['Brazil', 'Morocco', 'Haiti', 'Scotland'],
    'D': ['USA', 'Paraguay', 'Australia', 'Turkey'],
    'E': ['Germany', 'Curacao', 'Ivory Coast', 'Ecuador'],
    'F': ['Netherlands', 'Japan', 'Sweden', 'Tunisia'],
    'G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'H': ['Spain', 'Cabo Verde', 'Saudi Arabia', 'Uruguay'],
    'I': ['France', 'Senegal', 'Iraq', 'Norway'],
    'J': ['Argentina', 'Algeria', 'Austria', 'Jordan'],
    'K': ['Portugal', 'Congo DR', 'Uzbekistan', 'Colombia'],
    'L': ['England', 'Croatia', 'Ghana', 'Panama'],
}

# ---------------------------------------------------------------------------
# Round of 32 — Official bracket and CONFIRMED results
# 32 advancing teams → 16 winners advance to Round of 16
# Format: each entry is (team1, team2, winner)
# ---------------------------------------------------------------------------
ROUND_OF_32_RESULTS = [
    # Match 1
    ('Canada',      'South Africa',          'Canada'),
    # Match 2
    ('Brazil',      'Japan',                 'Brazil'),
    # Match 3
    ('Paraguay',    'Germany',               'Paraguay'),       # 4-3 pens
    # Match 4
    ('Morocco',     'Netherlands',           'Morocco'),        # 3-2 pens
    # Match 5
    ('Norway',      'Ivory Coast',           'Norway'),
    # Match 6
    ('France',      'Sweden',                'France'),
    # Match 7
    ('Mexico',      'Ecuador',               'Mexico'),
    # Match 8
    ('England',     'Congo DR',              'England'),
    # Match 9
    ('Belgium',     'Senegal',               'Belgium'),        # AET
    # Match 10
    ('USA',         'Bosnia and Herzegovina','USA'),
    # Match 11
    ('Spain',       'Austria',               'Spain'),
    # Match 12
    ('Portugal',    'Croatia',               'Portugal'),
    # Match 13
    ('Switzerland', 'Algeria',               'Switzerland'),
    # Match 14
    ('Egypt',       'Australia',             'Egypt'),          # 4-2 pens
    # Match 15
    ('Argentina',   'Cabo Verde',            'Argentina'),      # AET
    # Match 16
    ('Colombia',    'Ghana',                 'Colombia'),
]

# ---------------------------------------------------------------------------
# Round of 16 — Official bracket with known & pending results
# The 16 R32 winners are placed into the R16 bracket.
# Bracket structure: winner of slot i plays winner of slot i+1 (paired by 2s)
# ---------------------------------------------------------------------------
# Each entry: (team1, team2, winner_or_None)
# winner=None means the match is still to be played (will be simulated)
ROUND_OF_16_BRACKET = [
    # Slot 0 vs Slot 1 → QF winner plays in QF match 0
    ('Morocco',      'Canada',      'Morocco'),   # July 4 — PLAYED (3-0)
    ('France',       'Paraguay',    'France'),    # July 4 — PLAYED (1-0)
    # Slot 2 vs Slot 3 → QF winner plays in QF match 1
    ('Brazil',       'Norway',      None),        # July 5 — TO SIMULATE
    ('Mexico',       'England',     None),        # July 5 — TO SIMULATE
    # Slot 4 vs Slot 5 → QF winner plays in QF match 2
    ('Portugal',     'Spain',       None),        # July 6 — TO SIMULATE
    ('USA',          'Belgium',     None),        # July 6 — TO SIMULATE
    # Slot 6 vs Slot 7 → QF winner plays in QF match 3
    ('Switzerland',  'Egypt',       None),        # July 7 — TO SIMULATE
    ('Argentina',    'Colombia',    None),        # July 7 — TO SIMULATE
]

# ---------------------------------------------------------------------------
# All 16 teams currently in the Round of 16
# ---------------------------------------------------------------------------
R16_TEAMS = [t1 if w is None else w
             for t1, t2, w in ROUND_OF_16_BRACKET
             if w is not None] + \
            [t1 for t1, t2, w in ROUND_OF_16_BRACKET if w is None] + \
            [t2 for t1, t2, w in ROUND_OF_16_BRACKET if w is None]

# Derive active teams properly (all 16 R16 participants, not just slot-0)
R16_TEAMS = set()
for t1, t2, w in ROUND_OF_16_BRACKET:
    R16_TEAMS.add(t1)
    R16_TEAMS.add(t2)

# All 32 R32 participants
R32_TEAMS = set()
for t1, t2, w in ROUND_OF_32_RESULTS:
    R32_TEAMS.add(t1)
    R32_TEAMS.add(t2)

# ---------------------------------------------------------------------------
# Load team data & compute Hybrid Strength Rating
# ---------------------------------------------------------------------------

def load_teams() -> dict:
    """
    Loads team data from the predictions CSV and computes the Hybrid Strength.
    Returns a dict: team_name → {Elo_Rating, Predicted_Stage, Strength, ...}
    """
    df = pd.read_csv(PREDICTIONS_PATH)
    df.columns = [c.strip() for c in df.columns]
    # Hybrid Strength: combines Elo rating and ML-predicted stage
    df['Strength'] = df['Elo_Rating'] + df['Predicted_Stage'] * 50
    team_data = df.set_index('Team').to_dict('index')
    return team_data


# ---------------------------------------------------------------------------
# Core match simulation — UNCHANGED from original
# ---------------------------------------------------------------------------

def simulate_match(team1_strength: float, team2_strength: float,
                   is_knockout: bool = False):
    """
    Simulates a match between two teams using their hybrid Strength ratings.

    Uses a Poisson goal model where each team's expected goals (λ) is adjusted
    by the strength difference. In knockout mode, draws are resolved via an
    Elo-based penalty probability.

    Returns:
        (team1_goals, team2_goals, winner_index)
        winner_index: 0 = team1 wins, 1 = team2 wins, 2 = draw (group stage only)
    """
    base_avg_goals = 1.4

    # Strength difference drives expected goal adjustment
    strength_diff = team1_strength - team2_strength
    diff_adjustment = (strength_diff / 100) * 0.2

    t1_lambda = max(0.1, base_avg_goals + diff_adjustment)
    t2_lambda = max(0.1, base_avg_goals - diff_adjustment)

    t1_goals = np.random.poisson(t1_lambda)
    t2_goals = np.random.poisson(t2_lambda)

    if t1_goals > t2_goals:
        return t1_goals, t2_goals, 0
    elif t2_goals > t1_goals:
        return t1_goals, t2_goals, 1
    else:
        if is_knockout:
            # Elo-based probability for extra time / penalties
            win_prob = 1 / (1 + 10 ** (-strength_diff / 400))
            winner = 0 if random.random() < win_prob else 1
            return t1_goals, t2_goals, winner
        return t1_goals, t2_goals, 2  # draw (group stage)


# ---------------------------------------------------------------------------
# Bracket simulation — starts from the current R16 state
# ---------------------------------------------------------------------------

def simulate_tournament_from_r16(team_data: dict) -> dict:
    """
    Simulates the remaining tournament starting from the official R16 bracket.

    For each R16 match:
      - If already played (winner is known), uses the real result.
      - If pending, simulates using the Poisson/Elo model.

    The R16 bracket is positionally paired: winners of consecutive slot pairs
    meet in the quarterfinals, and so on.

    Returns a dict mapping stage names to lists of advancing team names:
      {
        'R16':    [16 team names],
        'QF':     [8 team names],
        'SF':     [4 team names],
        'Final':  [2 team names],
        'Winner': str,
      }
    """
    results = {
        'R16':   [],
        'QF':    [],
        'SF':    [],
        'Final': [],
        'Winner': None,
    }

    # --- Round of 16 ---
    r16_winners = []
    for t1_name, t2_name, known_winner in ROUND_OF_16_BRACKET:
        if known_winner is not None:
            # Real result — use it deterministically
            winner_name = known_winner
        else:
            # Simulate this match
            t1_str = team_data[t1_name]['Strength']
            t2_str = team_data[t2_name]['Strength']
            _, _, w_idx = simulate_match(t1_str, t2_str, is_knockout=True)
            winner_name = t1_name if w_idx == 0 else t2_name

        r16_winners.append(winner_name)
        results['R16'].append(winner_name)

    # --- Quarterfinals (pairs: 0v1, 2v3, 4v5, 6v7) ---
    qf_winners = []
    for i in range(0, len(r16_winners), 2):
        t1_name = r16_winners[i]
        t2_name = r16_winners[i + 1]
        t1_str = team_data[t1_name]['Strength']
        t2_str = team_data[t2_name]['Strength']
        _, _, w_idx = simulate_match(t1_str, t2_str, is_knockout=True)
        winner_name = t1_name if w_idx == 0 else t2_name
        qf_winners.append(winner_name)
        results['QF'].append(winner_name)

    # --- Semifinals (pairs: 0v1, 2v3) ---
    sf_winners = []
    for i in range(0, len(qf_winners), 2):
        t1_name = qf_winners[i]
        t2_name = qf_winners[i + 1]
        t1_str = team_data[t1_name]['Strength']
        t2_str = team_data[t2_name]['Strength']
        _, _, w_idx = simulate_match(t1_str, t2_str, is_knockout=True)
        winner_name = t1_name if w_idx == 0 else t2_name
        sf_winners.append(winner_name)
        results['SF'].append(winner_name)

    # --- Final ---
    t1_name, t2_name = sf_winners[0], sf_winners[1]
    t1_str = team_data[t1_name]['Strength']
    t2_str = team_data[t2_name]['Strength']
    _, _, w_idx = simulate_match(t1_str, t2_str, is_knockout=True)
    winner_name = t1_name if w_idx == 0 else t2_name

    results['Final'].append(t1_name)
    results['Final'].append(t2_name)
    results['Winner'] = winner_name

    return results


# ---------------------------------------------------------------------------
# Monte Carlo runner
# ---------------------------------------------------------------------------

def run_monte_carlo(num_simulations: int = 10_000) -> pd.DataFrame:
    """
    Runs `num_simulations` simulations of the remaining FIFA 2026 tournament
    and computes each team's probability of reaching each knockout stage.

    Probability categories:
      R32_prob   — 1.0 if team reached the Round of 32, else 0.0  (factual)
      R16_prob   — 1.0 if team reached the Round of 16, else 0.0  (factual)
      QF_prob    — Monte Carlo probability of reaching the QF
      SF_prob    — Monte Carlo probability of reaching the SF
      Final_prob — Monte Carlo probability of reaching the Final
      Winner_prob— Monte Carlo probability of winning the tournament
    """
    team_data = load_teams()
    all_teams = list(team_data.keys())

    # Initialise counters
    stage_counts = {team: {s: 0 for s in ['QF', 'SF', 'Final', 'Winner']}
                    for team in all_teams}

    print(f"================================================================")
    print(f"  FIFA World Cup 2026 - Official Tournament Monte Carlo Sim")
    print(f"  Simulating remaining fixtures from Round of 16")
    print(f"  Simulations: {num_simulations:,}")
    print(f"================================================================\n")

    print("  Round of 32 -> all 16 matches complete")
    print("  Round of 16 -> Morocco 3-0 Canada  |  France 1-0 Paraguay\n")
    print("Remaining fixtures to simulate:")
    pending = [(t1, t2) for t1, t2, w in ROUND_OF_16_BRACKET if w is None]
    for t1, t2 in pending:
        print(f"  {t1:15s} vs {t2}")
    print(f"\nStarting {num_simulations:,} Monte Carlo iterations...\n")

    for i in range(num_simulations):
        sim_result = simulate_tournament_from_r16(team_data)

        for stage in ['QF', 'SF', 'Final']:
            for team in sim_result[stage]:
                stage_counts[team][stage] += 1

        stage_counts[sim_result['Winner']]['Winner'] += 1

        if (i + 1) % 1000 == 0:
            print(f"  Progress: {i + 1:,} / {num_simulations:,} "
                  f"({(i + 1) / num_simulations * 100:.0f}%)")

    # ---------------------------------------------------------------------------
    # Build results DataFrame
    # ---------------------------------------------------------------------------
    rows = []
    for team in all_teams:
        in_r32 = team in R32_TEAMS
        in_r16 = team in R16_TEAMS

        row = {
            'Team':        team,
            'R32_prob':    1.0 if in_r32 else 0.0,
            'R16_prob':    1.0 if in_r16 else 0.0,
            'QF_prob':     stage_counts[team]['QF']     / num_simulations,
            'SF_prob':     stage_counts[team]['SF']      / num_simulations,
            'Final_prob':  stage_counts[team]['Final']   / num_simulations,
            'Winner_prob': stage_counts[team]['Winner']  / num_simulations,
        }
        rows.append(row)

    results_df = pd.DataFrame(rows)
    results_df = results_df.sort_values('Winner_prob', ascending=False)
    results_df = results_df.reset_index(drop=True)

    return results_df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    NUM_SIMS = 10_000

    results = run_monte_carlo(NUM_SIMS)

    # Save to CSV
    output_path = os.path.join(
        BASE_PATH, "monte_carlo", "monte_carlo_results_2026.csv"
    )
    results.to_csv(output_path, index=False)

    # ---------------------------------------------------------------------------
    # Console report
    # ---------------------------------------------------------------------------
    print(f"\n{'=' * 65}")
    print(f"  Simulation Complete  --  {NUM_SIMS:,} iterations")
    print(f"  Results saved to: {output_path}")
    print(f"{'=' * 65}\n")

    # Active 16 teams only (teams still in tournament)
    active = results[results['R16_prob'] == 1.0].copy()
    active = active.sort_values('Winner_prob', ascending=False)

    col_fmt = "{:<22} {:>8} {:>8} {:>8} {:>8} {:>18}"
    print(col_fmt.format("Team", "QF%", "SF%", "Final%", "Win%", "Status"))
    print("-" * 70)

    for _, row in active.iterrows():
        # Flag teams already confirmed into QF (Morocco & France)
        r16_done = row['QF_prob'] > 0.98   # known R16 winners ~= 1.0 QF entry
        status = "[R16 confirmed]" if r16_done else ""
        print(col_fmt.format(
            row['Team'],
            f"{row['QF_prob']*100:.1f}",
            f"{row['SF_prob']*100:.1f}",
            f"{row['Final_prob']*100:.1f}",
            f"{row['Winner_prob']*100:.1f}",
            status,
        ))

    total_win_prob = active['Winner_prob'].sum()
    print(f"\n  Total Winner probability (should ~= 1.0): {total_win_prob:.4f}")

    # Sanity checks
    print(f"\n{'- ' * 32}")
    print("  Sanity Checks:")

    morocco_r16 = results.loc[results['Team'] == 'Morocco', 'R16_prob'].values
    france_r16  = results.loc[results['Team'] == 'France',  'R16_prob'].values
    ok = lambda v, exp: "PASS" if v == exp else "FAIL"
    print(f"    Morocco  R16_prob = {morocco_r16[0]:.1f}  (expected 1.0) [{ok(morocco_r16[0], 1.0)}]")
    print(f"    France   R16_prob = {france_r16[0]:.1f}  (expected 1.0) [{ok(france_r16[0], 1.0)}]")
    print(f"    R32 teams count   = {int(results['R32_prob'].sum())}  (expected 32) [{ok(int(results['R32_prob'].sum()), 32)}]")
    print(f"    R16 teams count   = {int(results['R16_prob'].sum())}  (expected 16) [{ok(int(results['R16_prob'].sum()), 16)}]")
    print(f"{'=' * 65}\n")
