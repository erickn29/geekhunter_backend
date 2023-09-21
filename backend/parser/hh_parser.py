import re
import time

import requests
from requests import request
from tqdm import tqdm
from bs4 import BeautifulSoup

from .base_parser import BaseParser
from .analyzer import Analyzer


class HHParser(BaseParser):
    """Парсер для hh.ru"""

    LINK = BaseParser.HH_LINK

    def __init__(self) -> None:
        super().__init__(url=self.LINK)

    def _get_num_pages(self, text: str) -> int:
        """Метод возвращает количество страниц с вакансиями"""
        counter = 0
        if text:
            time.sleep(self.sleep_time)
            elements_list = re.findall(r'pager-page-wrapper-\d+-\d+', text)

            if elements_list:
                for el in tqdm(elements_list):
                    last_el = int(el.split('-')[-1]) + 1
                    if last_el > counter:
                        counter = last_el
        return counter

    def _get_vacancies_links(self, pages: list[str]) -> list[str]:
        """Получаем список ссылок на вакансии"""
        links_list = []
        watched = []
        print(f'\nСобираем ссылки на вакансии со страниц {self.source_name}')
        for page in tqdm(pages):
            try:
                response = request(
                    method='GET', url=page, headers=self.headers
                )
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    blocks = soup.find_all('div', {'class': 'serp-item'})
                    for block in blocks:
                        block_title = block.find_all_next(
                            'a', {'data-qa': 'serp-item__title'}
                        )[0].text
                        block_salary = block.find_all_next(
                            'span',
                            {'data-qa': 'vacancy-serp__vacancy-compensation'}
                        )[0].text
                        block_company = block.find_all_next(
                            'a',
                            {'data-qa': 'vacancy-serp__vacancy-employer'}
                        )[0].text
                        block_link = block.find_all_next(
                            'a',
                            {'data-qa': 'serp-item__title'}
                        )[0]['href']
                        watched.append(
                            (block_title, block_salary, block_company)
                        )
                        if len(watched) > 1 and (
                            (block_title, block_salary, block_company)
                            not in watched[:-1]
                        ) and not (
                            set(
                                block_title.lower().split()
                            ) & set(self.STOP_WORDS)
                        ):
                            links_list.append(block_link)
                    time.sleep(self.sleep_time)
            except requests.exceptions.RequestException:
                print(f'Не смог обработать страницу {page}')
        return links_list

    def _get_vacancy_data(self, page: str, link: str) -> dict:
        """Метод возвращает информацию о вакансии"""
        if page:
            try:
                soup = BeautifulSoup(page, 'html.parser')
                title = self.string_cleaner(
                    soup.find('h1', {'data-qa': "vacancy-title"}).text
                )
                salary = self.string_cleaner(
                    soup.find('div', {'data-qa': 'vacancy-salary'}).text
                ).replace('на руки', '').replace('до вычета налогов', '')
                salary_from = None
                salary_to = None
                experience = None
                # text = ''
                new_text = ''
                stack = None
                company = ''
                company_address = ''
                is_remote = False
                if 'руб' in salary or '₽' in salary:
                    if 'от' in salary and 'до' not in salary:
                        salary_from = int(
                            ''.join([i for i in salary if i.isdigit()])
                        )
                    if 'до' in salary and 'от' not in salary:
                        salary_to = int(
                            ''.join([i for i in salary if i.isdigit()])
                        )
                    if 'от' in salary and 'до' in salary:
                        salary_list = salary.split('до')
                        salary_from = int(
                            ''.join([i for i in salary_list[0] if i.isdigit()])
                        )
                        salary_to = int(
                            ''.join([i for i in salary_list[1] if i.isdigit()])
                        )
                if 'USD' in salary or 'EUR' in salary:
                    if 'от' in salary and 'до' not in salary:
                        salary_from = int(
                            ''.join([i for i in salary if i.isdigit()])
                        ) * self.course_rate
                    if 'до' in salary and 'от' not in salary:
                        salary_to = int(
                            ''.join([i for i in salary if i.isdigit()])
                        ) * self.course_rate
                    if 'от' in salary and 'до' in salary:
                        salary_list = salary.split('до')
                        salary_from = int(
                            ''.join([i for i in salary_list[0] if i.isdigit()])
                        ) * self.course_rate
                        salary_to = int(
                            ''.join([i for i in salary_list[1] if i.isdigit()])
                        ) * self.course_rate
                if soup.find('span', {'data-qa': "vacancy-experience"}):
                    experience = Analyzer.get_experience(
                        self.string_cleaner(
                            soup.find(
                                'span', {'data-qa': "vacancy-experience"}
                            ).text
                        )
                    )
                # if soup.find('div', {'class': "vacancy-section"}):
                #     text = soup.find(
                #         'div', {'class': "vacancy-description"}
                #     ).text
                if soup.find('div', {'class': "bloko-tag-list"}):
                    stack_not_clear = soup.find_all(
                        'div', {'class': "bloko-tag bloko-tag_inline"}
                    )
                    stack = [i.text for i in stack_not_clear]
                if soup.find('div', {'class': "vacancy-company-details"}):
                    company = self.string_cleaner(
                        soup.find(
                            'div', {'class': "vacancy-company-details"}
                        ).text
                    )
                if soup.find('p', {'data-qa': "vacancy-view-location"}):
                    company_address = self.string_cleaner(
                        soup.find(
                            'p', {'data-qa': "vacancy-view-location"}
                        ).text
                    ).split(',')[0]
                if soup.find('span', {'data-qa': "vacancy-view-raw-address"}):
                    company_address = self.string_cleaner(
                        soup.find(
                            'span', {'data-qa': "vacancy-view-raw-address"}
                        ).text
                    ).split(',')[0]
                if soup.find('p', {'data-qa': "vacancy-view-employment-mode"}):
                    remote_section = self.string_cleaner(
                        soup.find(
                            'p', {'data-qa': "vacancy-view-employment-mode"}
                        ).text
                    ).lower()
                    if 'удаленная работа' in remote_section:
                        is_remote = True
                vacancy = {}
                grade = Analyzer.get_grade(title, new_text)
                vacancy.update({
                    'title': title,
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'is_remote': is_remote,
                    'experience': experience,
                    'grade': grade,
                    # 'text': text,
                    'stack': stack,
                    'company': company,
                    'company_address': company_address,
                    'link': link
                })
                time.sleep(self.sleep_time)
                return vacancy
            except AttributeError as e:
                print(e, link)
            except ValueError as e:
                print(e, link)
            except TypeError as e:
                print(e, link)
        return {}
