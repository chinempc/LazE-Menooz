from pydantic import BaseModel
from app.Models.meal_period import MealPeriod


class DailyMeals(BaseModel):
    day: str = None
    meals: MealPeriod = None
