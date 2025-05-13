import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

class Food(BaseModel):
    name: str
    quantity: str
    calories: int
    protein: int
    carbs: int
    fat: int

class Meal(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int
    foods: List[Food]

class DailyDietPlan(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int
    meals: List[Meal]

if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

isLoaded = load_dotenv()


if not isLoaded:
    raise ValueError("Failed to load environment variables")
else:
    print("Environment variables loaded successfully")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.beta.chat.completions.parse(
    model="gpt-4.1-2025-04-14",
    messages=[
        {"role": "system", "content": "You are nutritionists expert."},
        {"role": "user", "content": "Give me daily diet plan for 35 year old male. Total daily calories intake should ne 2300cal and protein intake should be minium 200g"}
        ],
        response_format=DailyDietPlan
)

daily_diet_plan = completion.choices[0].message.parsed
print(daily_diet_plan.model_dump_json(indent=2))