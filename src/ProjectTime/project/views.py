from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@staff_member_required
def home(request):
    return HttpResponseRedirect(reverse('admin:index'))
