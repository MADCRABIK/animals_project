from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# импорты для авторизации
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import LostAnimal
from .forms import LostAnimalForm


# Create your views here.


class LostAnimalListView(ListView):  # список всех животных в списке потеряшек
    model = LostAnimal
    template_name = 'lost/lost_list.html'
    queryset = model.objects.filter(moderated=True)


class LostAnimalCreateView(LoginRequiredMixin, CreateView):  # добавление нового животного в список потеряшек
    permission_denied_message = 'Для доступа к этой странице необходимо авторизоваться на сайте'
    login_url = '/login/'

    model = LostAnimal
    template_name = 'lost/lost_create.html'
    form_class = LostAnimalForm

    def form_valid(self, form):
        animal = form.save()
        animal.author = self.request.user

        # объявление не отправляется на модерацию, если его опубликовал superuser
        if self.request.user.is_superuser:
            animal.moderated = True

        animal.save()
        return HttpResponseRedirect(self.model.get_absolute_url(animal))


class LostAnimalDetailView(DetailView):  # страница конкретного объявления по первичному ключу
    model = LostAnimal
    template_name = 'lost/lost_detail.html'
    context_object_name = 'animal'

    def get_object(self, queryset=None):
        obj = super(LostAnimalDetailView, self).get_object(queryset)
        if obj.moderated:
            return obj
        else:
            raise Http404('Объявление не найдено')


# редактирование конкретной записи в модели
class LostAnimalUpdateView(LoginRequiredMixin, UpdateView):
    permission_denied_message = 'Для доступа к этой странице необходимо авторизоваться на сайте'
    login_url = '/login/'

    model = LostAnimal
    template_name = 'lost/lost_edit.html'
    form_class = LostAnimalForm

    def dispatch(self, request, *args, **kwargs):
        animal = self.get_object()
        if request.user == animal.author or request.user.is_superuser:
            return super(LostAnimalUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404('У Вас нет доступа к этой странице.')


def lost_animal_delete(request, pk):  # удаление конкретной записи в модели
    animal = LostAnimal.objects.get(id=pk)
    if request.user == animal.author or request.user.is_superuser:
        animal.delete()
        return HttpResponseRedirect('/lost/list/')
    else:
        raise Http404('У Вас нет доступа к этой странице.')