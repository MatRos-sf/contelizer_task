from http import HTTPStatus

from django.views.generic.edit import FormView

from .forms import PeselForm
from .pesel import Pesel


class PeselView(FormView):
    template_name = "pesel_validator/pesel.html"
    form_class = PeselForm

    def form_valid(self, form):
        pesel = Pesel(form.cleaned_data.get("pesel"))
        return self.render_to_response(
            self.get_context_data(
                form=form, message="Pesel is valid", info=pesel.get_info()
            )
        )

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form), status=HTTPStatus.BAD_REQUEST
        )
