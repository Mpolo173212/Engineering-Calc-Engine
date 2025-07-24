import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.dirname(__file__))


# Import the solver function from the solvers folder
from Solvers.Hazen_Williams import calculate_headloss

# Page setup
st.set_page_config(page_title="Hazen-Williams Sensitivity Tool", layout="centered")
st.title("💧 Hazen-Williams Sensitivity Analysis")

st.markdown("This tool calculates headloss using the Hazen-Williams equation and allows sensitivity analysis by varying one parameter at a time.")

# Base inputs
st.subheader("Base Inputs (Hold Constant)")
Q_base = st.number_input("Flow rate Q (cfs)", value=10.0)
C_base = st.number_input("Hazen-Williams C coefficient", value=130.0)
D_base = st.number_input("Pipe diameter D (inches)", value=12.0)
L_base = st.number_input("Pipe length L (ft)", value=1000.0)

# Convert inches to feet
D_base_ft = D_base / 12

# Sensitivity variable
st.subheader("Sensitivity Variable")
variable = st.selectbox("Choose a variable to analyze:", ["Q", "C", "D", "L"])

min_val = st.number_input(f"Minimum value for {variable}", value=5.0)
max_val = st.number_input(f"Maximum value for {variable}", value=20.0)
steps = st.slider("Number of steps", min_value=5, max_value=100, value=20)

# Generate data
vals = np.linspace(min_val, max_val, steps)
results = []

for val in vals:
    Q = Q_base
    C = C_base
    D = D_base_ft
    L = L_base

    if variable == "Q":
        Q = val
    elif variable == "C":
        C = val
    elif variable == "D":
        D = val / 12  # Convert to feet
    elif variable == "L":
        L = val

    hL = calculate_headloss(Q, C, D, L)
    results.append((val, hL))

df = pd.DataFrame(results, columns=[f"{variable}", "Headloss (ft)"])

# Plotting
st.subheader("📉 Sensitivity Plot")
fig, ax = plt.subplots()
ax.plot(df[variable], df["Headloss (ft)"], marker='o')
ax.set_xlabel(variable)
ax.set_ylabel("Headloss (ft)")
ax.set_title(f"Effect of {variable} on Headloss")
ax.grid(True)
st.pyplot(fig)

# Download
st.subheader("📥 Download Results")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name='sensitivity_results.csv', mime='text/csv')

# Show table
with st.expander("Show Data Table"):
    st.dataframe(df)
