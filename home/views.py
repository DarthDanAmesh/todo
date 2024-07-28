from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import Mzalendo
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from .forms import MzalendoForm
from django.core.paginator import Paginator

# in future add required mixin for logins to access the details materials
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import modelform_factory


class IndexView(TemplateView):
    template_name = 'index.html'
    


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect("mzalendo:login")
    else:
        form = CustomUserCreationForm()
    
    for field in form.fields.values():
        field.help_text = ""
    return render(
        request, "registration/register.html", {"form": form}
    )

# fix the index.html to be a list view


def mzalendo_list_view(request):
    mzalendo_list = Mzalendo.objects.all()
    paginator = Paginator(mzalendo_list, 10)  # Show 10 mzalendos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mzalendo/mzalendo_list.html', {'page_obj': page_obj, 'mzalendo': mzalendo_list})



def mzalendo_create_view(request):
    form = MzalendoForm()
    if request.method == "POST":
        form = MzalendoForm(request.POST, request.FILES)
        if form.is_valid():
            mzalendo = form.save(commit=False)
            wazalendo = Mzalendo.objects.all()
            context = {'mzalendo_list': wazalendo}
            mzalendo.save()
            return render(request, 'mzalendo/mzalendo_detail.html', context)
        else:
            form = MzalendoForm(request.POST, request.FILES or None)
            messages.success(request, 'Did not create post successfully')
            context = {'form': form}
    form = MzalendoForm()
    context = {'form': form}
    return render(request, 'mzalendo/create_mzalendo.html', context)

class MzalendoDetailView(DetailView):
    model = Mzalendo
    template_name = 'mzalendo/mzalendo_detail.html'
    context_object_name = 'mzalendo'



@require_http_methods(["GET", "POST"])
def quick_edit(request, pk):
    book = get_object_or_404(Mzalendo, pk=pk)
    if request.method == "POST":
        mzalendo.name = request.POST.get("name", "").strip()
        mzalendo.county = request.POST.get("county", "").strip()
        mzalendo.age = request.POST.get("age", "").strip()
        mzalendo.gender = request.POST.get("gender", "").strip()
        mzalendo.life = request.POST.get("life", "").strip()
        mzalendo.dod = request.POST.get("dod", "").strip()
        mzalendo.cover = request.POST.get("cover", "").strip()
        mzalendo.save()
        return render(request, "partials/mzalendo.html", {"mzalendo": mzalendo})
    return render(request, "partials/edit.html", {"mzalendo": mzalendo})


class PostDelete(DeleteView):
    model = Mzalendo
    template_name = 'mzalendo/delete_mzalendo.html'
    context_object_name = 'mzalendo'
    success_url = reverse_lazy("mzalendo:mzalendo_list")


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    context = {
        'pk': comment.pk
    }
    if request.method == 'POST':
        if request.user == comment.user:
            time.sleep(0.3)
            comment.delete()
            return render(request, 'mzalendo/delete_mzalendo.html', context)
        return HttpResponseForbidden('Not Allowed')

    return HttpResponseNotAllowed( ['POST'], 'Not Allowed')