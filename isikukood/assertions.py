import datetime
from typing import List

import isikukood.functions
import isikukood.errors


def assert_ordernumber_range(ordernumber: int) -> None:
    """Assert that the given argument is between 0 and 999 (inclusive).

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        assert ordernumber in range(0, 999 + 1)
    except AssertionError:
        raise AssertionError(f'Order number was {ordernumber}, expected a value between 0 and 999 (incl.)')


def assert_numeric(arg: str) -> None:
    """Assert that the given argument is numeric.

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        assert arg.isnumeric()
    except AssertionError:
        raise AssertionError(f'Given argument ({arg}) is not numeric')


def assert_gender(gender: str) -> None:
    """Assert that the given argument is either 'm' or 'f'.

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        assert gender in ['m', 'f']
    except AssertionError:
        raise AssertionError(f'Expected gender to be either m or f - got {gender} instead.')


def assert_first_digit(ssn: str) -> None:
    """Assert that the first character of the given argument is between 1 and 8 (inclusive).

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        assert int(ssn[0]) in range(1, 8+1)
    except AssertionError:
        raise AssertionError(f'Given SSN ({ssn}) begins with a {ssn[0]}, expected a value between 1 and 8 (incl.)')


def assert_year_range(yyyy: int) -> None:
    """Assert that the given argument is between 1800 and 2199 (inclusive).

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        assert yyyy in range(1800, 2199 + 1)
    except AssertionError:
        raise AssertionError(f'Expected year to be between 1800 and 2199 (incl.) - got {yyyy} instead.')


def assert_existing_date(date: str) -> None:
    """Assert that the given date exists (no February 29th on non-leap years, no April 31st, etc.).

    Args:
        date (str): Date in ISO 8601 (YYYY-MM-DD).

    Raises:
        AssertionError: When the assertion fails.
    """

    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise AssertionError(f'Date {date} is invalid')


def assert_constructor_list(ssns: List[str]) -> None:
    """Sanity check called by SSN constructors.
    Asserts that the given argument contains no duplicates and that every one of its elements is a valid Estonian SSN.

    Args:
        ssns (List[str]): List of SSNs coming from Isikukood.construct().

    Raises:
        AssertionError: When any of the assertions fail.
    """

    try:
        # Ensure that there are no duplicates
        assert len(ssns) == len(set(ssns))

        for ssn in ssns:
            isikukood.assertions.assert_valid_ssn(ssn)
    except AssertionError as e:
        raise AssertionError(isikukood.errors.BUG_MSG + str(e))


def assert_valid_ssn(ssn: str) -> None:
    """Assert that the given argument is a valid Estonian SSN. Currently, this performs the following checks:
     * that the SSN is numeric
     * that the first digit is between 1 and 8 (inclusive)
     * that the SSN is exactly 11 digits
     * that the checksum is correct
     * that the birthdate exists
     * that the year of birth is between 1800 and 2199 (inclusive)

    Raises:
        AssertionError: When any of the assertions fail.
    """

    assert_numeric(ssn)
    assert_first_digit(ssn)

    try:
        assert len(ssn) == 11
    except AssertionError:
        raise AssertionError(f'Given SSN ({ssn}) is {len(ssn)} digits, expected 11')

    assert_correct_checksum(ssn)

    try: birthdate = isikukood.functions.birthdate_from_ssn(ssn)
    except ValueError as e: raise AssertionError(e)

    assert_year_range(int(birthdate[:4]))
    assert_existing_date(birthdate)


def assert_correct_checksum(ssn: str) -> None:
    """Assert that the given SSN's checksum is correct.

    Raises:
        AssertionError: When the assertion fails.
    """

    expected_checksum = isikukood.functions.calculate_checksum(ssn)
    try:
        assert str(expected_checksum) == ssn[10]
    except AssertionError:
        raise AssertionError(f'Invalid checksum for {ssn} - expected {expected_checksum}')


def assert_enum_arguments(genders: List[str], days: List[int], months: List[int], years: List[int]) -> None:
    """Assert that the arguments for functions.enum() are valid. This performs the following checks:
     * that every element in genders is either 'm' or 'f'
     * that every element in days is between 1 and 31 (inclusive)
     * that every element in months is between 1 and 12 (inclusive)
     * that every element in years is between 1800 and 2199 (inclusive)

     Raises:
         AssertionError: When any of the assertions fail.
    """
    try:
        for g in genders: assert g == 'm' or g == 'f'
    except AssertionError:
        raise AssertionError(f'Genders must contain \'m\', \'f\', or both. Got {genders} instead.')

    for d in days:
        try:
            assert d in range(1, 31 + 1)
        except AssertionError:
            raise AssertionError(f'Days must only contain values between 1 and 31 (incl.), found unexpected value {d}')

    for m in months:
        try:
            assert m in range(1, 12 + 1)
        except AssertionError:
            raise AssertionError(f'Months must only contain values between 1 and 12 (incl.), found unexpected value {m}')

    for y in years:
        isikukood.assertions.assert_year_range(y)
