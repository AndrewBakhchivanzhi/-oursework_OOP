from utils.classes import HH,SuperJob,JSONSaver


count = 15
page = 1
name = input('Введите вакансию ')
town = input('Введите город для поиска ')
calary = int(input('Введите ожидаемую зарплату '))
while True:
    JSONSaver.clear_file()
    sj = SuperJob(name, page, count)
    hh = HH(name, page, count)
    JSONSaver.add_vacancy(sj.vacancies_to_lstdir())
    JSONSaver.add_vacancy(hh.vacancies_to_lstdir())
    JSONSaver.find_salary(calary)
    JSONSaver.find_town(town)
    filtered_lst = JSONSaver.load_file()
    if filtered_lst == []:
        page += 1
        pass
    else:
        for vacancy in filtered_lst:
             print(f'\nДолжность - {vacancy["Должность"]}\n'
                   f'Зарплата - {vacancy["Зарплата"]}\n'
                   f'Город - {vacancy["Город"]}\n'
                   f'График работы - {vacancy["График работы"]}\n'
                   f'Обязанности - {vacancy["Обязанности"]}\n'
                   f'Платформа размещения вакансии - {vacancy["Платформа размещения вакансии"]}')
        next_page = input('Перейти на следующую страницу дa/нет ')
        if next_page == 'да' or next_page == 'д':
            print("_" * 8, "СЛЕДУЮЩАЯ СТРАНИЦА", "_" * 8)
            page += 1
        else:
            break




