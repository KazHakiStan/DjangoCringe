from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from friends_app.models import Friendship


def friendship(request, action, pk):
    new_friend = get_object_or_404(User, pk=pk)

    # Добавление в друзья(Возможно нужна проверка если ли уже в базе ???)
    if action == 'add':
        Friendship.objects.get_or_create(sender=request.user, receiver=new_friend)

    # Принимаем заявку в друзья
    elif action == 'accepted':
        friend = Friendship.objects.filter(Q(sender=pk) & Q(receiver=request.user.pk) & Q(wait_answer=True))[0]
        # проверка чтобы не сломать бд
        if friend:
            friend.wait_answer = False
            friend.is_accepted = True
            friend.save()
            return redirect('profile')

    # Отклоняем заявку в друзья
    elif action == 'reject':
        friend = Friendship.objects.filter(Q(sender=pk) & Q(receiver=request.user.pk) & Q(wait_answer=True))[0]

        # проверка чтобы не сломать бд
        if friend:
            friend.wait_answer = False
            friend.save()
            return redirect('profile')

    # Удаление из друзей
    elif action == 'remove':
        friend = Friendship.objects.filter((Q(sender=pk) & Q(receiver=request.user.pk)) |
                                           (Q(sender=request.user.pk) & Q(receiver=pk)) & Q(is_accepted=True))[0]

        # Без удаления не придумал как проще
        # Проверка, чтобы не сломать бд
        if friend:
            friend.sender = new_friend
            friend.receiver = request.user
            friend.is_accepted = False
            friend.is_sub = True
            friend.save()

    # Подписка на пользователя
    elif action == 'sub':
        Friendship.objects.get_or_create(sender=request.user, receiver=new_friend, wait_answer=False)

    # Отписка от пользователя, следовательно, удаление из базы
    elif action == 'unsub':
        friend = Friendship.objects.filter(Q(sender=request.user.pk) & Q(receiver=pk) & Q(is_accepted=False))
        friend.delete()

    return redirect(f'/profile/{pk}')