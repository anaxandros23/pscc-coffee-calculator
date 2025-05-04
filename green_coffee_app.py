import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Green Coffee Cost Calculator", layout="centered")
st.title("☕ Green Coffee Cost Calculator")

st.markdown("""
Enter the details for each green coffee origin below. This calculator will account for:
- Volume loss (18% for parchment, 45% for dry naturals)
- Fixed ₱10/kg hulling service fee
- Additional fuel or handling costs
- Final cost is based on usable post-hulling volume
""")

# Default Data
initial_data = pd.DataFrame({
    "Origin": ["Nueva Vizcaya", "Sagada", "Kiangan"],
    "Weight (kg)": [1000, 50, 281],
    "Price per kg (₱)": [320, 450, 430],
    "Processing Type": ["", "Parchment", "Parchment"],
    "For Hulling": [False, True, True],
    "Additional Costs (₱)": [0, 0, 0],
})

input_df = st.data_editor(
    initial_data,
    column_config={
        "Processing Type": st.column_config.SelectboxColumn(
            "Processing Type",
            options=["Parchment", "Dry Natural"]
        )
    },
    num_rows="dynamic",
    use_container_width=True
)

# Processing loss rates
loss_rates = {"Parchment": 0.18, "Dry Natural": 0.45}

if st.button("Calculate Blended Cost"):
    summary = []
    total_cost = 0
    total_final_volume = 0

    for _, row in input_df.iterrows():
        origin = row["Origin"]
        weight = row["Weight (kg)"]
        price = row["Price per kg (₱)"]
        proc_type = row["Processing Type"]
        for_hulling = row["For Hulling"]
        addl_costs = row["Additional Costs (₱)"]

        purchase_total = weight * price
        hulling_fee = weight * 10 if for_hulling else 0
        loss_rate = loss_rates[proc_type] if for_hulling and proc_type in loss_rates else 0

        final_volume = weight * (1 - loss_rate)
        total_with_addl = purchase_total + hulling_fee + addl_costs
        final_cost_per_kg = total_with_addl / final_volume if final_volume else 0

        total_cost += total_with_addl
        total_final_volume += final_volume

        summary.append({
            "Origin": origin,
            "Input Weight (kg)": round(weight, 2),
            "Loss Rate (%)": int(loss_rate * 100),
            "Final Volume (kg)": round(final_volume, 2),
            "Total Cost (₱)": round(total_with_addl, 2),
            "Cost per Final kg (₱)": round(final_cost_per_kg, 2),
        })

    blended_cost = total_cost / total_final_volume if total_final_volume else 0

    st.subheader("📊 Cost Summary")
    summary_df = pd.DataFrame(summary)
    st.dataframe(summary_df)
    st.success(f"☕ Blended Green Coffee Cost: ₱{blended_cost:.2f} per kg")

    # CSV download
    csv = summary_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Summary as CSV",
        data=csv,
        file_name="green_coffee_summary.csv",
        mime="text/csv"
    )
