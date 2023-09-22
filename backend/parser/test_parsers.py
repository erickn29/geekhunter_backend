from datetime import datetime

from parser.hh_parser import HHParser
from parser.schema import VacanciesList


def test_hh() -> VacanciesList:
    """Функция для тестирования парсера hh.ru"""
    print('run hh parser')
    parser = HHParser()
    return parser.get_all_vacancies(test=True, vacancies_count=5)


def main(wright_to_file: bool = True) -> VacanciesList:
    """Функция для тестирования парсеров"""
    print('run main func')
    hh_result = test_hh()
    if wright_to_file:
        with open(
            f'test_{datetime.strftime(datetime.now(), "%d_%m_%Y")}.json',
            'w',
            encoding='utf-8'
        ) as f:
            f.write(hh_result.model_dump_json())
    print('Test is done!')
    return hh_result


if __name__ == '__main__':
    main(wright_to_file=True)
