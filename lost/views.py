from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import LostAnimal
from .forms import LostAnimalForm

# Create your views here.


class LostAnimalListView(ListView):  # список всех животных в списке потеряшек
    model = LostAnimal
    template_name = 'lost/lost_list.html'


class LostAnimalCreateView(LoginRequiredMixin, CreateView):  # добавление нового животного в список потеряшек
    permission_denied_message = 'Для доступа к этой странице необходимо авторизоваться на сайте'
    login_url = '/login/'
    redirect_field_name = 'redirected_to'

    model = LostAnimal
    template_name = 'lost/lost_create.html'
    form_class = LostAnimalForm

    def form_valid(self, form):
        animal = form.save()
        animal.author = self.request.user
        animal.save()
        return redirect(self.model.get_absolute_url(animal))


class LostAnimalDetailView(DetailView):  # страница конкретного объявления по первичному ключу
    model = LostAnimal
    template_name = 'lost/lost_detail.html'
    context_object_name = 'animal'


class LostAnimalUpdateView(UpdateView):  # редактирование конкретной модели потерянного животного
    model = LostAnimal
    template_name = 'lost/lost_edit.html'
    form_class = LostAnimalForm


def lost_animal_delete(request, pk):
    animal = LostAnimal.objects.get(id=pk)
    animal.delete()
    return HttpResponseRedirect('/lost_list/')
