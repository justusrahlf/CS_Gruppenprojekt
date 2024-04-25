from openai import OpenAI
from os import environ
from dotenv import load_dotenv
from json import loads

load_dotenv()

client = OpenAI(
    api_key=environ.get("OPENAI_API_KEY"),
)


def answer(cal, carbs, protein, fat):
    input_content = f"For the given calories: {cal}cal, carbs: {carbs}g, protein: {protein}g, fat: {fat}g, create three diverse meal suggestions (breakfast, lunch and dinner) for a day which fits the requirement."
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

    content = input_content + output_content

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
    )

    return loads(completion.choices[0].message.content)
