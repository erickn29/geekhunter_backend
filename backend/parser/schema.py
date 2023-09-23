from pydantic import BaseModel, model_validator


class DefaultDataModel(BaseModel):
    """Базовый класс для работы с данными"""

    name: str

    # @model_validator(mode='after')
    # def check_name_length(self) -> 'DefaultDataModel':
    #     """Метод валидирует длину строки"""
    #     max_length = 128
    #     if 0 < len(self.name) <= max_length:
    #         print(f'Name length error: {self.name}')
    #     return self


class StackTool(DefaultDataModel):
    """Класс для работы с навыками"""

    pass


class Language(DefaultDataModel):
    """Класс для работы с языками"""

    pass


class City(DefaultDataModel):
    """Класс для работы с городами"""

    pass


class Speciality(DefaultDataModel):
    """Класс для работы со специализацией"""

    pass


class Experience(DefaultDataModel):
    """Класс для работы с опытом"""

    pass


class Grade(DefaultDataModel):
    """Класс для работы с грейдом"""

    name: str | None


class Company(BaseModel):
    """Класс для работы с компаниями"""

    name: str
    city: City = None


class Vacancy(BaseModel):
    """Класс для работы с вакансией"""

    title: str
    text: str
    link: str
    speciality: Speciality
    experience: Experience
    language: Language
    company: Company
    is_remote: bool = False
    salary_from: int | None
    salary_to: int | None
    grade: Grade
    stack: list[StackTool] | None

    @model_validator(mode='after')
    def check_salary_exists(self) -> 'Vacancy':
        """Метод проверяет есть ли хотя бы 1 значение в зарплате (от или до)"""
        if not any([self.salary_to, self.salary_from]):
            print(f'No salaries in vacancy: {self.link}')
        return self


class VacanciesList(BaseModel):
    """Класс для работы со списком вакансий"""

    data: list[Vacancy] = []
