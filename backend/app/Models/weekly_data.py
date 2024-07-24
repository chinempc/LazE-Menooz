from pydantic import BaseModel
from app.Models.daily_meals import DailyMeals


class WeeklyData(BaseModel):
    start_date: str = None
    end_date: str = None
    daily_meals: dict[str, DailyMeals] = None
