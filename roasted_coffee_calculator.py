import streamlit as st

# Title
st.title("Roasted Coffee Cost Calculator")

# Input for green coffee cost per kg
gcb_cost = st.number_input("Enter Green Coffee Cost (₱ per kg):", min_value=0.0, step=0.1)

# Constants
green_input_kg = 1.25
electricity_cost_per_kg = 12.32
packaging_cost_per_kg = 25.00

# Calculations
adjusted_gcb_cost = gcb_cost * green_input_kg
total_cost_per_kg = adjusted_gcb_cost + electricity_cost_per_kg + packaging_cost_per_kg

# Suggested retail prices
srp_30 = total_cost_per_kg * 1.30
srp_35 = total_cost_per_kg * 1.35
srp_40 = total_cost_per_kg * 1.40

# Output
if gcb_cost > 0:
    st.markdown("### Results")
    st.write(f"**Adjusted Green Coffee Cost (1.25kg):** ₱{adjusted_gcb_cost:,.2f}")
    st.write(f"**Total Cost per 1kg Roasted Coffee:** ₱{total_cost_per_kg:,.2f}")
    
    st.markdown("### Suggested Retail Prices")
    st.write(f"**+30% Markup:** ₱{srp_30:,.2f}")
    st.write(f"**+35% Markup:** ₱{srp_35:,.2f}")
    st.write(f"**+40% Markup:** ₱{srp_40:,.2f}")
