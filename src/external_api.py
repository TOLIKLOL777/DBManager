import requests

hh_api = "https://api.hh.ru/"
companies = [
    {"id": 15478, "name": "VK"},
    {"id": 1740, "name": "Яндекс"},
    {"id": 3529, "name": "СБЕР"},
    {"id": 64174, "name": "2ГИС"},
    {"id": 78638, "name": "Т-банк"},
    {"id": 1122462, "name": "Skyeng"},
    {"id": 866511, "name": "ООО НПП ЭКРА"},
    {"id": 120583, "name": "Кейсистемс"},
    {"id": 4181, "name": "Банк ВТБ (ПАО)"},
    {"id": 1455, "name": "ООО HeadHunter"},
]


def get_employers() -> list:
    """Возвращает информацию с API запроса о компаниях"""
    employers = []
    for company in companies:
        params = {"employer_id": company["id"]}
        data = requests.get(url=hh_api + "employers/" + str(company["id"]), params=params)
        employers.append({company["name"]: data.json()})
    return employers


def get_vacancies() -> list:
    """Возвращает информацию с API запроса о вакациях компаний"""
    vacancies = []
    for company in companies:
        params = {"employer_id": company["id"], "per_page": 100}
        data = requests.get(url=hh_api + "vacancies", params=params)
        vacancies.append(data.json())
    return vacancies
