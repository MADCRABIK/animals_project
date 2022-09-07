from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Dialog, Message
from .forms import MessageForm

# Create your views here.


@login_required(login_url='login')
def dialog_list_view(request):
    dialogs = Dialog.objects.filter(members__in=[request.user.id])
    context = {'dialogs': dialogs}
    return render(request, 'chats/chats.html', context=context)


@login_required(login_url='login')
def dialog_detail_view(request, pk):
    dialog = Dialog.objects.get(pk=pk)
    form = MessageForm()
    context = {'dialog': dialog, 'form': form}

    match request.method:
        case 'POST':
            message = request.POST.get('message')
            from_user = request.user
            to_user = None
            for member in dialog.members.all():
                if member != request.user:
                    to_user = member

            Message.objects.create(dialog=dialog,
                                   from_user=from_user,
                                   to_user=to_user,
                                   message=message,
                                   )

            return redirect(reverse('chat_detail', kwargs={'pk': pk}))
        case _:
            if request.user in dialog.members.all():
                return render(request, 'chats/chat_detail.html', context=context)
            else:
                return redirect(reverse('home'))


@login_required(login_url='login')
def get_dialog(request, author_id):  # работает через жопу, надо переделать
    dialogs = Dialog.objects.filter(members__in=[request.user.id])
    dialog = None

    for chat in dialogs:
        members = list()
        expected_members = [request.user.id, author_id]
        for member in chat.members.all():
            members.append(member.id)
        expected_members.sort()
        members.sort()
        print(expected_members)
        print(members)
        print(expected_members == members)
        if expected_members == members:
            dialog = chat
            break

    if dialog is None:
        dialog = Dialog.objects.create()
        dialog.members.add(request.user.id)
        dialog.members.add(author_id)

    return redirect(reverse('chat_detail', kwargs={'pk': dialog.pk}))
