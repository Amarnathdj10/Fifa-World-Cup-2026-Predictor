import pandas as pd
import numpy as np
import os
import random

# Setup paths
base_path = r"d:\Fifa-World-Cup-2026-Predictor"
predictions_path = os.path.join(base_path, "finalmodel", "final_predictions_2026.csv")

def load_teams():
    df = pd.read_csv(predictions_path)
    df.columns = [c.strip() for c in df.columns]
    return df

# Official 2026 Groups (Mapped to CSV names)
OFFICIAL_GROUPS = {
    'A': ['Mexico', 'South Africa', 'Korea Republic', 'Czech Republic'],
    'B': ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'],
    'C': ['Brazil', 'Haiti', 'Morocco', 'Scotland'],
    'D': ['USA', 'Paraguay', 'Australia', 'Turkey'],
    'E': ['Germany', 'Curacao', 'Ivory Coast', 'Ecuador'],
    'F': ['Netherlands', 'Japan', 'Sweden', 'Tunisia'],
    'G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'H': ['Spain', 'Cabo Verde', 'Saudi Arabia', 'Uruguay'],
    'I': ['France', 'Senegal', 'Iraq', 'Norway'],
    'J': ['Argentina', 'Algeria', 'Austria', 'Jordan'],
    'K': ['Portugal', 'Congo DR', 'Uzbekistan', 'Colombia'],
    'L': ['England', 'Croatia', 'Ghana', 'Panama']
}

def simulate_match(team1_rating, team2_rating, is_knockout=False):
    base_avg_goals = 1.4
    elo_diff = team1_rating - team2_rating
    diff_adjustment = (elo_diff / 100) * 0.2
    
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
            win_prob = 1 / (1 + 10**(-elo_diff / 400))
            winner = 0 if random.random() < win_prob else 1
            return t1_goals, t2_goals, winner
        return t1_goals, t2_goals, 2

def get_official_groups(teams_df):
    """
    Constructs the groups using the official assignments and team data from CSV.
    """
    team_data = teams_df.set_index('Team').to_dict('index')
    groups = {}
    for gn, members in OFFICIAL_GROUPS.items():
        groups[gn] = []
        for name in members:
            data = team_data[name].copy()
            data['Team'] = name
            groups[gn].append(data)
    return groups

def simulate_group_stage(groups):
    standings = {}
    for group_name, teams in groups.items():
        stats = {t['Team']: {'points': 0, 'goals_for': 0, 'goals_against': 0, 'gd': 0, 'team_data': t} for t in teams}
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                t1, t2 = teams[i], teams[j]
                g1, g2, winner = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'])
                stats[t1['Team']]['goals_for'] += g1
                stats[t1['Team']]['goals_against'] += g2
                stats[t2['Team']]['goals_for'] += g2
                stats[t2['Team']]['goals_against'] += g1
                if winner == 0: stats[t1['Team']]['points'] += 3
                elif winner == 1: stats[t2['Team']]['points'] += 3
                else:
                    stats[t1['Team']]['points'] += 1
                    stats[t2['Team']]['points'] += 1
        for team in stats:
            stats[team]['gd'] = stats[team]['goals_for'] - stats[team]['goals_against']
        ranked = sorted(stats.values(), key=lambda x: (x['points'], x['gd'], x['goals_for']), reverse=True)
        standings[group_name] = ranked
    return standings

def get_advancers_positions(standings):
    """
    Returns a structured dict of advancers by their position (A1, A2, B1, etc.)
    and the list of 8 best 3rd placed teams.
    """
    positions = {}
    thirds = []
    for gn, ranked in standings.items():
        positions[f'{gn}1'] = ranked[0]['team_data']
        positions[f'{gn}2'] = ranked[1]['team_data']
        thirds.append(ranked[2])
    
    best_thirds = sorted(thirds, key=lambda x: (x['points'], x['gd'], x['goals_for']), reverse=True)[:8]
    best_thirds_teams = [t['team_data'] for t in best_thirds]
    
    return positions, best_thirds_teams

def simulate_scheduled_knockout(positions, best_thirds):
    """
    Simulates the knockout stage using a fixed bracket logic.
    """
    # Round of 32 Pairing Logic (Structured approximation)
    r32_matches = [
        (positions['A1'], best_thirds[0]), (positions['B1'], best_thirds[1]),
        (positions['C1'], best_thirds[2]), (positions['D1'], best_thirds[3]),
        (positions['E1'], best_thirds[4]), (positions['F1'], best_thirds[5]),
        (positions['G1'], best_thirds[6]), (positions['H1'], best_thirds[7]),
        (positions['I1'], positions['A2']), (positions['J1'], positions['B2']),
        (positions['K1'], positions['C2']), (positions['L1'], positions['D2']),
        (positions['E2'], positions['F2']), (positions['G2'], positions['H2']),
        (positions['I2'], positions['J2']), (positions['K2'], positions['L2'])
    ]
    
    stages = {'R16': [], 'QF': [], 'SF': [], 'Final': [], 'Winner': None}
    
    # R32 -> R16
    r16_teams = []
    for t1, t2 in r32_matches:
        _, _, w = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'], is_knockout=True)
        winner = t1 if w == 0 else t2
        r16_teams.append(winner)
        stages['R16'].append(winner['Team'])
        
    # R16 -> QF
    qf_teams = []
    for i in range(0, len(r16_teams), 2):
        t1, t2 = r16_teams[i], r16_teams[i+1]
        _, _, w = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'], is_knockout=True)
        winner = t1 if w == 0 else t2
        qf_teams.append(winner)
        stages['QF'].append(winner['Team'])
        
    # QF -> SF
    sf_teams = []
    for i in range(0, len(qf_teams), 2):
        t1, t2 = qf_teams[i], qf_teams[i+1]
        _, _, w = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'], is_knockout=True)
        winner = t1 if w == 0 else t2
        sf_teams.append(winner)
        stages['SF'].append(winner['Team'])
        
    # SF -> Final
    final_teams = []
    for i in range(0, len(sf_teams), 2):
        t1, t2 = sf_teams[i], sf_teams[i+1]
        _, _, w = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'], is_knockout=True)
        winner = t1 if w == 0 else t2
        final_teams.append(winner)
        stages['Final'].append(winner['Team'])
        
    # Final
    t1, t2 = final_teams[0], final_teams[1]
    _, _, w = simulate_match(t1['Elo_Rating'], t2['Elo_Rating'], is_knockout=True)
    winner = t1 if w == 0 else t2
    stages['Winner'] = winner['Team']
    
    return stages

def run_monte_carlo(num_simulations=1000):
    df = load_teams()
    team_names = df['Team'].tolist()
    stats = {team: {'R32': 0, 'R16': 0, 'QF': 0, 'SF': 0, 'Final': 0, 'Winner': 0} for team in team_names}
    
    print(f"Starting Scheduled Monte Carlo Simulation ({num_simulations} iterations)...")
    for i in range(num_simulations):
        groups = get_official_groups(df)
        standings = simulate_group_stage(groups)
        positions, best_thirds = get_advancers_positions(standings)
        results = simulate_scheduled_knockout(positions, best_thirds)
        
        # All 32 teams reach R32
        for t in list(positions.values()) + best_thirds:
            stats[t['Team']]['R32'] += 1
            
        for stage in ['R16', 'QF', 'SF', 'Final']:
            for team in results[stage]:
                stats[team][stage] += 1
        stats[results['Winner']]['Winner'] += 1
        
        if (i+1) % 100 == 0: print(f"Progress: {i+1}/{num_simulations}")
            
    results_list = []
    for team, stages in stats.items():
        row = {'Team': team}
        for st, count in stages.items(): row[f'{st}_prob'] = count / num_simulations
        results_list.append(row)
    
    return pd.DataFrame(results_list).sort_values('Winner_prob', ascending=False)

if __name__ == "__main__":
    results = run_monte_carlo(1000)
    output_path = os.path.join(base_path, "monte_carlo", "scheduled_results_2026.csv")
    results.to_csv(output_path, index=False)
    print(f"\nScheduled Simulation Complete. Results saved to: {output_path}")
    print("\nTop 10 Teams by Scheduled Win Probability:")
    print(results[['Team', 'Winner_prob', 'Final_prob', 'SF_prob']].head(10))
