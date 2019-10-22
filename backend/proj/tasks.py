from __future__ import absolute_import, unicode_literals
from .celery import app
from celery.utils.log import get_task_logger

from models.food_list import Food_List_Model
from models.food import Food
from models.user import UserModel

import requests

@app.task
def get_user_data(*args):
    try:
        response = requests.get('https://randomuser.me/api/')
        response.raise_for_status() # if response is successful
    except HTTPError as http_err:
        print(f'HTTP error occurred in get_user_data: {http_err}')
    except Exception as err:
        print(f'Other error occurred in get_user_data: {err}')
    else:
     return response.json()

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
