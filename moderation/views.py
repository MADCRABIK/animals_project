from django.shortcuts import render
from django.http import HttpResponseRedirect

from good_hands.models import AnimalToGoodHands
from lost.models import LostAnimal

from django.contrib.auth.decorators import user_passes_test

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)  # декоратор разрешает доступ только superuser'у
def to_moderate(request):
    lost_animals = LostAnimal.objects.filter(moderated=False)
    good_hands_animals = AnimalToGoodHands.objects.filter(moderated=False)

    context = {'lost_animals': lost_animals,
               'good_hands_animals': good_hands_animals}

    return render(request, 'moderation/moderate_list.html', context)


def publish_lost(request, pk):
    animal = LostAnimal.objects.get(id=pk)
    animal.moderated = True
    animal.save()

    return HttpResponseRedirect('/moderation/to_moderate')


def publish_good_hands(request, pk):
    animal = AnimalToGoodHands.objects.get(id=pk)
    animal.moderated = True
    animal.save()

    return HttpResponseRedirect('/moderation/to_moderate')


def reject_lost(request, pk):
    animal = LostAnimal.objects.get(id=pk)
    animal.delete()

    return HttpResponseRedirect('/moderation/to_moderate')


def reject_good_hands(request, pk):
    animal = AnimalToGoodHands.objects.get(id=pk)
    animal.delete()

    return HttpResponseRedirect('/moderation/to_moderate')
