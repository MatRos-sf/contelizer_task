from tempfile import NamedTemporaryFile
from unittest.mock import patch

from django.test import TestCase

from text_processing.text_tools import RegexPatterns, process_file, shuffle_text


class ShuffleTextTest(TestCase):
    def test_should_return_shuffled_text_when_random_is_mocked(self):
        text = "This is a test!"
        expected_result = "Tihs is a tset!"
        with patch("random.shuffle", side_effect=lambda x: x.reverse()):
            result = shuffle_text(text, RegexPatterns.MIX_POLISH_ENGLISH.value)

        self.assertEqual(result, expected_result)


class ProcessFileTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create temp file with test content
        cls.temp_file = NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")

        cls.temp_file.write("This is a test!\n")
        cls.temp_file.write("Th-is is a t'est!\n")
        cls.temp_file.write("T12s is3 anothEr tęst!\n")

        cls.temp_file.close()

        cls.file_path = cls.temp_file.name

    @classmethod
    def tearDownClass(cls):
        import os

        os.remove(cls.file_path)
        super().tearDownClass()

    @patch("random.shuffle", side_effect=lambda x: x.reverse())
    def test_should_return_expected_text(self, mock_shuffle):
        expected_text = (
            "Tihs is a tset!\n" "Ti-hs is a tse't!\n" "T21s is3 aEhtonr tsęt!\n"
        )
        result = process_file(self.file_path, RegexPatterns.MIX_POLISH_ENGLISH.value)
        self.assertEqual(result, expected_text)
