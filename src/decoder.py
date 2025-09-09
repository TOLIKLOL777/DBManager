from src.external_api import get_employers, get_vacancies


def employers_info() -> list:
    employers = get_employers()
    employers_data = []
    for i in employers:
        for employer in i:
            employers_data.append(
                [i[employer]["id"], i[employer]["name"], i[employer]["alternate_url"], i[employer]["open_vacancies"]]
            )
    return employers_data


def vacancies_info() -> list:
    vacancies = get_vacancies()
    vacancies_data = []
    for i in vacancies:
        for vacancy in i["items"]:
            vacancies_data.append(
                [
                    vacancy.get("id"),
                    vacancy.get("employer").get("id"),
                    vacancy.get("employer").get("name"),
                    vacancy.get("name"),
                    vacancy.get("salary", {}).get("from") if vacancy.get("salary") else 0,
                    vacancy.get("salary", {}).get("to") if vacancy.get("salary") else 0,
                    vacancy["alternate_url"],
                ]
            )
    return vacancies_data
