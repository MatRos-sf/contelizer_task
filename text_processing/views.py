import os
from http import HTTPStatus
from pathlib import Path
from typing import Union

import magic
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.edit import FormView

from .forms import TextProcessingForm
from .text_tools import RegexPatterns, process_file


class TextProcessingFormView(FormView):
    template_name = "text_processing/text_processing.html"
    form_class = TextProcessingForm

    def is_text_file(self, file_path: Union[str, Path]) -> bool:
        """
        Checks if file is text.
        Note: I use comparing mime type with "text/plain". It's only basic idea,
        and may not work for all files.
        """

        return magic.from_file(file_path, mime=True) == "text/plain"

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Handles POST request.
        Checks:
            - file was uploaded
            - file is text
        """

        file = form.cleaned_data.get("file")

        if not file:
            messages.error(self.request, "File must be uploaded.")
            return redirect("text_processing", status_code=HTTPStatus.BAD_REQUEST)

        # save file to tmp folder
        fs = FileSystemStorage(location=settings.UPLOAD_TEMP_FOLDER)
        file_path = settings.UPLOAD_TEMP_FOLDER / fs.save(file.name, file)

        if not self.is_text_file(file_path):
            fs.delete(file_path)
            messages.error(self.request, "File must be text.")
            return redirect("text_processing", status_code=HTTPStatus.BAD_REQUEST)

        return redirect("results", filename=file_path.name)


class ResultsView(View):
    def get(self, request, filename) -> HttpResponse:
        file_path: Path = settings.UPLOAD_TEMP_FOLDER / filename
        if not os.path.isfile(file_path):
            raise Http404("...")

        content = process_file(file_path, RegexPatterns.MIX_POLISH_ENGLISH.value)
        # remove file after processing
        os.remove(file_path)

        return render(
            request,
            "text_processing/results.html",
            {"content": content},
            status=HTTPStatus.OK,
        )
