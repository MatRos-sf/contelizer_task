from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class TextProcessingFormViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("text_processing")

    # def tearDown(self) -> None:
    #     # delete temp file
    #     import os
    #     if hasattr(self, "temp_file"):
    #         os.remove(settings.UPLOAD_TEMP_FOLDER / self.temp_file)
    #         self.temp_file = None
    #     super().tearDown()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "text_processing/text_processing.html")

    def test_should_redirect_to_result_when_file_is_correct(self):
        file_content = b"Test valid"
        test_file = SimpleUploadedFile(
            "test.txt", file_content, content_type="text/plain"
        )
        self.temp_file = test_file.name
        response = self.client.post(self.url, {"file": test_file})
        self.assertRedirects(
            response, reverse("results", kwargs={"filename": "test.txt"})
        )

    # def test_should_show_error_message_when_file_is_not_text(self):
    #     file_content = b"\x00\x01\x02\x03"
    #     test_file = SimpleUploadedFile("test.mp3", file_content, content_type="audio/mpeg")
    #     self.temp_file = test_file.name
    #     response = self.client.post(self.url, {"file": test_file}, follow=True)
    #     print(response.context)
    #     # self.assertEqual(response.context["messages"][0].message, "File is not text")
