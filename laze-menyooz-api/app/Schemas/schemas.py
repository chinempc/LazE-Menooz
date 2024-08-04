from app.Models.weekly_data import WeeklyData
from app.Models.daily_meals import DailyMeals
from app.Models.meal_period import MealPeriod


# Serializers: JSON -> Object | Bracket Notation []
def serialize_weekly(weekly_data: dict):
    return WeeklyData(
        start_date=weekly_data['start_date'],
        end_date=weekly_data['end_date'],
        daily_meals=serialize_daily_meals_multi(weekly_data['daily_meals']),
    )


def serialize_daily_meals_multi(daily_meals: dict):
    data = {}
    for daily in daily_meals:
        data[daily] = serialize_daily_meals(daily_meals[daily])
    return data


def serialize_daily_meals(daily_meals):
    return {
        "day": daily_meals['day'],
        "meals": serialize_meal_period(daily_meals["meals"])
    }


def serialize_meal_period(meal_period):
    if "lunch" in meal_period and "dinner" in meal_period:
        return {
            "lunch": meal_period["lunch"],
            "dinner": meal_period["dinner"]
        }
    elif "lunch" in meal_period:
        return {
            "lunch": meal_period["lunch"]
        }
    elif "dinner" in meal_period:
        return {
            "dinner": meal_period["dinner"]
        }


# Deserializers: Object -> JSON | Dot Notation .

# Week Data
def deserialize_weekly(weekly_data: WeeklyData):
    return {
        "start_date": weekly_data.start_date,
        "end_date": weekly_data.end_date,
        "daily_meals": deserialize_daily_meals_multi(weekly_data.daily_meals),
    }


def deserialize_daily_meals_multi(daily_meals):
    data = {}
    for daily in daily_meals:
        data[daily] = deserialize_daily_meals(daily_meals[daily])
    return data


def deserialize_daily_meals(daily_meals: DailyMeals):
    return {
        "day": daily_meals.day,
        "meals": deserialize_meal_period(daily_meals.meals)
    }


def deserialize_meal_period(meal_period: MealPeriod):
    return {
        "lunch": meal_period.lunch,
        "dinner": meal_period.dinner
    }
