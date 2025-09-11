from src.external_api import get_employers, get_vacancies


def employers_info() -> list:
    """Переводит запрос с API в нужный формат с нужными данными"""
    employers = get_employers()
    employers_data = []
    for employer in employers:
        employers_data.append(
            [employer["id"], employer["name"], employer["alternate_url"], employer["open_vacancies"]]
        )
    return employers_data


def vacancies_info() -> list:
    """Переводит запрос с API в нужный формат с нужными данными"""
    vacancies = get_vacancies()
    vacancies_data = []
    for i in vacancies:
        for vacancy in i["items"]:
            vacancies_data.append(
                [
                    vacancy.get("id"),
                    vacancy.get("employer").get("id"),
                    vacancy.get("name"),
                    vacancy.get("salary", {}).get("from") if vacancy.get("salary") else 0,
                    vacancy.get("salary", {}).get("to") if vacancy.get("salary") else 0,
                    vacancy["alternate_url"],
                ]
            )
    return vacancies_data
