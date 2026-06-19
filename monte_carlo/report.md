# 2026 FIFA World Cup: Monte Carlo Simulation Report

## 1. Project Objective
The goal was to implement a probabilistic simulation of the 2026 FIFA World Cup to determine the win probabilities for each participating team, accounting for the new 48-team format and inherent match-day randomness.

## 2. Methodology

### A. Match Prediction Engine
Matches are simulated using a **Poisson Distribution** to determine goals scored by each team:
- **Team Strength**: Calculated based on the latest Elo ratings.
- **Expected Goals ($\lambda$)**: The mean number of goals for a team is adjusted based on the Elo difference between competitors. A higher-rated team has a higher $\lambda$.
- **Upset Potential**: By using a Poisson process, the model naturally allows for upsets (e.g., a lower-rated team scoring more goals than a higher-rated one).
- **Knockout Logic**: In the event of a draw in knockout stages, a winner is determined probabilistically, slightly favoring the higher-rated team to simulate quality under pressure.

### B. Tournament Structure (2026 Format)
The simulation strictly follows the new FIFA 2026 guidelines:
1.  **Group Stage**: 12 groups of 4 teams.
2.  **Points System**: 3 for a win, 1 for a draw, 0 for a loss. Tie-breakers include GD (Goal Difference) and GS (Goals Scored).
3.  **Progression**: 
    - The top 2 teams from each of the 12 groups advance.
    - The 8 best 3rd-placed teams (ranked by points/GD) also advance to fill the **Round of 32**.
4.  **Knockout Bracket**: Sequential elimination rounds (R32, R16, QF, SF, Final).

### C. Simulation Scale
- **Iterations**: 1,000 full tournament simulations were performed to generate stable win probabilities.

## 3. Initial Results Summary

Based on the latest Elo ratings and 1,000 simulated tournaments, the following teams emerge as favorites:

| Rank | Team | Win Probability % | Finalist Probability % |
| :--- | :--- | :--- | :--- |
| 1 | **Argentina** | 20.9% | 29.9% |
| 2 | **France** | 13.5% | 22.8% |
| 3 | **Portugal** | 10.8% | 17.7% |
| 4 | **England** | 9.6% | 16.0% |
| 5 | **Netherlands** | 6.7% | 12.6% |

*Note: Argentina's high probability is driven by their current #1 Elo ranking and recent performance metrics.*

## 4. Real-World Scheduled Simulation (June 2026 Update)
As of **June 14, 2026**, the tournament is officially underway. We have updated the simulation to use the **Official Group Stage Assignments** and a structured knockout bracket.

| Rank | Team | Win Probability % (Scheduled) | Path Difficulty |
| :--- | :--- | :--- | :--- |
| 1 | **Argentina** | 21.2% | Moderate (Group J) |
| 2 | **France** | 11.6% | High (Group I) |
| 3 | **Portugal** | 9.0% | Moderate (Group K) |
| 4 | **Netherlands** | 8.4% | High (Group F) |
| 5 | **England** | 7.5% | High (Group L) |

*The scheduled simulation accounts for the specific opponents each team faces in their groups, which slightly shifts the probabilities compared to the randomized model.*

## 5. File Structure
All related files are in the `monte_carlo/` directory:
- `monte_carlo_simulation.py`: Baseline model using randomized groups.
- `scheduled_bracket_simulation.py`: **NEW** Official 2026 schedule model.
- `monte_carlo_results_2026.csv`: Data from randomized model.
- `scheduled_results_2026.csv`: **NEW** Data from scheduled model.
- `report.md`: This document.

## 6. Future Enhancements
- **Live Score Integration**: Feeding real-time group stage results from the ongoing matches to refine knockout predictions.
- **Dynamic Elo Evolution**: Updating team ratings match-by-match based on their 2026 performance.
