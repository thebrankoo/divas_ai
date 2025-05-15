from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Food(BaseModel):
    name: str = Field(description="Food name")
    quantity: str = Field(description="Quantity of the food")
    calories: int = Field(description="Calories of the food")
    protein: int = Field(description="Protein of the food")
    carbs: int = Field(description="Carbs of the food")
    fat: int = Field(description="Fat of the food")

class Meal(BaseModel):
    name: str = Field(description="Meal name")
    calories: int = Field(description="Calories of the meal representing the sum of all foods calories in the meal")
    protein: int = Field(description="Protein of the meal representing the sum of all foods protein in the meal")
    carbs: int = Field(description="Carbs of the meal representing the sum of all foods carbs in the meal")
    fat: int = Field(description="Fat of the meal representing the sum of all foods fat in the meal")
    foods: List[Food] = Field(description="List of foods in the meal")

class DailyDietPlan(BaseModel):
    calories: int = Field(description="Calories of the daily diet plan representing the sum of all meals calories")
    protein: int = Field(description="Protein of the daily diet plan representing the sum of all meals protein")
    carbs: int = Field(description="Carbs of the daily diet plan representing the sum of all meals carbs")
    fat: int = Field(description="Fat of the daily diet plan representing the sum of all meals fat")
    meals: List[Meal] = Field(description="List of meals in the daily diet plan")