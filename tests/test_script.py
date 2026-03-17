import pytest
from script import read_csv, get_median_by_coffee_spent_each_student, do_correct_row

"""
Check that if this function get name of not exist file
this function throw exception about that
"""
def test_not_exist_file(capsys):
    read_csv(["Some.csv"])

    capt = capsys.readouterr()

    assert "не найден !" in capt.out


"""
Make example gruop of rows
in which check one of possible error 
related to types
"""
@pytest.mark.parametrize("enter, expected", [
(["Семён Семёныч", "2023-01-10", "450", "7.5", "12", "норм", "Математика"], ""),
([], "Пустая строка !"),
(["Семён Семёныч", "er", "450", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "2023-40-10", "450", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "0-01-10", "450", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "-5-01-10", "450", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "2023-01-50", "450", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "2023-01-10", "er", "7.5", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "2023-01-10", "450", "er", "12", "норм", "Математика"], "не соответствует формату"),
(["Семён Семёныч", "2023-01-10", "450", "7.5", "er", "норм", "Математика"], "не соответствует формату"),
])
def test_check_finding_errors_in_raw_data(capsys, enter, expected):
    do_correct_row(enter, 1)

    capt = capsys.readouterr()

    assert expected in capt.out


"""
Simply check that using "median" not "mean" or etc
"""
@pytest.mark.parametrize("enter, expected", [
([["I", "+", 2]], 2),
([["I", "+", 2], ["I", "+", 3]], 2.5),
([["I", "+", 1], ["I", "+", 3], ["I", "+", 100]], 3),
])
def test_use_median(enter, expected):
    assert get_median_by_coffee_spent_each_student(enter)["I"] == expected