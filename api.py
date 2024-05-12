from json import loads
from os import environ

# pip install openai -> This is the OpenAI API we use
from openai import OpenAI

# pip install dotenv -> This is to load the .env file
from dotenv import load_dotenv


load_dotenv()

# Initialize OpenAI client using the OPEN_API_KEY from the .env file. https://www.freecodecamp.org/news/heres-how-you-can-actually-use-node-environment-variables-8fdf98f53a0a/#:~:text=env%20files%20allow%20you%20to,in%20there%20on%20different%20lines.&text=To%20read%20these%20values%2C%20there,the%20dotenv%20package%20from%20npm.
client = OpenAI(
    api_key=environ.get("OPENAI_API_KEY"),
)


# Define function to create a dict with meal ideas from calories, carbs, proetin and fat
def answer(cal, carbs, protein, fat):
    # First part of question asked to chatgpt
    input_content = f"For the exact amount of given macronutrients: {cal}cal, {carbs}g carbs, {protein}g protein and {fat}g fat, create three diverse meal suggestions (breakfast, lunch and dinner) for a day. Match the calorie requirement exactly (!) and use foods from various kitchens."

    # Second part of question asked to chatgpt
    output_content = """
    Answer in Python parsable JSON, each value should be in german! Only in exactly the following form: {
        "breakfast": {
            meal_title: "", // title of meal
            ingredients: [
            {
                name: "ingredient 1", // name of ingredient
                amount: "amount", // amount in grams
                calories: 0, // amount of calories
                carbs: 0, // amount of carbs in grams
                protein: 0, // amount of protein in grams
                fat: 0, // amount of fat in grams
            },
            {
                name: "ingredient 2", // name of ingredient
                amount: "amount", // amount in grams
                calories: 0, // amount of calories
                carbs: 0, // amount of carbs in grams
                protein: 0, // amount of protein in grams
                fat: 0, // amount of fat in grams
            },
            ...
        ]},
        "lunch": {...},
        "dinner": {...}
    }
    """

    # Add both question strings together
    content = input_content + output_content

    # Ask chatgpt (using an API) https://www.geeksforgeeks.org/how-to-use-chatgpt-api-in-python/
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": content}],
        response_format={"type": "json_object"},
    )

    return loads(completion.choices[0].message.content)
