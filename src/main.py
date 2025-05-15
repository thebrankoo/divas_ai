import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from models import DailyDietPlan
from nutrition_search import NutritionSearch

if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

isLoaded = load_dotenv()

if not isLoaded:
    raise ValueError("Failed to load environment variables")
else:
    print("Environment variables loaded successfully")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize nutrition search tool
try:
    nutrition_tool = NutritionSearch()
    print("Nutrition search tool initialized successfully")
except ValueError as e:
    print(f"Warning: {e}")
    print("Continuing without nutrition search capability")
    nutrition_tool = None

# Step 1: Generate a basic diet plan
system_prompt = """
You are a nutritionist expert who generates accurate, realistic meal plans in JSON format. Always ensure:
- The sum of all foods in each meal matches the meal’s totals for calories, protein, carbs, and fat.
- The sum of all meals matches the top-level daily totals.
- All nutritional values must be mathematically correct and based on realistic food data.
- Include multiple meals with specific foods, exact quantities (e.g., grams, ml), and detailed macronutrient values.
- The plan must meet the user's target for total calories and macronutrient distribution (e.g., protein, carbs, fat).
Avoid rounding errors, missing values, or hallucinated ingredients or quantities.
"""

user_prompt = """
Create a daily diet plan that includes exactly 3 meals.
- Total daily calories must be not greater than 2300 kcal
- Minimum total protein must be not less than 200g

Each meal must list foods with their quantities and a full macronutrient breakdown (calories, protein, carbs, fat).

Ensure that:
- The sum of all foods protein,fat, carbs and calories in a meal matches the meal’s totals protein,fat, carbs and calories
- The sum of all meals protein,fat, carbs and calories matches the daily totals protein, fat, carbs and calories
- All values are accurate and based on realistic food data
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

completion = client.chat.completions.create(
    model="gpt-4.1-2025-04-14",
    messages=messages,
    tools=nutrition_tool.tools,
    temperature=0,
    top_p=1
)

completion.model_dump()

def call_function(name, args):
    print(f"Calling function: {name} with args: {args}")
    if name == "get_food_details":
        return nutrition_tool.get_food_details(**args)

messages.append(completion.choices[0].message)

for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    result = call_function(name, args)

    if result == None:
        print(f"No matching foods found in database for tool call: {tool_call.id}")
    else:
        messages.append({
            "role": "tool", 
            "tool_call_id": tool_call.id, 
            "content": json.dumps(result)
        })
        
print("Generating diet plan...")

completion_2 = client.beta.chat.completions.parse(
    model="gpt-4.1-2025-04-14",
    messages=messages ,
    tools=nutrition_tool.tools,
    response_format=DailyDietPlan
)

final_response = completion_2.choices[0].message.parsed
print(final_response.model_dump_json(indent=2))