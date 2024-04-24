# Source: https://www.omnicalculator.com/health/bmr-harris-benedict-equation


# Define function to calculate the basal metabolic rate (BMR)
# BMR: Equivalent to the amount of energy, in calories, that your body needs to function if it were to rest for 24 hours
def calculate_bmr(user):
    # Apply formula depending on the gender
    if user["gender"] == "Männlich":
        bmr = (10 * user["weight"]) + (6.25 * user["height"]) - (5 * user["age"]) + 5
    else:
        bmr = (10 * user["weight"]) + (6.25 * user["height"]) - (5 * user["age"]) - 161

    # Return the BMR
    return bmr


# Define function to calculate total daily energy expenditure (TDEE)
# TDEE: Equivalent to the number of calories you burn throughout a 24-hour period
def calculate_tdee(user):
    # Define activity level factors
    activity_level_factors = {
        "Sitzend": 1.2,
        "Leicht aktiv": 1.375,
        "Mäßig aktiv": 1.55,
        "Sehr aktiv": 1.725,
    }

    # Get BMR
    bmr = calculate_bmr(user)

    # Apply the Harris-Benedict equation revised by Mifflin and St Jeor (https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation)
    tdee = bmr * activity_level_factors[user["activity_level"]]

    # Return TDEE
    return tdee


# Define function to calculate the macronutrient distribution
def calculate_macronutrients(user):
    # Get the TDEE
    tdee = calculate_tdee(user)

    # Define macronutrient distribution based on the goal
    if user["goal"] == "Gewichtsverlust":
        # For weight loss, typically aim for a deficit of 500 calories per day
        calorie_deficit = 500
        adjusted_tdee = tdee - calorie_deficit

        # Set macronutrient distribution percentages
        carb_percentage = 40
        protein_percentage = 30
        fat_percentage = 30
    elif user["goal"] == "Muskelzuwachs":
        # For muscle gain, typically aim for a slight surplus of calories
        calorie_surplus = 200
        adjusted_tdee = tdee + calorie_surplus

        # Set macronutrient distribution percentages
        carb_percentage = 50
        protein_percentage = 30
        fat_percentage = 20
    else:
        # For maintaining fitness, maintain TDEE
        adjusted_tdee = tdee

        # Set macronutrient distribution percentages
        carb_percentage = 45
        protein_percentage = 25
        fat_percentage = 30

    # Calculate macronutrient amounts in grams
    carb_grams = int(
        (adjusted_tdee * carb_percentage) / 100 / 4
    )  # 4 calories per gram of carbs
    protein_grams = int(
        (adjusted_tdee * protein_percentage) / 100 / 4
    )  # 4 calories per gram of protein
    fat_grams = int(
        (adjusted_tdee * fat_percentage) / 100 / 9
    )  # 9 calories per gram of fat

    # Return macronutrient distribution
    return {
        "Kalorien": int(adjusted_tdee),
        "Kohlenhydrate": carb_grams,
        "Proteine": protein_grams,
        "Fette": fat_grams,
    }
