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