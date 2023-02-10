from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from .models import Uzduotis
from .forms import UzduotisCreateUpdateForm, UzduotisApzvalgaForm


# Create your views here.

@login_required
def index(request):
    num_aktyvios = Uzduotis.objects.filter(vartotojas=request.user, vartotojas__is_active=True, status__exact='p').count()


    context = {
         "num_aktyvios": num_aktyvios,

     }
    return render(request, 'index.html', context=context)




@csrf_protect
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

class UzduotysList(ListView):
    model = Uzduotis
    context_object_name = 'uzduotys'
    template_name = 'uzduotys.html'



class UzduotisDetail(FormMixin, DetailView):

    model = Uzduotis
    context_object_name = 'uzduotis'
    template_name = 'uzduotis.html'
    form_class = UzduotisApzvalgaForm

    def get_success_url(self):
        return reverse('uzduotis', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VartotojoUzduotisList(LoginRequiredMixin, ListView):
    model = Uzduotis
    template_name = 'vartotojo_uzduotyss.html'
    context_object_name = "uzduotys"

    def get_queryset(self):
        return Uzduotis.objects.filter(vartotojas=self.request.user).order_by('-sukurta')

class VartotojoUzduotysList(LoginRequiredMixin, ListView):
    model = Uzduotis
    context_object_name = 'uzduotis'
    template_name = 'vartotojo_uzduotis.html'

    def get_queryset(self):
        return Uzduotis.objects.filter(vartotojas=self.request.user).order_by('-sukurta')

class VartotojoUzduotysDetail(LoginRequiredMixin, DetailView):
    model = Uzduotis
    template_name = 'vartotojo_uzduotis.html'

class UzduotisVartotojoCreate(LoginRequiredMixin, CreateView):
    model = Uzduotis
    success_url = "/todolist/vartotojouzduotys/"
    template_name = 'vartotojo_uzduotis_form.html'
    form_class = UzduotisCreateUpdateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.save()
        return super().form_valid(form)

class UzduotisVartotojoUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Uzduotis
    template_name = 'vartotojo_uzduotis_form.html'
    form_class = UzduotisCreateUpdateForm

    def get_success_url(self):
         return reverse("uzduotis", kwargs={"pk": self.object.id})

    def form_valid(self, form):
         form.instance.vartotojas = self.request.user
         return super().form_valid(form)

    def test_func(self):
        uzduotis = self.get_object()
        return self.request.user == uzduotis.vartotojas


class UzduotisVartotojoDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Uzduotis
    success_url = "/todolist/vartotojouzduotys/"
    template_name = 'vartotojo_uzduotis_trinti.html'
    context_object_name = 'uzduotis'


    def test_func(self):
        uzduotis = self.get_object()
        return self.request.user == uzduotis.vartotojas
