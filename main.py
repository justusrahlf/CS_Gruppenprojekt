import streamlit as st
from data_helper import *
from calculator import calculate_macronutrients
from api import answer
from matplotlib import pyplot as plt
import base64

# Set page title and subtitle
st.title("Macronutrient planner")
st.markdown("University of St. Gallen - Computer Science 9.1")
st.markdown(
    "Creators: Theo Rostalski, Felix Höner, Justus Rahlf, Loredana Salvi, Moritz Müller, Richard Blanc, Fabian von Widdern")

# Function to load and encode the image to base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the image and encode it to base64
image_base64 = get_image_as_base64("logo.png")

# HTML and CSS to position the logo in the upper right corner responsively
st.markdown(
    f"""
    <style>
    .logo-container {{
        position: absolute;
        top: -180px;
        right: 10px;
        z-index: 1;
    }}
    .logo {{
        width: 100px;
        max-width: 100%;
        height: auto;
    }}
    @media (max-width: 600px) {{
        .logo-container {{
            top: 10px;
            right: 10px;
        }}
        .logo {{
            width: 80px;
        }}
    }}
    @media (max-width: 400px) {{
        .logo-container {{
            top: 5px;
            right: 5px;
        }}
        .logo {{
            width: 60px;
        }}
    }}
    
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{image_base64}" class="logo">
    </div>
    """,
    unsafe_allow_html=True
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

# Create columns for layout
col1, col2 = st.columns([1, 1])

# Display an empty table for results using placeholder in column 1
with col1:
    st.header("Nährwerte")
    empty_result_table = {
        "Kalorien": 0,
        "Protein (g)": 0,
        "Fett (g)": 0,
        "Kohlenhydrate (g)": 0,
}
    result_table_placeholder = st.empty()
    result_table_placeholder.table(empty_result_table)

# Create an empty space where we put the pie chart in column 2
with col2:
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
        weights = [result["Kohlenhydrate"],result["Proteine"], result["Fette"] ] #soll sich anpassen an die Berechnung 
        
        fig, ax = plt.subplots()
        space, texts, autotexts = ax.pie(weights, labels=nutritional_value, autopct = "%1.2f%%", startangle = 90, shadow = True, explode = (0.08, 0.08, 0.08),radius=0.8)
        
        for text in texts:
            text.set_fontsize(10)
            text.set_weight('bold')
            
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
    
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
