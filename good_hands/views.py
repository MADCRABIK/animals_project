from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404

# импорты для авторизации
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import AnimalToGoodHands
from .forms import AnimalToGoodHandsForm

# Create your views here.


class GoodHandsListView(ListView):  # список объявлений
    model = AnimalToGoodHands
    template_name = 'good_hands/good_hands_list.html'


class GoodHandsDetailView(DetailView):  # страница отдельного объявления
    model = AnimalToGoodHands
    template_name = 'good_hands/good_hands_detail.html'
    context_object_name = 'animal'


class GoodHandsCreateView(LoginRequiredMixin, CreateView):  # создание нового объявления
    permission_denied_message = 'Для доступа к этой странице необходимо авторизоваться на сайте'
    login_url = '/login/'

    form_class = AnimalToGoodHandsForm
    model = AnimalToGoodHands
    template_name = 'good_hands/good_hands_create.html'

    def form_valid(self, form):
        animal = form.save()
        animal.author = self.request.user
        animal.save()
        return redirect(self.model.get_absolute_url(animal))


class GoodHandsUpdateView(LoginRequiredMixin, UpdateView):  # редактирование объявления
    permission_denied_message = 'Для доступа к этой странице необходимо авторизоваться на сайте'
    login_url = '/login/'

    form_class = AnimalToGoodHandsForm
    model = AnimalToGoodHands
    template_name = 'good_hands/good_hands_edit.html'

    def dispatch(self, request, *args, **kwargs):
        animal = self.get_object()
        if request.user == animal.author or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


@login_required
def good_hands_delete(request, pk):  # удаление объявления
    animal = AnimalToGoodHands.objects.get(id=pk)

    if request.user == animal.author or request.user.is_superuser:
        animal.delete()
        return HttpResponseRedirect('/good_hands/list')
    else:
        raise Http404('У Вас нет доступа к этой странице')



