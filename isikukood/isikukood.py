import datetime
from multipledispatch import dispatch
from typing import List


_BUG_MSG = '\n\n\nSanity check failed - this is probably a bug in the module. Please report it, thanks!' \
           '\nThe original exception was: '


def _assert_numeric(ssn: str) -> None:
    try:
        assert ssn.isnumeric()
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is not numeric')


def _assert_gender(gender: str) -> None:
    """
    Assert that the given string is either 'm' or 'f'.
    Upon failing the check, a ValueError is raised.
    """

    try:
        assert gender in ['m', 'f']
    except AssertionError:
        raise ValueError(f'Expected gender to be either m or f - got {gender} instead.')


def _assert_first_digit(ssn: str) -> None:
    try:
        assert int(ssn[0]) in range(1, 8+1)
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) begins with a {ssn[0]}, expected a value between 1 and 8 (incl.)')


def _assert_year_range(yyyy: int) -> None:
    """
    Assert that the given year is between 1800 and 2199 (incl.)
    Upon failing the check, a ValueError is raised.
    """

    try:
        assert yyyy in range(1800, 2199 + 1)
    except AssertionError:
        raise ValueError(f'Expected year to be between 1800 and 2199 (incl.) - got {yyyy} instead.')


def _is_valid_date(date: str) -> bool:
    """
    Checks whether the given date is valid (no February 29th on non-leap years, etc.)
    :param date: Date in ISO 8601 (YYYY-MM-DD)
    :return: True if the given date is valid, False otherwise
    """

    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return False

    return True


def _construct_assert_list(ssns: List[str]) -> None:
    try:
        # Ensure that there are no duplicates
        assert len(ssns) == len(set(ssns))

        for ssn in ssns:
            assert_valid_ssn(ssn)
    except ValueError as e:
        raise AssertionError(_BUG_MSG + str(e))


def ordernumber_from_ssn(ssn: str) -> int:
    return int(ssn[7:10])


def gender_from_ssn(ssn: str) -> str:
    if int(ssn[0]) % 2 == 0: return 'f'
    else: return 'm'


def gender_marker(yyyy: int, gender: str) -> str:
    _assert_year_range(yyyy)
    _assert_gender(gender)

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


def assert_valid_ssn(ssn: str) -> None:
    """
    Assert that the given SSN is valid. Currently, this performs the following checks:
     * that the SSN is numeric
     * that the first digit is between 1 and 8 (incl.)
     * that the SSN is exactly 11 digits
     * that the checksum is correct
     * that the date is valid, i.e. that it exists and is between 1800.01.01 and 2199.12.31 (incl.)
    Upon failing any of the checks, a ValueError is raised.
    :param ssn: Estonian SSN
    """

    _assert_numeric(ssn)

    _assert_first_digit(ssn)

    try:
        assert len(ssn) == 11
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 11')

    expected_checksum = ssn_checksum(ssn)
    try:
        assert int(ssn[-1]) == expected_checksum
    except AssertionError:
        raise ValueError(f'Given SSN\'s ({ssn}) checksum is not valid, expected {expected_checksum}')

    birthdate = birthdate_from_ssn(ssn)
    _assert_year_range(int(birthdate[:4]))
    if not _is_valid_date(birthdate):
        raise ValueError(f'Invalid date for SSN {ssn}')


def birthdate_from_ssn(ssn: str) -> str:
    """
    :param ssn: Estonian SSN
    :return: Corresponding birthdate in ISO 8601 (yyyy-mm-dd)
    """

    _assert_first_digit(ssn)

    if ssn[0] in ['1', '2']: yy1 = '18'
    if ssn[0] in ['3', '4']: yy1 = '19'
    if ssn[0] in ['5', '6']: yy1 = '20'
    if ssn[0] in ['7', '8']: yy1 = '21'

    yy2 = ssn[1:2 + 1]
    mm = ssn[3:4 + 1]
    dd = ssn[5:6 + 1]

    birthdate = f'{yy1}{yy2}-{mm}-{dd}'
    _is_valid_date(birthdate)

    return birthdate


def insert_checksum(ssn: str) -> str:
    ssn = ssn[0:10]
    return ssn + str(ssn_checksum(ssn))


def ssn_checksum(ssn: str) -> int:
    """
    Calculate the given SSN's checksum as per https://et.wikipedia.org/wiki/Isikukood#Kontrollnumber
    :param ssn: Estonian SSN. May or may not contain the checksum digit already
                (can be either 10 or 11 digits).
    :return: Corresponding checksum
    """

    _assert_numeric(ssn)

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


class Isikukood:
    def __init__(self, gender: str, birthdate: str):
        self.gender = gender
        self.birthdate = birthdate

    @classmethod
    def from_ssn(cls, ssn: str):
        assert_valid_ssn(ssn)

        gender = gender_from_ssn(ssn)

        return cls(gender, birthdate_from_ssn(ssn))

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender: str):
        new_gender = new_gender.lower()
        _assert_gender(new_gender)
        self._gender = new_gender

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, new_birthdate: str):
        yyyy = int(new_birthdate[:4])
        _assert_year_range(yyyy)
        if not _is_valid_date(new_birthdate):
            raise ValueError(f'Given birthdate ({new_birthdate}) is not valid.')

        self._birthdate = new_birthdate

    def _gen_ssn(self, ordernumber: int) -> str:
        gm = gender_marker(int(self.birthdate[:4]), self.gender)
        xxyy = str(self.birthdate[2:4])
        mm = str(self.birthdate[5:7])
        dd = str(self.birthdate[8:10])

        base = gm + xxyy + mm + dd + "{0:03}".format(ordernumber)
        return base + str(ssn_checksum(base))

    @dispatch(int)
    def construct(self, ordernumber: int) -> str:
        ssn = self._gen_ssn(ordernumber)

        _construct_assert_list([ssn])

        return ssn

    @dispatch(list)
    def construct(self, ordernumbers: List[int]) -> List[str]:
        ret = []
        for onum in ordernumbers:
            ret.append(self._gen_ssn(onum))

        _construct_assert_list(ret)

        return ret

    @dispatch()
    def construct(self) -> List[str]:
        ret = []
        for i in range(999 + 1):
            ret.append(self._gen_ssn(i))

        _construct_assert_list(ret)

        return ret
