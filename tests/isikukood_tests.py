import unittest

from isikukood import Isikukood
import isikukood


class AssertionsTestCase(unittest.TestCase):
    def test_assert_ordernumber_range(self):
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_ordernumber_range(-1))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_ordernumber_range(1000))

    def test_assert_numeric(self):
        try: isikukood.assertions.assert_numeric('123')
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_numeric('x'))

    def test_assert_gender(self):
        try: isikukood.assertions.assert_gender('m')
        except Exception as e: self.fail(e)

        try: isikukood.assertions.assert_gender('f')
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_gender('x'))

    def test_assert_first_digit(self):
        try: isikukood.assertions.assert_first_digit('5xxxxxxxxxx')
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_first_digit('0xxxxxxxxxx'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_first_digit('9xxxxxxxxxx'))

    def test_assert_year_range(self):
        try: isikukood.assertions.assert_year_range(2000)
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_year_range(1799))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_year_range(2200))

    def test_assert_existing_date(self):
        try: isikukood.assertions.assert_existing_date('2000-01-01')
        except Exception as e: self.fail(e)

        try: isikukood.assertions.assert_existing_date('2000-02-29')
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_existing_date('2001-02-29'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_existing_date('2000-04-31'))

    def test_assert_constructor_list(self):
        try: isikukood.assertions.assert_constructor_list(['50001010006', '50001010017', '50001010028', '50001010039'])
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_constructor_list(['50001010006', '50001010017', '50001010006', '50001010039']))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_constructor_list(['50001010006', 'x']))

    def test_assert_valid_ssn(self):
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('50001x10006'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('90001010006'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('500010100060'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('50000000000'))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('50000000005'))

    def test_assert_correct_checksum(self):
        try: isikukood.assertions.assert_correct_checksum('50001010006')
        except Exception as e: self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_valid_ssn('50001010000'))

    def test_assert_enum_arguments(self):
        try:
            isikukood.assertions.assert_enum_arguments(['m', 'f'], list(range(1, 31+1)), list(range(1, 12+1)), list(range(1800, 2199+1)))
            isikukood.assertions.assert_enum_arguments(['m', 'f'], [1], [1], [1800])
            isikukood.assertions.assert_enum_arguments(['m', 'f'], [31], [12], [2199])
        except AssertionError as e:
            self.fail(e)

        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments([], [1], [1], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f', 'x'], [1], [1], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [0], [1], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [32], [1], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [1], [0], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [1], [13], [2000]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [1], [1], [1799]))
        self.assertRaises(AssertionError, lambda: isikukood.assertions.assert_enum_arguments(['m', 'f'], [1], [1], [2200]))


class FunctionsTestCase(unittest.TestCase):
    def test_ordernumber_from_ssn(self):
        self.assertEqual(isikukood.functions.ordernumber_from_ssn('50001010006'), 0)
        self.assertEqual(isikukood.functions.ordernumber_from_ssn('50001010104'), 10)
        self.assertEqual(isikukood.functions.ordernumber_from_ssn('50001011003'), 100)
        self.assertEqual(isikukood.functions.ordernumber_from_ssn('50001019993'), 999)

    def test_gender_from_ssn(self):
        self.assertEqual(isikukood.functions.gender_from_ssn('50001010006'), 'm')
        self.assertEqual(isikukood.functions.gender_from_ssn('60001010007'), 'f')

    def test_gender_marker(self):
        self.assertEqual(isikukood.functions.gender_marker(1800, 'm'), '1')
        self.assertEqual(isikukood.functions.gender_marker(1800, 'f'), '2')
        self.assertEqual(isikukood.functions.gender_marker(1900, 'm'), '3')
        self.assertEqual(isikukood.functions.gender_marker(1900, 'f'), '4')
        self.assertEqual(isikukood.functions.gender_marker(2000, 'm'), '5')
        self.assertEqual(isikukood.functions.gender_marker(2000, 'f'), '6')
        self.assertEqual(isikukood.functions.gender_marker(2100, 'm'), '7')
        self.assertEqual(isikukood.functions.gender_marker(2100, 'f'), '8')

    def test_birthdate_from_ssn(self):
        self.assertEqual(isikukood.functions.birthdate_from_ssn('10001010002'), '1800-01-01')
        self.assertEqual(isikukood.functions.birthdate_from_ssn('30001010004'), '1900-01-01')
        self.assertEqual(isikukood.functions.birthdate_from_ssn('50001010006'), '2000-01-01')
        self.assertEqual(isikukood.functions.birthdate_from_ssn('70001010008'), '2100-01-01')

    def test_insert_checksum(self):
        self.assertEqual(isikukood.functions.insert_checksum('5000101000x'), '50001010006')


class IsikukoodTestCase(unittest.TestCase):
    def test_instantiate(self):
        try: Isikukood('m', '2000-01-01')
        except ValueError as e: self.fail(e)
        self.assertRaises(ValueError, lambda: Isikukood('m', '2999-01-01'))
        self.assertRaises(ValueError, lambda: Isikukood.from_ssn('38001085710'))

    def test_instantiate_from_ssn(self):
        try: Isikukood.from_ssn('50001010006')
        except ValueError as e: self.fail(e)
        self.assertRaises(ValueError, lambda: Isikukood.from_ssn('50001010000'))

    def test_construct_int(self):
        ik = Isikukood('m', '2000-01-01')
        self.assertEqual(ik.construct(0), '50001010006')
        self.assertEqual(ik.construct(10), '50001010104')
        self.assertEqual(ik.construct(100), '50001011003')
        self.assertEqual(ik.construct(999), '50001019993')

        ik = Isikukood('m', '2000-01-01')
        self.assertRaises(ValueError, lambda: ik.construct(-1))

        ik = Isikukood('m', '2000-01-01')
        self.assertRaises(ValueError, lambda: ik.construct(1000))

    def test_construct_list(self):
        ik = Isikukood('m', '2000-01-01')
        self.assertEqual(ik.construct([]), [])

        ik = Isikukood('m', '2000-01-01')
        self.assertEqual(ik.construct([0]), ['50001010006'])

        ik = Isikukood('m', '2000-01-01')
        self.assertEqual(ik.construct([0, 1, 2, 3]), ['50001010006', '50001010017', '50001010028', '50001010039'])


if __name__ == '__main__':
    unittest.main()
