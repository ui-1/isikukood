# Isikukood

Small Estonian social security number library (I know they're not really SSNs but I don't have a better English name for them)

# Table of Contents

* [functions](#functions)
  * [ordernumber\_from\_ssn](#functions.ordernumber_from_ssn)
  * [gender\_from\_ssn](#functions.gender_from_ssn)
  * [gender\_marker](#functions.gender_marker)
  * [birthdate\_from\_ssn](#functions.birthdate_from_ssn)
  * [insert\_checksum](#functions.insert_checksum)
  * [calculate\_checksum](#functions.calculate_checksum)
  * [enum](#functions.enum)
* [isikukood](#isikukood)
  * [Isikukood](#isikukood.Isikukood)
    * [from\_ssn](#isikukood.Isikukood.from_ssn)
    * [construct](#isikukood.Isikukood.construct)
    * [construct](#isikukood.Isikukood.construct)
    * [construct](#isikukood.Isikukood.construct)
* [assertions](#assertions)
  * [assert\_ordernumber\_range](#assertions.assert_ordernumber_range)
  * [assert\_numeric](#assertions.assert_numeric)
  * [assert\_gender](#assertions.assert_gender)
  * [assert\_first\_digit](#assertions.assert_first_digit)
  * [assert\_year\_range](#assertions.assert_year_range)
  * [assert\_existing\_date](#assertions.assert_existing_date)
  * [assert\_constructor\_list](#assertions.assert_constructor_list)
  * [assert\_valid\_ssn](#assertions.assert_valid_ssn)
  * [assert\_correct\_checksum](#assertions.assert_correct_checksum)
  * [assert\_enum\_arguments](#assertions.assert_enum_arguments)

---
<a id="functions"></a>

# functions

---
<a id="functions.ordernumber_from_ssn"></a>

#### ordernumber\_from\_ssn

```python
def ordernumber_from_ssn(ssn: str) -> int
```

Extract the order number from the given SSN.

**Examples**:

```python
    >>>isikukood.ordernumber_from_ssn('50001010006')
    0
    >>>isikukood.ordernumber_from_ssn('50001010105')
    10
```

---
<a id="functions.gender_from_ssn"></a>

#### gender\_from\_ssn

```python
def gender_from_ssn(ssn: str) -> str
```

Extract the gender from the given SSN.

**Examples**:

     ```python
        >>>isikukood.gender_from_ssn('50001010006')
        'm'
        >>>isikukood.gender_from_ssn('60001010007')
        'f'
    ```
  

**Returns**:

- `str` - Either 'm' or 'f'.
  
  ---

---
<a id="functions.gender_marker"></a>

#### gender\_marker

```python
def gender_marker(yyyy: int, gender: str) -> str
```

Find the suitable gender marker (first digit), given gender and year of birth.

**Examples**:

```python
    >>>isikukood.gender_marker(2000, 'm')
    '5'
    >>>isikukood.gender_marker(1999, 'm')
    '3'
```
  

**Arguments**:

- `yyyy` _int_ - Year of birth.
- `gender` _str_ - Either 'm' or 'f'.
  

**Returns**:

- `int` - A number between 1 and 8 (inclusive).
  

**Raises**:

- `ValueError` - When either one of the arguments is invalid.

---
<a id="functions.birthdate_from_ssn"></a>

#### birthdate\_from\_ssn

```python
def birthdate_from_ssn(ssn: str) -> str
```

Find the birthdate, given an SSN.

**Examples**:

```python
    >>>isikukood.birthdate_from_ssn('50001010006')
    '2000-01-01'
```
  

**Arguments**:

- `ssn` _str_ - Estonian SSN.
  

**Returns**:

- `str` - Corresponding birthdate in ISO 8601 (yyyy-mm-dd).

---
<a id="functions.insert_checksum"></a>

#### insert\_checksum

```python
def insert_checksum(ssn: str) -> str
```

**Examples**:

```python
    >>>isikukood.insert_checksum('5000101000x')
    '50001010006'
```
  

**Arguments**:

- `ssn` _str_ - Estonian SSN, can be either 10 or 11 digits.
  

**Returns**:

- `str` - The given SSN but with the 11th digit replaced with a newly calculated checksum.
  

**Raises**:

- `ValueError` - When the given SSN is not 10 or 11 digits in length.

---
<a id="functions.calculate_checksum"></a>

#### calculate\_checksum

```python
def calculate_checksum(ssn: str) -> int
```

Calculate the given SSN's checksum as per https://et.wikipedia.org/wiki/Isikukood#Kontrollnumber

**Examples**:

```python
    >>>isikukood.calculate_checksum('5000101000')
    6
```
  

**Arguments**:

- `ssn` _str_ - Estonian SSN. May or may not already contain the checksum digit (can be either 10 or 11 digits).
  

**Returns**:

- `int` - Corresponding checksum.

---
<a id="functions.enum"></a>

#### enum

```python
def enum(genders: List[str] = None,
         days: List[int] = None,
         months: List[int] = None,
         years: List[int] = None,
         onums: List[int] = None) -> List[str]
```

Generate all valid Estonian SSNs possible with the given arguments.

**Examples**:

```python
    >>>isikukood.enum(days=[1], months=[1], years=[2000], onums=[0, 1, 2])
    ['50001010006', '50001010017', '50001010028', '60001010007', '60001010018', '60001010029']
```
  

**Arguments**:

- `genders` _List[str]_ - A list in which each element is either 'm' or 'f'. Defaults to ['m', 'f'].
- `days` _List[int]_ - Days of the month, such as [5, 6, 7, 8, 9]. Defaults to [1; 31].
- `months` _List[int]_ - Months of the year, such as [9, 10, 11, 12]. Defaults to [1; 12].
- `years` _List[int]_ - Years, such as [2000, 2001, 2002]. Defaults to the current year.
- `onums` _List[int]_ - Order numbers, such as [371, 372, ..., 420]. Defaults to [0; 999].
  

**Returns**:

- `List[str]` - List of SSNs.
  

**Raises**:

- `ValueError` - When any of the given arguments is invalid.

---
<a id="isikukood"></a>

# isikukood

---
<a id="isikukood.Isikukood"></a>

## Isikukood Objects

```python
class Isikukood()
```

---
<a id="isikukood.Isikukood.from_ssn"></a>

#### from\_ssn

```python
@classmethod
def from_ssn(cls, ssn: str)
```

Instantiate the class from an already existing SSN.

**Examples**:

```python
    >>>isikukood.Isikukood('m', '2000-01-01')
```
  

**Raises**:

- `ValueError` - When the given SSN is invalid.

---
<a id="isikukood.Isikukood.construct"></a>

#### construct

```python
@multimethod
def construct() -> List[str]
```

Generate all possible SSNs with the instance's gender and birthdate.

**Examples**:

```python
    >>>isikukood.Isikukood('m', '2000-01-01').construct()
    ['50001010006', '50001010017', '50001010028', ...]
```
  
  

**Returns**:

- `List[str]` - List of SSNs.

---
<a id="isikukood.Isikukood.construct"></a>

#### construct

```python
@multimethod
def construct(ordernumber: int) -> str
```

Generate an SSN with the instance's gender and birthdate and the order number that was given as an argument.

**Examples**:

```python
    >>>isikukood.Isikukood('m', '2000-01-01').construct(111)
    '50001011112'
```
  

**Raises**:

- `ValueError` - When the given order number is invalid.

---
<a id="isikukood.Isikukood.construct"></a>

#### construct

```python
@multimethod
def construct(ordernumbers: List[int]) -> List[str]
```

Generate all possible SSNs with the instance's gender and birthdate
and with all the order numbers that were given as an argument.

**Examples**:

```python
    >>>isikukood.Isikukood('m', '2000-01-01').construct([111, 222, 333])
    ['50001011112', '50001012229', '50001013335']
```
  

**Arguments**:

- `ordernumbers` _List[int]_ - List of order numbers.
  

**Returns**:

- `List[str]` - List of SSNs.
  

**Raises**:

- `ValueError` - When any of the given order numbers is invalid.

---
<a id="assertions"></a>

# assertions

---
<a id="assertions.assert_ordernumber_range"></a>

#### assert\_ordernumber\_range

```python
def assert_ordernumber_range(ordernumber: int) -> None
```

Assert that the given argument is between 0 and 999 (inclusive).

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_numeric"></a>

#### assert\_numeric

```python
def assert_numeric(arg: str) -> None
```

Assert that the given argument is numeric.

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_gender"></a>

#### assert\_gender

```python
def assert_gender(gender: str) -> None
```

Assert that the given argument is either 'm' or 'f'.

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_first_digit"></a>

#### assert\_first\_digit

```python
def assert_first_digit(ssn: str) -> None
```

Assert that the first character of the given argument is between 1 and 8 (inclusive).

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_year_range"></a>

#### assert\_year\_range

```python
def assert_year_range(yyyy: int) -> None
```

Assert that the given argument is between 1800 and 2199 (inclusive).

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_existing_date"></a>

#### assert\_existing\_date

```python
def assert_existing_date(date: str) -> None
```

Assert that the given date exists (no February 29th on non-leap years, no April 31st, etc.).

**Arguments**:

- `date` _str_ - Date in ISO 8601 (YYYY-MM-DD).
  

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_constructor_list"></a>

#### assert\_constructor\_list

```python
def assert_constructor_list(ssns: List[str]) -> None
```

Sanity check called by SSN constructors.
Asserts that the given argument contains no duplicates and that every one of its elements is a valid Estonian SSN.

**Arguments**:

- `ssns` _List[str]_ - List of SSNs coming from Isikukood.construct().
  

**Raises**:

- `AssertionError` - When any of the assertions fail.

---
<a id="assertions.assert_valid_ssn"></a>

#### assert\_valid\_ssn

```python
def assert_valid_ssn(ssn: str) -> None
```

Assert that the given argument is a valid Estonian SSN. Currently, this performs the following checks:
* that the SSN is numeric
* that the first digit is between 1 and 8 (inclusive)
* that the SSN is exactly 11 digits
* that the checksum is correct
* that the birthdate exists
* that the year of birth is between 1800 and 2199 (inclusive)

**Raises**:

- `AssertionError` - When any of the assertions fail.

---
<a id="assertions.assert_correct_checksum"></a>

#### assert\_correct\_checksum

```python
def assert_correct_checksum(ssn: str) -> None
```

Assert that the given SSN's checksum is correct.

**Raises**:

- `AssertionError` - When the assertion fails.

---
<a id="assertions.assert_enum_arguments"></a>

#### assert\_enum\_arguments

```python
def assert_enum_arguments(genders: List[str], days: List[int],
                          months: List[int], years: List[int]) -> None
```

Assert that the arguments for functions.enum() are valid. This performs the following checks:
* that every element in genders is either 'm' or 'f'
* that every element in days is between 1 and 31 (inclusive)
* that every element in months is between 1 and 12 (inclusive)
* that every element in years is between 1800 and 2199 (inclusive)

**Raises**:

- `AssertionError` - When any of the assertions fail.

