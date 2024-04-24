import streamlit as st
from data_helper import *
from calculator import calculate_macronutrients
from api import answer

# Set page title and subtitle
st.title("Macronutrient planner")
st.markdown("University of St. Gallen - Computer Science 9.1")
st.markdown(
    "Creators: Theo Rostalski, Felix Höner, Justus Rahlf, Loredana Salvi, Moritz Müller, Richard Blanc, Fabian von Widdern"
)

# Create input fields for calculating the macronutrient distribution
gender = st.selectbox(
    "Geschlecht", gender_list, index=gender_list.index(user["gender"])
)
age = st.number_input("Alter", min_value=5, max_value=120, step=1, value=user["age"])
weight = st.number_input(
    "Gewicht (kg)", min_value=1, max_value=500, step=1, value=user["weight"]
)
height = st.number_input(
    "Größe (cm)", min_value=1, max_value=300, step=1, value=user["height"]
)
activity_level = st.selectbox(
    "Aktivitätslevel",
    activity_levels,
    index=activity_levels.index(user["activity_level"]),
)
goal = st.selectbox("Ziel", goals, index=goals.index(user["goal"]))

# Display an empty table for results using placeholder
empty_result_table = {
    "Kalorien": 0,
    "Protein (g)": 0,
    "Fett (g)": 0,
    "Kohlenhydrate (g)": 0,
}
result_table_placeholder = st.empty()
result_table_placeholder.table(empty_result_table)


# Create button for handling the data and calculation
if st.button("Berechne"):
    # Update user dictionary with new values
    user["gender"] = gender
    user["age"] = age
    user["weight"] = weight
    user["height"] = height
    user["activity_level"] = activity_level
    user["goal"] = goal

    # Call function to perform calculations
    result = calculate_macronutrients(user)

    # Display results in the table
    result_table_placeholder.table(result)

    st.json(
        answer(
            result["Kalorien"],
            result["Kohlenhydrate"],
            result["Proteine"],
            result["Fette"],
        )
    )
