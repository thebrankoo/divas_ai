import os
import json
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import fooddatacentral as fdc

# Load environment variables
load_dotenv()

class NutritionSearch:
    """Tool for searching macronutrient information using the USDA FoodData Central API."""
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_food_details",
                "description": "Get nutritional information for a specific food.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "food_name": {"type": "string", "description": "Name of the food to search nutritional information for"},
                    },
                    "required": ["food_name"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
    ]

    def __init__(self):
        """Initialize the NutritionSearch tool with an API key."""
        self.api_key = os.getenv("FDC_API_KEY")
        if not self.api_key:
            raise ValueError("FDC_API_KEY not found in environment variables")
    
    def search_food(self, query: str, max_results: int = 5):
        """Search for foods matching the query."""
        try:
            results = fdc.search(self.api_key, query)
            return results.head(max_results)
        except Exception as e:
            print(f"Error searching for food: {e}")
            return None
    
    def get_nutrients(self, fdc_id: int):
        """Get nutritional information for a specific food."""
        try:
            nutrients = fdc.nutrients(self.api_key, fdc_id=fdc_id)
            print(f"@@@ Nutrients: {nutrients}")
        except Exception as e:
            print(f"Error getting nutrients: {e}")
            return None
    
    def get_food_details(self, food_name: str):
        """Search for and return detailed nutrition information for a food."""
        search_results = self.search_food(food_name, max_results=1)
        
        if search_results is None or search_results.empty:
            return None

        fdc_id = int(search_results.iloc[0]["fdcId"])
        food_nutrients = search_results.iloc[0]["foodNutrients"]
        
        # Extract macronutrients of interest
        macros = {}
        
        for nutrient in food_nutrients:
            name = nutrient["nutrientName"].lower()
            value = float(nutrient["value"])
            unit = nutrient["unitName"]
            
            if "protein" in name:
                macros["protein"] = {
                    "amount": value,
                    "unit": unit
                }
            elif "carbohydrate, by difference" in name:
                macros["carbs"] = {
                    "amount": value,
                    "unit": unit
                }
            elif "total lipid (fat)" in name:
                macros["fat"] = {
                    "amount": value,
                    "unit": unit
                }
            elif "energy" in name and unit == "KCAL":
                macros["calories"] = {
                    "amount": value,
                    "unit": "kcal"
                }
        
        return {
            "food_name": str(food_name),
            "fdc_id": int(fdc_id),
            "description": str(search_results.iloc[0].get("description", food_name)),
            "macros": macros,
            "found": True
        }

# Test code
# if __name__ == "__main__":
#     load_dotenv()
#     search = NutritionSearch()
#     result = search.get_food_details("large egg")
#     print("\nDataFrame Info:")
#     print(result)