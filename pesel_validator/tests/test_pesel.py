from datetime import datetime

from django.test import TestCase
from parameterized import parameterized

from pesel_validator.pesel import Gender, Pesel


class PeselTest(TestCase):
    @parameterized.expand([("02212026896"), (91101358455)])
    def test_valid_pesel(self, pesel):
        pesel = Pesel(pesel)
        self.assertTrue(pesel)

    @parameterized.expand(["75020688844", "71100459784"])
    def test_pesel_belong_to_female(self, pesel):
        pesel = Pesel(pesel)
        self.assertEqual(pesel.gender, Gender.FEMALE)

    @parameterized.expand(["91042832816", "88061668797"])
    def test_pesel_belong_to_male(self, pesel):
        pesel = Pesel(pesel)
        self.assertEqual(pesel.gender, Gender.MALE)

    @parameterized.expand(
        [("00010155558", 1900, 1), ("99123189877", 1999, 12), ("53061121395", 1953, 6)]
    )
    def test_pesel_is_from_1900_1999(self, pesel, expected_year, expected_month):
        pesel = Pesel(pesel)
        self.assertEqual(pesel.date_of_birth.year, expected_year)
        self.assertEqual(pesel.date_of_birth.month, expected_month)

    @parameterized.expand(
        [("00210162769", 2000, 1), ("99323122281", 2099, 12), ("53252429251", 2053, 5)]
    )
    def test_pesel_is_from_2000_2099(self, pesel, expected_year, expected_month):
        pesel = Pesel(pesel)
        self.assertEqual(pesel.date_of_birth.year, expected_year)
        self.assertEqual(pesel.date_of_birth.month, expected_month)

    @parameterized.expand(
        [
            ("00410195712", 2100, 1),
        ]
    )
    def test_pesel_is_from_2100_2199(self, pesel, expected_year, expected_month):
        pesel = Pesel(pesel)
        self.assertEqual(pesel.date_of_birth.year, expected_year)
        self.assertEqual(pesel.date_of_birth.month, expected_month)

    # TODO: Write test using generate class

    @parameterized.expand(["", "1", "1" * 10])
    def test_pesel_is_short(self, pesel):
        with self.assertRaises(ValueError) as error_message:
            Pesel(pesel)

        self.assertEqual("Pesel must be 11 digits", str(error_message.exception))

    @parameterized.expand(["a" * 11, "1234567890" + "a"])
    def test_pesel_contains_non_digits(self, pesel):
        with self.assertRaises(ValueError) as error_message:
            Pesel(pesel)

        self.assertEqual("Pesel must be digits", str(error_message.exception))

    # TODO: invalid date of birth

    def test_checksum_is_invalid(self):
        pesel_str = "61080353331"
        with self.assertRaises(ValueError) as error_message:
            Pesel(pesel_str)

        self.assertEqual("The checksum is not valid", str(error_message.exception))

    def test_should_extract_correct_payload(self):
        pesel_str = "25240113976"
        expected_date_of_birth = datetime(2025, 4, 1).strftime("%d/%m/%Y")
        expected_gender = Gender.MALE.value
        pesel = Pesel(pesel_str)
        payload = pesel.get_info()
        self.assertEqual(payload.get("pesel"), pesel_str)
        self.assertEqual(payload.get("date_of_birth"), expected_date_of_birth)
        self.assertEqual(payload.get("gender"), expected_gender)
