import datetime
from typing import List

import isikukood.assertions
import isikukood.errors
import isikukood.isikukood


def ordernumber_from_ssn(ssn: str) -> int:
    """Extract the order number from the given SSN.

    Examples:
        >>>isikukood.ordernumber_from_ssn('50001010006')
        0
        >>>isikukood.ordernumber_from_ssn('50001010105')
        10
    """

    return int(ssn[7:10])


def gender_from_ssn(ssn: str) -> str:
    """Extract the gender from the given SSN.

    Examples:
        >>>isikukood.gender_from_ssn('50001010006')
        'm'
        >>>isikukood.gender_from_ssn('60001010007')
        'f'

    Returns:
        str: Either 'm' or 'f'.
    """

    if int(ssn[0]) % 2 == 0: return 'f'
    else: return 'm'


def gender_marker(yyyy: int, gender: str) -> str:
    """Find the suitable gender marker (first digit), given gender and year of birth.

    Examples:
        >>>isikukood.gender_marker(2000, 'm')
        '5'
        >>>isikukood.gender_marker(1999, 'm')
        '3'

    Args:
        yyyy (int): Year of birth.
        gender (str): Either 'm' or 'f'.

    Returns:
        int: A number between 1 and 8 (inclusive).

    Raises:
        ValueError: When either one of the arguments is invalid.
    """

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
    """Find the birthdate, given an SSN.

    Examples:
        >>>isikukood.birthdate_from_ssn('50001010006')
        '2000-01-01'

    Args:
        ssn (str): Estonian SSN.

    Returns:
        str: Corresponding birthdate in ISO 8601 (yyyy-mm-dd).
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
    """
    Examples:
        >>>isikukood.insert_checksum('5000101000x')
        '50001010006'

    Args:
        ssn (str): Estonian SSN, can be either 10 or 11 digits.

    Returns:
        str: The given SSN but with the 11th digit replaced with a newly calculated checksum.

    Raises:
        ValueError: When the given SSN is not 10 or 11 digits in length.
    """

    try:
        assert len(ssn) in [10, 11]
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 10 or 11')

    ssn = ssn[0:10]
    return ssn + str(calculate_checksum(ssn))


def calculate_checksum(ssn: str) -> int:
    """Calculate the given SSN's checksum as per https://et.wikipedia.org/wiki/Isikukood#Kontrollnumber

    Examples:
        >>>isikukood.calculate_checksum('5000101000')
        6

    Args:
        ssn (str): Estonian SSN. May or may not already contain the checksum digit (can be either 10 or 11 digits).

    Returns:
        int: Corresponding checksum.
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


def enum(genders: List[str]=None, days: List[int]=None, months: List[int]=None, years: List[int]=None,
         onums: List[int]=None) -> List[str]:
    """Generate all valid Estonian SSNs possible with the given arguments.

    Examples:
        >>>isikukood.enum(days=[1], months=[1], years=[2000], onums=[0, 1, 2])
        ['50001010006', '50001010017', '50001010028', '60001010007', '60001010018', '60001010029']

    Args:
        genders (List[str]): A list in which each element is either 'm' or 'f'. Defaults to ['m', 'f'].
        days (List[int]): Days of the month, such as [5, 6, 7, 8, 9]. Defaults to [1; 31].
        months (List[int]): Months of the year, such as [9, 10, 11, 12]. Defaults to [1; 12].
        years (List[int]): Years, such as [2000, 2001, 2002]. Defaults to the current year.
        onums (List[int]): Order numbers, such as [371, 372, ..., 420]. Defaults to [0; 999].

    Returns:
        List[str]: List of SSNs.

    Raises:
        ValueError: When any of the given arguments is invalid.
    """

    if genders is None: genders = ['m', 'f']
    if days is None: days = list(range(1, 31 + 1))
    if months is None: months = list(range(1, 12 + 1))
    if years is None: years = [datetime.datetime.now().year]
    if onums is None: onums = list(range(0, 999 + 1))

    genders = [g.lower() for g in genders]
    genders = list(set(genders))
    days = list(set(days))
    months = list(set(months))
    years = list(set(years))
    onums = list(set(onums))

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
    for date in dates:
        try: isikukood.assertions.assert_existing_date(date)
        except AssertionError: continue
        dates_pruned.append(date)

    ssns = []
    for gender in genders:
        for date in dates_pruned:
            ssns.extend(isikukood.Isikukood(gender, date).construct(onums))
    ssns.sort()
    isikukood.assertions.assert_constructor_list(ssns)

    return ssns
