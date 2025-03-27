import random
from datetime import datetime
from enum import StrEnum
from typing import Dict, Optional


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


def generate_date_of_birth_in_pesel(date_of_birth):
    year = date_of_birth.year
    if year < 1800 or year > 2299:
        raise ValueError("Date of birth not valid. Year must be between 1800 and 2299.")

    year = date_of_birth.year
    month = date_of_birth.month
    if 1800 <= year <= 1899:
        month += 80
    elif 2000 <= year <= 2099:
        month += 20
    elif 2100 <= year <= 2199:
        month += 40
    elif 2200 <= year <= 2299:
        month += 60

    return f"{str(year)[2:4]}{str(month).zfill(2)}{str(date_of_birth.day).zfill(2)}"


def generate_ordinal_number(gender: Optional[Gender] = None) -> str:
    male_numbers = [str(i) for i in range(10) if i % 2 != 0]
    female_numbers = [str(i) for i in range(10) if i % 2 == 0]
    if not gender:
        last_number = random.choice(male_numbers + female_numbers)
    elif gender == Gender.MALE:
        last_number = random.choice(male_numbers)
    else:
        last_number = random.choice(female_numbers)
    numbers = list(map(str, range(10)))
    return "".join(random.choices(numbers, k=3)) + last_number


def find_control_number(numbers: str) -> str:
    a, b, c, d, e, f, g, h, i, j = map(int, numbers)
    checksum = (
        1 * a + 3 * b + 7 * c + 9 * d + 1 * e + 3 * f + 7 * g + 9 * h + 1 * i + 3 * j
    )
    k = 10 - (checksum % 10)
    return str(0) if k == 10 else str(k)


class Pesel:
    def __init__(self, pesel: str | int) -> None:
        self.pesel = str(pesel)
        self.check_basic_valid()
        self.set_date_of_birth()
        self.set_gender()
        self.check_checksum()

    def check_basic_valid(self) -> None:
        """
        Checks if the pesel contains 11 digits and all of them are digits.

        Note: I could have used a regular expression here, but I decided to separate the validation logic instead.
        """
        # if not re.match(r"^\d{11}$", self.pesel):
        if len(self.pesel) != 11:
            raise ValueError("Pesel must be 11 digits")
        elif not self.pesel.isdigit():
            raise ValueError("Pesel must be digits")

    def set_date_of_birth(self) -> None:
        """
        Sets the date of birth based on the first six digits of the pesel.
        """
        year = int(self.pesel[:2])
        month = int(self.pesel[2:4])
        day = int(self.pesel[4:6])
        # 1900 - 1999
        if 0 < month <= 12:
            self.date_of_birth = datetime(year + 1900, month, day)
        # 1800 - 1899
        elif 80 < month <= 92:
            self.date_of_birth = datetime(year + 1800, month - 80, day)
        # 2000 - 2099
        elif 20 < month <= 32:
            self.date_of_birth = datetime(year + 2000, month - 20, day)
        # 2100 - 2199
        elif 40 < month <= 52:
            self.date_of_birth = datetime(year + 2100, month - 40, day)
        # 2200 - 2299
        elif 60 < month <= 72:
            self.date_of_birth = datetime(year + 2200, month - 60, day)
        else:
            raise ValueError("Date of birth not valid")

    def set_gender(self) -> None:
        ordinal_number = int(self.pesel[-2])
        if ordinal_number % 2 == 0:
            self.gender = Gender.FEMALE
        else:
            self.gender = Gender.MALE

    def check_checksum(self) -> None:
        """
        Checks if the last number of checksum must be equal to 0
        Checksum formula: 1*a + 3*b + 7*c + 9*d + 1*e + 3*f + 7*g + 9*h + 1*i +3*j + 1*k
        """
        a, b, c, d, e, f, g, h, i, j, k = map(int, self.pesel)
        checksum = (
            1 * a
            + 3 * b
            + 7 * c
            + 9 * d
            + 1 * e
            + 3 * f
            + 7 * g
            + 9 * h
            + 1 * i
            + 3 * j
            + 1 * k
        )
        if str(checksum)[-1] != "0":
            raise ValueError("The checksum is not valid")

    def get_info(self) -> Dict[str, str]:
        return {
            "pesel": self.pesel,
            "date_of_birth": self.date_of_birth.strftime("%d/%m/%Y"),
            "gender": self.gender.value,
        }

    @classmethod
    def generate_pesel(
        cls,
        date_of_birth: Optional[datetime] = None,
        gender: Optional[Gender] = None,
    ) -> "Pesel":
        if not date_of_birth:
            year = random.choice(range(1800, 2300))
            month = random.choice(range(1, 13))
            day = random.choice(range(1, 28))
            date_of_birth = datetime(year, month, day)

        d = generate_date_of_birth_in_pesel(date_of_birth)
        p = generate_ordinal_number(gender)
        k = find_control_number(d + p)
        return cls(d + p + k)
