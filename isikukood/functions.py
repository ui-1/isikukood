import datetime
from typing import List

import isikukood.assertions
import isikukood.errors
import isikukood.isikukood


def ordernumber_from_ssn(ssn: str) -> int:
    return int(ssn[7:10])


def gender_from_ssn(ssn: str) -> str:
    if int(ssn[0]) % 2 == 0: return 'f'
    else: return 'm'


def gender_marker(yyyy: int, gender: str) -> str:
    try:
        isikukood.assertions.assert_year_range(yyyy)
        isikukood.assertions.assert_gender(gender)
    except AssertionError as e: raise ValueError(e)

    if yyyy in range(1800, 1899 + 1):
        if gender == 'm': return '1'
        if gender == 'f': return '2'
    if yyyy in range(1900, 1999 + 1):
        if gender == 'm': return '3'
        if gender == 'f': return '4'
    if yyyy in range(2000, 2099 + 1):
        if gender == 'm': return '5'
        if gender == 'f': return '6'
    if yyyy in range(2100, 2199 + 1):
        if gender == 'm': return '7'
        if gender == 'f': return '8'


def birthdate_from_ssn(ssn: str) -> str:
    """
    :param ssn: Estonian SSN
    :return: Corresponding birthdate in ISO 8601 (yyyy-mm-dd)
    """
    try: isikukood.assertions.assert_first_digit(ssn)
    except AssertionError as e: raise ValueError(e)

    if ssn[0] in ['1', '2']: yy1 = '18'
    if ssn[0] in ['3', '4']: yy1 = '19'
    if ssn[0] in ['5', '6']: yy1 = '20'
    if ssn[0] in ['7', '8']: yy1 = '21'

    yy2 = ssn[1:2 + 1]
    mm = ssn[3:4 + 1]
    dd = ssn[5:6 + 1]

    birthdate = f'{yy1}{yy2}-{mm}-{dd}'

    try: isikukood.assertions.assert_existing_date(birthdate)
    except AssertionError as e: raise ValueError(e)

    return birthdate


def insert_checksum(ssn: str) -> str:
    ssn = ssn[0:10]
    return ssn + str(calculate_checksum(ssn))


def calculate_checksum(ssn: str) -> int:
    """
    Calculate the given SSN's checksum as per https://et.wikipedia.org/wiki/Isikukood#Kontrollnumber
    :param ssn: Estonian SSN. May or may not contain the checksum digit already
                (can be either 10 or 11 digits).
    :return: Corresponding checksum
    """

    try: isikukood.assertions.assert_numeric(ssn)
    except AssertionError as e: raise ValueError(e)

    try: assert len(ssn) in [10, 11]
    except AssertionError: raise ValueError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 10 or 11')

    k = 0

    for i in range(1, 9 + 1):
        k += int(ssn[i-1]) * i
    k += int(ssn[9])

    j = k % 11
    if j < 10: return j

    k = 0
    for i in range(3, 9 + 1):
        k += int(ssn[i-3]) * i
    for i in range(1, 3 + 1):
        k += int(ssn[i+6]) * i

    j = k % 11
    if j < 10: return j
    else: return 0


def enum(genders: List[str]=None, days: List[int]=None, months: List[int]=None, years: List[int]=None) -> List[str]:

    """
    :param genders: Either ['m'], ['f'], or ['m', 'f']
    :param days: Days of the month, such as [5, 6, 7, 8, 9]
    :param months: Months of the year, such as [9, 10, 11, 12]
    :param years: Years, such as [2000, 2001, 2002]
    :return: List of all valid Estonian SSNs with the given arguments
    """

    if genders is None: genders = ['m', 'f']
    if days is None: days = list(range(1, 31 + 1))
    if months is None: months = list(range(1, 12 + 1))
    if years is None: years = [datetime.datetime.now().year]

    genders = [g.lower() for g in genders]
    genders = sorted(list(set(genders)))
    days = sorted(list(set(days)))
    months = sorted(list(set(months)))
    years = sorted(list(set(years)))

    try: isikukood.assertions.assert_enum_arguments(genders, days, months, years)
    except AssertionError as e: raise ValueError(e)

    for lis in [days, months, years]:
        for i in range(len(lis)):
            if int(lis[i]) < 10: lis[i] = '0' + str(lis[i])  # 2 -> 02
            else: lis[i] = str(lis[i])

    dates = []
    for year in years:
        for month in months:
            for day in days:
                dates.append(f'{year}-{month}-{day}')

    dates_pruned = []
    for d in dates:
        try: isikukood.assertions.assert_existing_date(d)
        except AssertionError: continue
        dates_pruned.append(d)

    ssns = []
    for g in genders:
        for d in dates_pruned:
            ssns.extend(isikukood.Isikukood(g, d).construct())
    ssns.sort()
    isikukood.assertions.assert_constructor_list(ssns)

    return ssns
