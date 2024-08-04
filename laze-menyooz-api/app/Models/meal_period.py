from pydantic import BaseModel


class MealPeriod(BaseModel):
    lunch: str = None
    dinner: str = None
