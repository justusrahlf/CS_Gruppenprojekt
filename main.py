import streamlit as st
from data_helper import *
from calculator import calculate_macronutrients
from api import answer
from matplotlib import pyplot as plt

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
st.header("Nährwerte")
result_table_placeholder = st.empty()
result_table_placeholder.table(empty_result_table)

piechart = st.empty()

# Create an empty space where we put the meal
menu_vorschlag = st.empty()

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
    with piechart.container():
      
        # Data for the visualisation
        
        # Data for Graph 1
        nutritional_value = ["Kohlenhydrate", "Proteine", "Fette"]
        weights = [result["Kohlenhydrate"],result["Proteine"], result["Fette"] ]
        
        # Data for Graph 2
        own_calories = result["Kalorien"]
        durchschnitt_kalorien_schweiz = 2573  # Durchschnittliche tägliche Kalorienaufnahme laut Statista
        kalorien_daten = [own_calories, durchschnitt_kalorien_schweiz]
        labels = ['Eigene Kalorien', 'Durchschnitt Schweiz']
       
        # Creating a figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5)) 
        fig.subplots_adjust(wspace=0.5)
       
        # Determine the font size of the labels
        fontsize_for_labels = 10 
 
        # Creating the Piechart
        space, texts, autotexts = ax1.pie(weights, labels=nutritional_value, autopct = "%1.2f%%", startangle = 90, shadow = True, explode = (0.08, 0.08, 0.08))
        ax1.set_title('Aufteilung der Nährwerte', fontweight='bold')
       
        for text in texts:
            text.set_fontsize(fontsize_for_labels)
            text.set_weight('bold')
           
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(fontsize_for_labels)
            autotext.set_weight('bold')
       
        # Creating the Bar Chart
        ax2.bar(labels, kalorien_daten, color = ['blue', 'green'])
        ax2.set_title('Durchschnittlich weltweiter vergleich deiner Kalorien', fontweight = "bold") 
        ax2.set_ylabel('Kalorien', fontdict={'weight': 'bold'}) #set_ylabel erwartet ein dic
        ax2.set_xticklabels(labels,fontsize = fontsize_for_labels, fontweight = 'bold')
      
        #Showig both Graphs
        st.pyplot(fig)

    # Ask Chatgpt
    with st.spinner():
        data = answer(
            result["Kalorien"],
            result["Kohlenhydrate"],
            result["Proteine"],
            result["Fette"],
        )

    # Replace the empty space with the menu: https://docs.streamlit.io/develop/api-reference/layout/st.empty
    with menu_vorschlag.container():
        st.header("Dein Menüvorschlag")
        st.subheader("Frühstück: " + data["breakfast"]["meal_title"])
        for food in data["breakfast"]["ingredients"]:
            st.markdown(
                food["name"]
                + " ("
                + food["amount"]
                + "): "
                + str(food["calories"])
                + "Kalorien, "
                + str(food["carbs"])
                + "g Kohlenhydrate, "
                + str(food["protein"])
                + "g Protein, "
                + str(food["fat"])
                + "g Fett"
            )

        st.subheader("Mittagessen: " + data["lunch"]["meal_title"])
        for food in data["lunch"]["ingredients"]:
            st.markdown(
                food["name"]
                + " ("
                + food["amount"]
                + "): "
                + str(food["calories"])
                + "Kalorien, "
                + str(food["carbs"])
                + "g Kohlenhydrate, "
                + str(food["protein"])
                + "g Protein, "
                + str(food["fat"])
                + "g Fett"
            )

        st.subheader("Abendessen: " + data["dinner"]["meal_title"])
        for food in data["dinner"]["ingredients"]:
            st.markdown(
                food["name"]
                + " ("
                + food["amount"]
                + "): "
                + str(food["calories"])
                + "Kalorien, "
                + str(food["carbs"])
                + "g Kohlenhydrate, "
                + str(food["protein"])
                + "g Protein, "
                + str(food["fat"])
                + "g Fett"
            )
