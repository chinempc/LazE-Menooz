from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Utilities.menu_bot import MenuBot
from app.Config.config import laze
from app.Schemas.schemas import serialize_daily_meals, deserialize_weekly
from app.Models.weekly_data import WeeklyData

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/{food_item}")
async def get_food_item(food_item: str):
    bot = MenuBot("umes", food_item)
    return bot.get_menu_data()


@app.get("/api/v2/{food_item}")
async def get_food_item(food_item: str):
    response = []
    input_start_date = "2024-08-04"

    # Define the aggregation pipeline
    pipeline = [
        {"$match": {"start_date": input_start_date}},
        {"$project": {"daily_meals": {"$objectToArray": "$daily_meals"}}},
        {"$unwind": "$daily_meals"},
        {"$match": {
            "$or": [
                {"daily_meals.v.meals.lunch": {"$regex": food_item.capitalize(), "$options": "i"}},
                {"daily_meals.v.meals.dinner": {"$regex": food_item.capitalize(), "$options": "i"}}
            ]
        }},
        {"$project": {
            "day": "$daily_meals.k",
            "meals": {
                "lunch": {
                    "$cond": {
                        "if": {
                            "$regexMatch": {"input": "$daily_meals.v.meals.lunch", "regex": food_item.capitalize(), "options": "i"}},
                        "then": "$daily_meals.v.meals.lunch",
                        "else": "$$REMOVE"
                    }
                },
                "dinner": {
                    "$cond": {
                        "if": {"$regexMatch": {"input": "$daily_meals.v.meals.dinner", "regex": food_item.capitalize(),
                                               "options": "i"}},
                        "then": "$daily_meals.v.meals.dinner",
                        "else": "$$REMOVE"
                    }
                }
            }
        }}
    ]

    # Execute the query
    documents = laze.aggregate(pipeline)
    for i in documents:
        i['day'] = datetime.strptime(i['day'], '%Y-%m-%d').strftime('%A')
        response.append(serialize_daily_meals(i))

    return response



