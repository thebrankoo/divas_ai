from pydantic import BaseModel
from typing import List, Dict, Optional

class MacroNutrient(BaseModel):
    amount: float
    unit: str

class FoodDetails(BaseModel):
    food_name: str
    fdc_id: int
    description: str
    macros: Dict[str, MacroNutrient]
    found: bool

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