# This is the base class
from app.Services.umes_service import UmesService


class MenuBot:
    def __init__(self, school: str, food_item: str):
        self.school_list = ['umes']
        self.current_school = None
        self.data = None

        self.get_menu(school, food_item)

    def get_menu(self, school: str, food_item: str):
        if school not in self.school_list:
            self.data = [{'serving_period': 'N/A',
                          'serving_day': 'N/A',
                          'served': 'N/A',
                          'message': 'Invalid school'}]
            return

        if school.lower() == 'umes':
            self.current_school = UmesService(food_item)

    def get_menu_data(self) -> list[dict]:
        return self.current_school.data if not self.data else self.data
