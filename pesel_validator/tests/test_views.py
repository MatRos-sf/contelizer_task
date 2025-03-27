from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from pesel_validator.forms import PeselForm
from pesel_validator.pesel import Pesel


class PeselViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("pesel")

    def test_check_valid_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pesel_validator/pesel.html")

    def test_check_context_data_when_enter_to_the_page(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context["form"], PeselForm)
        self.assertIsNone(response.context.get("message"))
        self.assertIsNone(response.context.get("info"))

    def test_check_set_context_when_form_is_valid(self):
        form_data = {"pesel": "25240196478"}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pesel_validator/pesel.html")
        self.assertEqual(response.context.get("message"), "Pesel is valid")
        self.assertEqual(response.context.get("info"), Pesel("25240196478").get_info())

    def test_check_set_context_when_form_is_invalid(self):
        form_data = {"pesel": "25240113975"}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        form_error = response.context.get("form").errors
        self.assertEqual(form_error, {"pesel": ["The checksum is not valid"]})
