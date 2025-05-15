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
You are a nutritionist expert tasked with creating a daily diet plan.
The plan should include multiple meals with specific foods, quantities, and macronutrient information.
Ensure the plan meets the user's requirements for total calories and macronutrient distribution.
"""

user_prompt = """
Give me daily diet plan for 35 year old male. 
Total daily calories intake should be 2300cal and protein intake should be minimum 200g
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_food_details",
#             "description": "Get nutritional information for a specific food.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "food_name": {"type": "string", "description": "Name of the food to search nutritional information for"},
#                 },
#                 "required": ["food_name"],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     }
# ]

completion = client.chat.completions.create(
    model="gpt-4.1-2025-04-14",
    messages=messages,
    tools=nutrition_tool.tools,
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
    
    print(f"@@JSON DUMP: {json.dumps(result)} for tool call: {tool_call.id}")
    messages.append({
        "role": "tool", 
        "tool_call_id": tool_call.id, 
        "content": json.dumps(result)
     })
        

# First, get a basic diet plan
completion_2 = client.beta.chat.completions.parse(
    model="gpt-4.1-2025-04-14",
    messages=messages ,
    tools=nutrition_tool.tools,
    response_format=DailyDietPlan
)

final_response = completion_2.choices[0].message.parsed
print(final_response.model_dump_json(indent=2))

# basic_diet_plan = completion.choices[0].message.parsed
# basic_diet_plan = DailyDietPlan(
#     calories=2300,
#     protein=200,
#     carbs=0,
#     fat=0,
#     meals=[
#         Meal(
#             name="Breakfast",
#             calories=500,
#             protein=50,
#             carbs=0,
#             fat=0,
#             foods=[
#                 Food(
#                     name="Eggs",
#                     quantity="2",
#                     calories=100,
#                     protein=10,
#                     carbs=0,
#                     fat=0
#                 )
#             ]
#         )
#     ]
# )

# # Step 2: If nutrition tool is available, enhance the diet plan with real nutrition data
# if nutrition_tool:
#     print("Enhancing diet plan with real nutrition data...")
#     enhanced_meals = []
    
#     for meal in basic_diet_plan.meals:
#         enhanced_foods = []
#         for food in meal.foods:
#             # Look up real nutrition data
#             print(f"Looking up nutrition data for {food.name}")
#             food_details = nutrition_tool.get_food_details(food.name)
            
#             if food_details["found"] and "macros" in food_details:
#                 macros = food_details["macros"]
#                 # Update food with real nutrition data
#                 enhanced_foods.append(Food(
#                     name=food_details["description"],
#                     quantity=food.quantity,
#                     calories=int(macros.get("calories", {}).get("amount", food.calories)),
#                     protein=int(macros.get("protein", {}).get("amount", food.protein)),
#                     carbs=int(macros.get("carbs", {}).get("amount", food.carbs)),
#                     fat=int(macros.get("fat", {}).get("amount", food.fat))
#                 ))
#             else:
#                 # Keep original food if not found
#                 enhanced_foods.append(food)
        
#         # Calculate updated meal totals
#         total_calories = sum(food.calories for food in enhanced_foods)
#         total_protein = sum(food.protein for food in enhanced_foods)
#         total_carbs = sum(food.carbs for food in enhanced_foods)
#         total_fat = sum(food.fat for food in enhanced_foods)
        
#         enhanced_meals.append(Meal(
#             name=meal.name,
#             calories=total_calories,
#             protein=total_protein,
#             carbs=total_carbs,
#             fat=total_fat,
#             foods=enhanced_foods
#         ))
    
#     # Calculate updated daily totals
#     total_calories = sum(meal.calories for meal in enhanced_meals)
#     total_protein = sum(meal.protein for meal in enhanced_meals)
#     total_carbs = sum(meal.carbs for meal in enhanced_meals)
#     total_fat = sum(meal.fat for meal in enhanced_meals)
    
#     # Create enhanced diet plan
#     enhanced_diet_plan = DailyDietPlan(
#         calories=total_calories,
#         protein=total_protein,
#         carbs=total_carbs,
#         fat=total_fat,
#         meals=enhanced_meals
#     )
    
#     print("Diet plan enhanced with real nutrition data")
#     print(enhanced_diet_plan.model_dump_json(indent=2))
# else:
#     # Use the basic diet plan if nutrition tool is not available
#     print(basic_diet_plan.model_dump_json(indent=2))