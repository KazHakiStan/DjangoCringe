from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View

from friends_app.models import Friendship
from profile_app.forms.edituserform import UserEditForm, ProfileEditForm
from profile_app.forms.loginform import LoginUserForm
# Create your views here.
from profile_app.forms.registerform import RegisterUserForm
from publication_app.models import Post
from tags_app.models import Tag



class UserLogin(LoginView):
    """Класс авторизации пользователей."""
    # Подключаем форму
    form_class = LoginUserForm

    # Указываем путь к template для авторизации
    template_name = 'profile_app/login.html'

    # Включаем переадресация для авторизированных пользователей
    redirect_authenticated_user = True

    # Если авторизированны, то куда будет переадресация
    next_page = reverse_lazy('posts')


class MainPage(View):
    """Класс главной страницы"""
    @staticmethod
    def get(request):
        posts = Post.objects.filter(is_public=True)
        tags = Tag.objects.all()

        context = {
            'title': "Cringe",
            'posts': posts,
            'tag': tags,
        }
        return render(request, 'profile_app/main_page.html', context)


class Register(View):
    """Класс регистрации пользователя"""
    @staticmethod
    def get(request):

        if request.user.is_authenticated:
            return redirect('posts')

        form = RegisterUserForm()

        context = {
            'title': 'Регистрация ',
            'form': form
        }
        return render(request, 'profile_app/register.html', context)

    @staticmethod
    def post(request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            context = {
                'user': user
            }
            return redirect('login')

        else:
            messages.error(request, 'Ошибка регистрации. Попробуйте снова')

            context = {
                'title': 'Регистрация ',
                'form': form
            }
            return render(request, 'profile_app/register.html', context)


class UserRedaction(View):
    """Класс редактирование пользователя """

    @staticmethod
    def get(request):
        # параметр 'instance' берет все данные пользователя, если в бд есть
        # Получаем информацию пользователя из модели user & profile
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        context = {
            'title': 'Редактирование профиля',
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(
            request,
            'profile_app/red_profile.html',
            context
        )

    @staticmethod
    def post(request):

        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')


def user_logout(request):
    """Функция выхода из аккаунта"""
    logout(request)
    return redirect('login')


class Profile(View):
    """Класс информации о 'своем' аккаунте"""
    @staticmethod
    def get(request):
        # Получаем посты пользователя
        post = Post.objects.filter(user=request.user.pk)

        # Получаем всех друзей
        friend = Friendship.objects.filter(Q(sender=request.user.pk) | Q(receiver=request.user.pk)).\
            filter(is_accepted=True)

        # Получаем всех подписчиков
        sub = Friendship.objects.filter(sender=request.user.pk, is_sub=True)

        # Получаем пользователей, которые нас добавили и ждут решение
        wait_answer = Friendship.objects.filter(receiver=request.user.pk, wait_answer=True)

        context = {
            'title': 'Информация о вашем аккаунте',
            'posts': post,
            'friends': friend,
            'subs': sub,
            'wait_answers': wait_answer,
        }

        return render(request, 'profile_app/profile.html', context)


class ProfileUserView(View):
    @staticmethod
    def get(request, pk):
        users = get_object_or_404(User, pk=pk)

        # Проверка, если перешел на свой аккаунт
        if users.pk == request.user.pk:
            return redirect('profile')

        friend = Friendship.objects.filter(Q(sender=pk) | Q(receiver=pk)).filter(is_accepted=True)
        sub = Friendship.objects.filter(sender=pk, is_sub=True)

        # Один запрос в базу с первым результатом
        is_friendship = Friendship.objects.filter((Q(sender=pk) & Q(receiver=request.user.pk)) |
                                                  (Q(sender=request.user.pk) & Q(receiver=pk)))

        is_friend = None
        is_subscribed = None
        is_follower = None

        # Если ли запись в бд
        if not is_friendship:
            "???"
            pass
        # Проверка на дружбу
        elif is_friendship.filter(is_accepted=True):
            is_friend = True
        # Проверка, что ты фолловер
        elif is_friendship.filter(Q(sender=request.user.pk) & Q(is_sub=True)):
            is_follower = True
        # Проверка, что на тебя подписаны
        elif is_friendship.filter(Q(receiver=request.user.pk) & Q(is_sub=True)):
            is_subscribed = True

        context = {
            'title': f'Профиль {users.username}',
            'users': users,
            'friends': friend,
            'subs': sub,
            'is_friend': is_friend,
            'is_subscribed': is_subscribed,
            'is_follower': is_follower,
        }
        return render(request, 'profile_app/profile_user.html', context)


class UserSearchListView(ListView):

    model = User
    queryset = User.objects.all()
    template_name = "profile_app/user_search.html"
    context_object_name = "search_list"

    def get_queryset(self):
        queryset = super(UserSearchListView, self).get_queryset()
        q = self.request.GET.get("q")

        if q:

            return queryset.filter(Q(username__startswith=q))
        return None
