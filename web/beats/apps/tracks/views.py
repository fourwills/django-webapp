from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    """ An index view"""
    template_name = "base.html"

    def get(self, request):
        """ GET to return a simple template """
        return render(
            request, self.template_name
        )
