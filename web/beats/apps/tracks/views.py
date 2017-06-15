from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class IndexView(View):
    """ An index view"""
    template_name = "base.html"

    def get(self, request):
        """ GET to return a simple template """
        return render(
            request, self.template_name
        )
