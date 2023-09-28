import time
from typing import NoReturn
import os
from dotenv import load_dotenv

import schedule
import requests


load_dotenv()


def get_parser_request() -> NoReturn:
    """Функция выполняет запрос на url, запускающий парсинг"""
    try:
        response = requests.request(
            'POST',
            'http://127.0.0.1:8000/api/v1/test/',
            data={'token': os.getenv('PARSER_TOKEN')}
        )
        if response.ok:
            print('Отправили запрос на парсинг')
    except requests.exceptions.RequestException as e:
        print(e)


scheduler = schedule.Scheduler()
scheduler.every().day.at("21:59").do(get_parser_request)


while True:
    scheduler.run_pending()
    time.sleep(1)
