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
    input_content = f"For the given calories: {cal}cal, carbs: {carbs}g, protein: {protein}g, fat: {fat}g, create three diverse meal suggestions (breakfast, lunch and dinner) for a day which fits the requirement."

    # Second part of question asked to chatgpt
    output_content = """
    Answer in Python parsable JSON only in exactly the following form: {
        "breakfast": {
            meal_title: "", // title of meal
            ingredients: [
            {
                name: "ingredient 1", // name of ingredient
                amount: "amount", // amount in european measurment units
                calories: 0, // amount of calories
                carbs: 0, // amount of carbs in grams
                protein: 0, // amount of protein in grams
                fat: 0, // amount of fat in grams
            },
            {
                name: "ingredient 2", // name of ingredient
                amount: "amount", // amount in european measurment units
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
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
    )

    # Return the result but change it into a dict as it is a string initially
    return loads(completion.choices[0].message.content)
