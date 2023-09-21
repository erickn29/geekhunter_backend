from datetime import datetime
import json
from typing import NoReturn

from parser.hh_parser import HHParser


def test_hh() -> dict:
    """Функция для тестирования парсера hh.ru"""
    print('run hh parser')
    parser = HHParser()
    return parser.get_all_vacancies(test=True, vacancies_count=5)


def main(wright_to_file: bool = False) -> NoReturn:
    """Функция для тестирования парсеров"""
    print('run main func')
    hh_result = test_hh()
    if wright_to_file:
        with open(
            f'test_{datetime.strftime(datetime.now(), "%d_%m_%Y")}.json',
            'w',
            encoding='utf-8'
        ) as f:
            f.write(json.dumps(hh_result, ensure_ascii=False))
    print('Test is done!')


if __name__ == '__main__':
    main(wright_to_file=True)
