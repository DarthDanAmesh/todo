from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
from .models import Mzalendo, Profile
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, FormView
from django.views import View
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .forms import MzalendoForm, UpdateAccountProfile, AccountProfileForm
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
# in future add required mixin for logins to access the details materials
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import modelform_factory
from django.contrib.auth import logout, login
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .tokens import account_activate_token

from django.urls import path
#from .views import MyLoginView, RegisterView


class IndexView(TemplateView):
    template_name = 'index.html'
    

class RegisterUser(FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('mzalendo:index')

    def form_valid(self, form):
        user = form.save()
        self.send_activation_email(user)
        messages.success(self.request, 'Account created successfully. Check your email for the activation link.')
        return super().form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = self.render_activation_email(user, current_site)
        
        email_sent = send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
        )
        
        if email_sent:
            print(f"Activation email sent successfully to {user.email}")
        else:
            print(f"Failed to send activation email to {user.email}")

    def render_activation_email(self, user, current_site):
        return render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activate_token.make_token(user),
        })


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activate_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            login(request=request, user=user)
            messages.add_message(request, messages.INFO, 'You are successfully activated your account')
            return redirect('mzalendo:index')
        else:
            return HttpResponse('The link is invalid sorry!')

# fix the index.html to be a list view


def mzalendo_list_view(request):
    mzalendo_list = Mzalendo.objects.all()
    paginator = Paginator(mzalendo_list, 6)  # Show 10 mzalendos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mzalendo/mzalendo_list.html', {'page_obj': page_obj, 'mzalendo': mzalendo_list})


@login_required
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


class MzalendoDetail(DetailView):
    model = Mzalendo
    template_name = 'mzalendo/mzalendo_detail.html'

# maybe not necessary because of the above DetailView
def mzalendo_detail_cpy(request, pk):
    mzalendo = get_object_or_404(Mzalendo, pk=pk)
    render(request, 'mzalendo/mzalendo_detail.html', {'mzalendo': mzalendo})


@method_decorator([login_required], name='dispatch')
class MzalendoEdit(UpdateView):
    model = Mzalendo
    fields = '__all__'
    template_name = 'partials/edit.html'
    success_url = reverse_lazy("mzalendo:mzalendo_list")

# i don't need this probably
def edit_post(request, id):
        mzalendo_post = get_object_or_404(Mzalendo, id=id)
        if request.method == 'GET':
            context = {'form': MzalendoForm(instance=mzalendo_post), 'id': id}
            return render(render, 'mzalendo/mzalendo_detail.html',context)
        elif request.method == 'POST':
            form = MzalendoForm(request.POST, instance=mzalendo_post)
            if form.is_valid():
                form.save()
                message.success(request, 'The post is updated!')
            else:
                message.error(request,'Correct errors found in the form!')
                return render(request, 'mzalendo/mzalendo_list.html',{'form':form})

# also I don't need this

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

@method_decorator([login_required], name='dispatch')
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

# to prevent the recursive limit error, don't use def logout(request) because it calls the logout from auth 
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

@method_decorator([login_required], name='dispatch')
class AccountProfile(View):
    def get(self, request):
        user_form_update= UpdateAccountProfile(instance=request.user)
        account_profile = AccountProfileForm(instance=request.user.profile)

        context = {'user_form_update':user_form_update,
        'account_profile':account_profile}

        return render(request, 'registration/profile.html', context)

    def post(self, request):
        user_form_update = UpdateAccountProfile(
            request.POST, instance=request.user)
        account_profile = AccountProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)
        
        if user_form_update.is_valid() and account_profile.is_valid():
            user_form_update.save()
            account_profile.save()

            messages.success(request, 'Profile has updated.')
            
            return redirect('mzalendo:index')
        else:
            context = {'user_form_update':user_form_update, 
            'account_profile':account_profile}

            messages.error(request, 'Profile update failed.')

            return render(request, 'registration/profile.html', context)

    
