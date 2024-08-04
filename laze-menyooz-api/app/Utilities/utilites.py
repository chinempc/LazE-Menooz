class Utilities:
    @staticmethod
    def get_pipeline(start_date: str, food_item: str):
        return [
            {"$match": {"start_date": start_date}},
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
                                "$regexMatch": {"input": "$daily_meals.v.meals.lunch", "regex": food_item.capitalize(),
                                                "options": "i"}},
                            "then": "$daily_meals.v.meals.lunch",
                            "else": "$$REMOVE"
                        }
                    },
                    "dinner": {
                        "$cond": {
                            "if": {
                                "$regexMatch": {"input": "$daily_meals.v.meals.dinner", "regex": food_item.capitalize(),
                                                "options": "i"}},
                            "then": "$daily_meals.v.meals.dinner",
                            "else": "$$REMOVE"
                        }
                    }
                }
            }}
        ]
