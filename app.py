import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from simulation import simulate_strategy_time_based, generate_small_projects, generate_large_projects

# Streamlit UI
st.title("R&D Investment Simulator")

st.sidebar.header("Simulation Parameters")
num_small_projects = st.sidebar.slider("Number of Small Projects", 10, 100, 50)
num_large_projects = st.sidebar.slider("Number of Large Projects", 5, 50, 20)
annual_budget_distribution = [
    st.sidebar.slider("Annual Budget for Cost C1", 100, 1000, 500),
    st.sidebar.slider("Annual Budget for Cost C2", 50, 500, 300),
    st.sidebar.slider("Annual Budget for Cost C3", 10, 300, 200),
]
max_time = st.sidebar.slider("Time Horizon (Months)", 12, 120, 60)

if st.button("Run Simulation"):
    # Generate projects
    small_projects = generate_small_projects(num_small_projects, max_time)
    large_projects = generate_large_projects(num_large_projects, max_time)
    
    # Run simulations
    outcomes_small = simulate_strategy_time_based(small_projects, annual_budget_distribution, max_time=max_time)
    outcomes_large = simulate_strategy_time_based(large_projects, annual_budget_distribution, max_time=max_time)
    
    # Display results
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(outcomes_small, shade=True, label="Many Smaller Projects", color='blue', ax=ax)
    sns.kdeplot(outcomes_large, shade=True, label="Fewer Larger Projects", color='red', ax=ax)
    plt.title("Comparison of R&D Outcomes")
    plt.xlabel("Total Reward")
    plt.ylabel("Density")
    plt.legend()
    st.pyplot(fig)
