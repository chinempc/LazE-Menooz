from datetime import datetime, timedelta
from app.Config.config import laze
from app.Models.daily_meals import DailyMeals
from app.Models.weekly_data import WeeklyData
from app.Models.daily_meals import DailyMeals
from app.Models.meal_period import MealPeriod
from app.Schemas.schemas import serialize_daily_meals
from app.Utilities.utilites import Utilities
import os
import requests
import pytesseract
from PIL import Image
import pathlib
import shutil
from bs4 import BeautifulSoup as bs


class UmesService:
    def __init__(self, food_item):
        self.data = None
        self.food_item = food_item
        # Init start/end of week
        # "start_date": "2024-06-30",
        # "end_date": "2024-07-06"
        self.start_date = (datetime.now() - timedelta(days=datetime.now().weekday() + 1))
        self.end_date = (self.start_date + timedelta(days=6)).strftime("%Y-%m-%d")
        self.start_date = self.start_date.strftime("%Y-%m-%d")

        # Check for this week's data in DB
        responses = laze.aggregate(Utilities.get_pipeline(self.start_date, food_item))
        try:
            result = []
            for response in responses:
                response['day'] = datetime.strptime(response['day'], '%Y-%m-%d').strftime('%A')
                result.append(serialize_daily_meals(response))
            self.mongo_to_objects(result)
        except Exception as e:
            # Check Redis Cache

            # If in neither scrape data from UMES site
            self.menu_dir = os.path.join(os.getcwd(),
                                         f'UMES-Menu~{self.start_date}')
            self.scrape_weekly_data()

    def scrape_weekly_data(self):
        try:
            self.download_menu()
            self.pictures_to_objects()
        except Exception as e:
            self.data = {'serving_period': 'N/A',
                         'serving_day': 'N/A',
                         'served': 'N/A',
                         'message': 'No valid page found'}
            print(f"Failed to scrape weekly data. Error: {e}")

    def download_menu(self):
        day_period_map = {
            3: 'Sunday-Lunch', 4: 'Sunday-Dinner',
            6: 'Monday-Lunch', 7: 'Monday-Dinner',
            9: 'Tuesday-Lunch', 10: 'Tuesday-Dinner',
            12: 'Wednesday-Lunch', 13: 'Wednesday-Dinner',
            15: 'Thursday-Lunch', 16: 'Thursday-Dinner',
            18: 'Friday-Lunch', 19: 'Friday-Dinner',
            21: 'Saturday-Lunch', 22: 'Saturday-Dinner'
        }
        images = ''
        img_normal_view = ("w_1480,h_832,al_c,q_85,usm_0.66_1.00_0.01,"
                           "enc_auto/3bc191_db59f0e42aa74aeaa84ee45887e692dd~mv2.jpg")

        # Reverse cycle through a list of 10 for weeks, as they change all the time and only 1 available
        for week_num in reversed(range(10)):
            url = f'https://www.umes-thscampusdining.com/post/week-{week_num + 1}-menus'
            root_html = bs(requests.get(url).text, "html.parser")

            # THIS MAY CHANGE, as of now invalid pages will have "We Couldn't Find This Page" under this div class
            if root_html.find("div", {'class': 'cJscj1'}):
                continue

            # Grab all images and make image dir if page is valid
            images = root_html.findAll("wow-image")
            os.makedirs(self.menu_dir)
            break

        if not images:
            return False

        for image_num, image in enumerate(images):
            # Skip the first 2 images as and all breakfast images
            if image_num < 2 or (image_num + 1) % 3 == 0:
                continue

            # Download each image from src attr
            image_data = requests.get(image.find("img")["src"].split('w_')[0] + img_normal_view)

            # Naming convention -> UMES-Menu~6-30_7-6/Sunday_Lunch.jpg
            file_name = f"{self.menu_dir}/{day_period_map[image_num]}.jpg"
            image_file = open(file_name, 'wb')

            image_file.write(image_data.content)
            image_file.close()

        return True

    def pictures_to_objects(self):
        # REDO This to match new JSON format

        # Loop through the folder, open and extract text from image by file name, check if food_item is in the data
        menu_images = os.listdir(self.menu_dir)
        day_counter = {
            'Sunday': 0,
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
        }
        found = False
        json_responses = []
        mongo_data = {}

        # Week Data object
        week_data = WeeklyData()
        week_data.start_date = self.start_date
        week_data.end_date = self.end_date

        # Loop through each image
        for menu_num, menu_image in enumerate(menu_images):
            day = menu_image.partition('-')[0]
            current_date = (datetime.strptime(week_data.start_date, "%Y-%m-%d") +
                            timedelta(days=day_counter[day])).strftime("%Y-%m-%d")
            menu_text = pytesseract.image_to_string(Image.open(f"{self.menu_dir}/{menu_image}"), lang='eng')
            curr_meal = MealPeriod(lunch=menu_text.lower())

            # Build Mongo Collection
            # Lunch Data
            if menu_image.partition('-')[2] == 'Lunch':
                mongo_data[current_date] = DailyMeals(day=day, meals=curr_meal)

            # Dinner Data
            else:
                mongo_data[current_date].meals.dinner = curr_meal

            if self.food_item.lower() in menu_text.lower():
                found = True
                json_responses.append(self.create_response_json(found, menu_image))

        # Delete image folder
        self.cleanup_images()

        # Upload Mongo Data
        week_data.daily_meals = mongo_data
        laze.insert_one(week_data.json())

        if not found:
            json_responses.append(self.create_response_json(False))

        self.data = json_responses

    def create_response_json(self, found, menu_image="N/A-N/A"):
        serving_period = menu_image.partition('-')[2].strip('.jpg') if menu_image != 'N/A' else menu_image
        serving_day = menu_image.partition('-')[0] if menu_image != 'N/A' else menu_image
        return {'serving_period': serving_period, 'serving_day': serving_day, 'served': found,
                'message': (f"{self.food_item.capitalize()} will be served for {serving_period} on {serving_day} this "
                            f"week 😃🍽️!!!") if found else f"{self.food_item.capitalize()} will not be served this " +
                                                          f"week 😔."}

    def cleanup_images(self):
        try:
            images_path = pathlib.Path(self.menu_dir)
            shutil.rmtree(images_path)
        except:
            print('Error while cleaning up images')

    def mongo_to_objects(self, responses):
        response_json = []
        found = False

        for daily in responses:
            day = daily['day']
            if "lunch" in daily['meals']:
                found = True
                response_json.append(self.create_response_json(found, f'{day}-Lunch'))

            if "dinner" in daily['meals']:
                found = True
                response_json.append(self.create_response_json(found, f'{day}-Dinner'))

        if not found:
            response_json.append(self.create_response_json(False, self.food_item))

        self.data = response_json
