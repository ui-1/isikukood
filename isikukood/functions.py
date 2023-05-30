import isikukood.assertions
import isikukood.errors


def ordernumber_from_ssn(ssn: str) -> int:
    return int(ssn[7:10])


def gender_from_ssn(ssn: str) -> str:
    if int(ssn[0]) % 2 == 0: return 'f'
    else: return 'm'


def gender_marker(yyyy: int, gender: str) -> str:
    isikukood.assertions.assert_year_range(yyyy)
    isikukood.assertions.assert_gender(gender)

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

    isikukood.assertions.assert_first_digit(ssn)

    if ssn[0] in ['1', '2']: yy1 = '18'
    if ssn[0] in ['3', '4']: yy1 = '19'
    if ssn[0] in ['5', '6']: yy1 = '20'
    if ssn[0] in ['7', '8']: yy1 = '21'

    yy2 = ssn[1:2 + 1]
    mm = ssn[3:4 + 1]
    dd = ssn[5:6 + 1]

    birthdate = f'{yy1}{yy2}-{mm}-{dd}'
    isikukood.assertions.assert_existing_date(birthdate)

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

    isikukood.assertions.assert_numeric(ssn)

    try:
        assert len(ssn) in [10, 11]
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 10 or 11')

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
