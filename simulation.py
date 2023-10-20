import numpy as np
import matplotlib.pyplot as plt

# Decision function
def make_decision(project, budget, ongoing_projects):
    if all(b - c >= 0 for b, c in zip(budget, project["cost"])):
        return "start"
    return "wait"

# Simulation function with time element for a 5-year horizon
def simulate_strategy_time_based(projects, annual_budget_distribution, num_simulations=1000, max_time=60):
    outcomes = []
    for _ in range(num_simulations):
        ongoing_projects = []
        budget = annual_budget_distribution.copy()
        all_started_projects = []
        for t in range(1, max_time + 1):
            # Replenish budget at the start of each year
            if t % 12 == 1:
                budget = [b + ab for b, ab in zip(budget, annual_budget_distribution)]
            # Check for project completions and adjust budget for ongoing projects
            completed_projects = [p for p in ongoing_projects if t >= p["arrival_time"] + p["duration"]]
            ongoing_projects = [p for p in ongoing_projects if t < p["arrival_time"] + p["duration"]]
            for p in completed_projects:
                budget = [b + c for b, c in zip(budget, p["cost"])]
            for p in projects:
                if p["arrival_time"] == t:
                    decision = make_decision(p, budget, ongoing_projects)
                    if decision == "start":
                        ongoing_projects.append(p)
                        all_started_projects.append(p)
                        budget = [b - c for b, c in zip(budget, p["cost"])]
        total_reward = sum(p["reward"]() for p in all_started_projects)
        outcomes.append(total_reward)
    return outcomes


# Adjusted project generator for many smaller projects
def generate_small_projects(num_projects=1000, max_time=120):
    projects = []
    for i in range(num_projects):
        cost = [np.random.randint(10, 50), np.random.randint(5, 25), np.random.randint(1, 10)]
        total_cost = sum(cost)
        arrival_time = np.random.randint(1, max_time)
        duration = np.random.randint(6, 24)  # 6 months to 2 years
        expected_reward = np.random.uniform(total_cost, 1.5 * total_cost)
        reward_function = lambda expected_reward=expected_reward: np.random.normal(expected_reward, expected_reward * 0.1)

        projects.append({
            "name": f"SmallP{i}",
            "cost": cost,
            "arrival_time": arrival_time,
            "duration": duration,
            "expected_reward": expected_reward,
            "reward": reward_function
        })
    return projects

# Adjusted project generator for fewer larger projects
def generate_large_projects(num_projects=200, max_time=120):
    projects = []
    for i in range(num_projects):
        cost = [np.random.randint(20, 100), np.random.randint(10, 50), np.random.randint(2, 20)]
        total_cost = sum(cost)
        arrival_time = np.random.randint(1, max_time)
        duration = np.random.randint(12, 48)  # 3 to 5 years
        expected_reward = np.random.uniform(total_cost, 1.5 * total_cost)
        reward_function = lambda expected_reward=expected_reward: np.random.normal(expected_reward, expected_reward * 0.1)

        projects.append({
            "name": f"LargeP{i}",
            "cost": cost,
            "arrival_time": arrival_time,
            "duration": duration,
            "expected_reward": expected_reward,
            "reward": reward_function
        })
    return projects

# # Generate projects for both scenarios
# small_projects = generate_small_projects()
# large_projects = generate_large_projects()

# # Run simulations for both scenarios
# outcomes_small = simulate_strategy_time_based(small_projects, annual_budget_distribution, max_time=120)
# outcomes_large = simulate_strategy_time_based(large_projects, annual_budget_distribution, max_time=120)