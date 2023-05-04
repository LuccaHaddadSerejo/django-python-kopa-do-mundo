from exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)
from datetime import datetime


def data_processing(d_team: dict) -> None:
    if d_team["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    f_c_year = 1930
    valid_years = []
    actual_year = datetime.now().year

    while f_c_year <= actual_year:
        valid_years.append(f_c_year)
        f_c_year
        f_c_year += 4

    date_str = d_team["first_cup"]
    date_f = datetime.strptime(date_str, "%Y-%m-%d")

    if valid_years.count(date_f.year) == 0:
        raise InvalidYearCupError("there was no world cup this year")

    possible_titles = 0
    t_f_cup = date_f.year

    while t_f_cup <= actual_year:
        t_f_cup += 4
        possible_titles += 1

    if d_team["titles"] > possible_titles:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
