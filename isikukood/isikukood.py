from multipledispatch import dispatch
from typing import List

import isikukood.functions
import isikukood.assertions


class Isikukood:
    def __init__(self, gender: str, birthdate: str):
        self.gender = gender
        self.birthdate = birthdate

    @classmethod
    def from_ssn(cls, ssn: str):
        """Instantiate the class from an already existing SSN.
        :raises ValueError: When the given SSN is invalid.
        """

        try: isikukood.assertions.assert_valid_ssn(ssn)
        except AssertionError as e: raise ValueError(e)

        gender = isikukood.functions.gender_from_ssn(ssn)

        return cls(gender, isikukood.functions.birthdate_from_ssn(ssn))

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender: str):
        new_gender = new_gender.lower()
        try: isikukood.assertions.assert_gender(new_gender)
        except AssertionError as e: raise ValueError(e)
        self._gender = new_gender

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, new_birthdate: str):
        yyyy = int(new_birthdate[:4])

        try:
            isikukood.assertions.assert_year_range(yyyy)
            isikukood.assertions.assert_existing_date(new_birthdate)
        except AssertionError as e: raise ValueError(e)

        self._birthdate = new_birthdate

    def _gen_ssn(self, ordernumber: int) -> str:
        gm = isikukood.functions.gender_marker(int(self.birthdate[:4]), self.gender)
        xxyy = str(self.birthdate[2:4])
        mm = str(self.birthdate[5:7])
        dd = str(self.birthdate[8:10])

        base = gm + xxyy + mm + dd + "{0:03}".format(ordernumber)
        return base + str(isikukood.functions.calculate_checksum(base))

    @dispatch()
    def construct(self) -> List[str]:
        """Generate all possible SSNs with the instance's gender and birthdate.
        :return: List of SSNs.
        :rtype: List[str]
        """

        ret = []
        for i in range(999 + 1):
            ret.append(self._gen_ssn(i))

        isikukood.assertions.assert_constructor_list(ret)

        return ret

    @dispatch(int)
    def construct(self, ordernumber: int) -> str:
        """Generate an SSN with the instance's gender and birthdate and the order number that was given as an argument.
        :raises ValueError: When the given order number is invalid.
        """

        try: isikukood.assertions.assert_ordernumber_range(ordernumber)
        except AssertionError as e: raise ValueError(e)

        ssn = self._gen_ssn(ordernumber)

        isikukood.assertions.assert_constructor_list([ssn])

        return ssn

    @dispatch(list)
    def construct(self, ordernumbers: List[int]) -> List[str]:
        """Generate all possible SSNs with the instance's gender and birthdate
        and with all the order numbers that were given as an argument.
        :param ordernumbers: List of order numbers.
        :type ordernumbers: List[int]
        :return: List of SSNs.
        :rtype: List[str]
        :raises ValueError: When any of the given order numbers is invalid.
        """

        ret = []
        for onum in ordernumbers:
            try: isikukood.assertions.assert_ordernumber_range(onum)
            except AssertionError as e: raise ValueError(e)
            ret.append(self._gen_ssn(onum))

        isikukood.assertions.assert_constructor_list(ret)

        return ret
