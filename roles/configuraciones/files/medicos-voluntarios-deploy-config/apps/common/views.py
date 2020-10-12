from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class MenuView(LoginRequiredMixin, TemplateView):
    template_name = "menu.html"

    def geta_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfiles = self.request.perfiles
        context.update({"perfiles": perfiles})
        return context


class LandingView(TemplateView):
    template_name = "landing.html"


class SuccessView(TemplateView):
    template_name = "success.html"
