import datetime
from typing import List

import isikukood.functions
import isikukood.errors


def assert_ordernumber_range(ordernumber: int) -> None:
    try:
        assert ordernumber in range(0, 999 + 1)
    except AssertionError:
        raise ValueError(f'Ordernumber was {ordernumber}, expected a value between 0 and 999 (incl.)')


def assert_numeric(ssn: str) -> None:
    try:
        assert ssn.isnumeric()
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is not numeric')


def assert_gender(gender: str) -> None:
    """
    Assert that the given string is either 'm' or 'f'.
    Upon failing the check, a ValueError is raised.
    """

    try:
        assert gender in ['m', 'f']
    except AssertionError:
        raise ValueError(f'Expected gender to be either m or f - got {gender} instead.')


def assert_first_digit(ssn: str) -> None:
    try:
        assert int(ssn[0]) in range(1, 8+1)
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) begins with a {ssn[0]}, expected a value between 1 and 8 (incl.)')


def assert_year_range(yyyy: int) -> None:
    """
    Assert that the given year is between 1800 and 2199 (incl.)
    Upon failing the check, a ValueError is raised.
    """

    try:
        assert yyyy in range(1800, 2199 + 1)
    except AssertionError:
        raise ValueError(f'Expected year to be between 1800 and 2199 (incl.) - got {yyyy} instead.')


def assert_existing_date(date: str) -> None:
    """
    Checks whether the given date is valid (no February 29th on non-leap years, etc.)
    :param date: Date in ISO 8601 (YYYY-MM-DD)
    :return: True if the given date is valid, False otherwise
    """

    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise AssertionError(f'Date {date} is invalid')


def assert_constructor_list(ssns: List[str]) -> None:
    try:
        # Ensure that there are no duplicates
        assert len(ssns) == len(set(ssns))

        for ssn in ssns:
            isikukood.assertions.assert_valid_ssn(ssn)
    except (ValueError, AssertionError) as e:
        raise AssertionError(isikukood.errors.BUG_MSG + str(e))


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

    assert_numeric(ssn)
    assert_first_digit(ssn)

    try:
        assert len(ssn) == 11
    except AssertionError:
        raise ValueError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 11')

    assert_correct_checksum(ssn)

    birthdate = isikukood.functions.birthdate_from_ssn(ssn)
    assert_year_range(int(birthdate[:4]))
    assert_existing_date(birthdate)


def assert_correct_checksum(ssn: str) -> None:
    expected_checksum = isikukood.functions.calculate_checksum(ssn)
    try:
        assert str(expected_checksum) == ssn[10]
    except AssertionError:
        raise AssertionError(f'Invalid checksum for {ssn} - expected {expected_checksum}')
