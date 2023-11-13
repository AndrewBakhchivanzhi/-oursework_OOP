import json
import requests

class Api_Vacancy:

    def __init__(self, name, page, count):
        self.name = name
        self.page = page
        self.count = count

    def __repr__(self):
        return f'{self.name}'


class HH(Api_Vacancy):

    url = 'https://api.hh.ru/vacancies'

    def __init__(self, name, page, count):
        super().__init__(name, page, count)

    def get_vacancies(self):
        vacancies = requests.get(HH.url, params={'text': self.name, 'page': self.page, 'per_page': self.count}).json()
        return vacancies

    def vacancies_to_lstdir(self):

        lst_vacancies = []
        hh_dict = self.get_vacancies()
        for element in hh_dict['items']:
            if element['salary'] is None:
                payment = 'Зарплата не указана'
            elif element['salary']['from'] is None:
                payment = 'До ' + str(element['salary']['to'])
            elif element['salary']['to'] is None:
                payment = 'От ' + str(element['salary']['from'])
            elif element['salary']['from'] and element['salary']['to'] is not None:
                payment = str(element['salary']['from']) + '-' + str(element['salary']['to'])

            vacancy = {
                "Должность": element['name'],
                "Зарплата": payment,
                "Город": element['area']['name'],
                "График работы": element['schedule']['name'],
                "Обязанности": element['snippet']['responsibility'],
                "Платформа размещения вакансии": 'hh.ru'

            }
            lst_vacancies.append(vacancy)

        return lst_vacancies

    def print_info(self) -> str:
        return json.dumps(self.get_vacancies(), indent=2, ensure_ascii=False)

class SuperJob(Api_Vacancy):

    api = 'v3.r.137937347.affda0fda7b1778f3d1e6fcdbb02eb17a1150e32.0d2af6a4da370b5c4ace1d393126236ec6dfc63d'
    url = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, name, page, count):
        super().__init__(name, page, count)

    def get_vacancies(self):

        headers = {'X-Api-App-Id': SuperJob.api}
        vacancies = requests.get(SuperJob.url, headers=headers,
                                 params={'keywords': self.name, 'page': self.page, 'count': self.count}).json()
        return vacancies

    def vacancies_to_lstdir(self):

        lst_vacancies = []
        sj_dict = self.get_vacancies()

        for element in sj_dict['objects']:
            if element['payment_from'] and element['payment_to'] != 0:
                payment = str(element['payment_from']) + '-' + str(element['payment_to'])
            elif element['payment_from'] == 0 and element['payment_to'] == 0:
                payment = "Зарплата не указана"
            elif element['payment_from'] == 0:
                payment = 'До ' + str(element['payment_to'])
            elif element['payment_to'] == 0:
                payment = 'От ' + str(element['payment_from'])
            else:
                payment = "Зарплата не указана"

            vacancy = {
                "Должность": element['profession'],
                "Зарплата": payment,
                "Город": element['town']['title'],
                "График работы": element['type_of_work']['title'],
                "Обязанности": element['candidat'].replace('•', '').replace('\n', ''),
                "Платформа размещения вакансии": "SuperJob.ru"

            }
            lst_vacancies.append(vacancy)
        return lst_vacancies

    def print_info(self) -> str:

        return json.dumps(self.get_vacancies(), indent=2, ensure_ascii=False)

class JSONSaver:

    def load_file(file='Vacancies.json'):
        with open(file, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        return vacancies

    def add_vacancy(text: list):
        vacancies = JSONSaver.load_file()
        with open('Vacancies.json', 'w', encoding='utf-8') as file:
            for vacancy in text:
                vacancies.append(vacancy)
            json.dump(vacancies, file, indent=2, ensure_ascii=False)

    def clear_file():
        with open('Vacancies.json', 'w', encoding='utf-8') as file:
            file.write('[]')

    def find_town(town):
        vacancies = JSONSaver.load_file()
        filtered_lst = []
        for vacancy in vacancies:
            if vacancy['Город'].lower() == town.lower():
                filtered_lst.append(vacancy)
        with open('Vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(filtered_lst, file, indent=2, ensure_ascii=False)

    def find_salary(salary):
        vacancies = JSONSaver.load_file()
        filtered_lst = []
        for vacancy in vacancies:
            try:
                splited_salary = vacancy['Зарплата'].split('-')
                if int(splited_salary[1]) >= salary:
                    filtered_lst.append(vacancy)
            except:
                if vacancy['Зарплата'] == 'Зарплата не указана':
                    pass
                elif int(vacancy['Зарплата'][3:]) >= salary:
                    filtered_lst.append(vacancy)
        with open('Vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(filtered_lst, file, indent=2, ensure_ascii=False)