from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from friends_app.models import Friendship
from publication_app.forms.add_post import ImagePostForm
from publication_app.forms.editpost import EditPostForm
from publication_app.models import Post, ImagePost
from tags_app.models import Tag
from comments_app.forms.add_comment import AddCommentsForm


class Posts(View):

    @staticmethod
    def get(request):
        # Запрос на получение всех твоих друзей и кого ты подписан
        friendship = Friendship.objects.filter(Q(sender=request.user.pk) |
                                               (Q(receiver=request.user.pk) & Q(is_accepted=True)))

        # Объявляем пустой список для id друзей\фоловеров
        users = []

        for friend in friendship:

            if friend.sender.pk not in users:
                users.append(friend.sender.pk)

            if friend.receiver.pk not in users:
                users.append(friend.receiver.pk)

        # Если у тебя друзья или фолловеры:
        if friendship:
            tags = Tag.objects.all()
            posts = Post.objects.filter(is_public=True).filter(user__in=users)

            # Проверка на наличие постов у "друзей"
            if posts:

                paginator = Paginator(posts, 3)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                context = {
                    'title': "Посты",
                    'name_text': 'Публикации друзей и фолловеров',
                    'posts': posts,
                    'tag': tags,
                    'information': None,
                    'page_obj': page_obj
                }

            # Если посты отсутствуют
            else:
                context = {
                    'title': "Посты",
                    'information': 'У вашей друзей/фолловеров нет постов. '
                                   'Найдите новых пользователей, которые вам интересны'
                }

        else:
            context = {
                'title': "Посты",
                'information': 'Вы еще никого не добавили в друзья/фолловеры. '
                               'Найдите пользователей, которые вам интересны'
            }

        return render(request, 'publication_app/news.html', context)


class AddPost(View):
    """View добавление постов"""
    @staticmethod
    def get(request):
        form = ImagePostForm()

        context = {
            'title': 'Добавление нового поста',
            'form': form
        }

        return render(request, 'publication_app/add_post.html', context)

    @staticmethod
    def post(request):

        form = ImagePostForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('image')

        if form.is_valid():
            tags = form.cleaned_data.get('tag')
            post_obj = Post.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                is_public=form.cleaned_data['is_public'],
            )

            for file in files:
                ImagePost.objects.create(
                    post=post_obj,
                    image=file
                )

            for tag in tags:
                post_obj.tag.add(tag)

            return redirect('posts')

        else:
            context = {
                'title': 'Добавление нового поста',
                'form': form
            }
            return render(request, 'publication_app/add_post.html', context)


class EditImagePost(View):
    """View редактирование постов"""
    # Функция формы модели (Возвращает класс FormSet для модели ImagePost)
    ImageFormSet = modelformset_factory(ImagePost, fields={"image", })

    def get(self, request, pk):

        get_post = Post.objects.get(pk=pk)

        # параметр 'instance' берет все данные поста, если в бд есть
        post_form = EditPostForm(instance=get_post)
        image_form = self.ImageFormSet(queryset=ImagePost.objects.filter(post=get_post))

        context = {
            "title": "Добавить пост",
            "form": post_form,
            "image": image_form
        }
        return render(request, 'publication_app/post_red.html', context)

    def post(self, request, pk):
        get_post = Post.objects.get(pk=pk)
        get_image = ImagePost.objects.filter(post=get_post)

        post_form = EditPostForm(data=request.POST, instance=get_post)
        form_image = self.ImageFormSet(request.POST or None, request.FILES or None)

        if post_form.is_valid() and form_image.is_valid():
            post_form.save()
            # enumerate дает нам i(индекс) и file(его значение)
            for i, file in enumerate(form_image):
                # Проверяем, добавил ли пользователь изображение
                if file.cleaned_data:

                    if file.cleaned_data["id"] is None:
                        ImagePost(post=get_post, image=file.cleaned_data.get('image')).save()
                    elif file.cleaned_data["image"] is False:
                        ImagePost.objects.get(id=request.POST.get(f'form-{i}-id')).delete()
                    else:
                        image = ImagePost(post=get_post, image=file.cleaned_data.get('image'))
                        obj_img = ImagePost.objects.get(id=get_image[i].id)
                        obj_img.image = image.image
                        obj_img.save()
            return redirect('posts')


def post_delete(request, pk):
    Post.objects.get(id=pk).delete()
    return redirect('posts')


class ReadPostView(View):
    """
      View чтение поста и добавление комментария
    """
    @staticmethod
    def get(request, pk):
        posts = Post.objects.get(pk=pk)
        form = AddCommentsForm()

        context = {
            'title': 'Пост',
            'name_text': 'Публикации',
            'posts': posts,
            'form': form,
        }
        return render(request, 'publication_app/post.html', context)

    @staticmethod
    def post(request, pk):
        # Записывает id пользователя и поста в перменную
        new_request = request.POST.copy()
        new_request['user'] = request.user.pk
        new_request['post'] = pk

        # Сохраняем
        form = AddCommentsForm(data=new_request)
        if form.is_valid:
            form.save()
            return redirect(f'/post/{pk}')


class Tags(View):
    @staticmethod
    def get(request):
        count_tag = Tag.objects.annotate(cnt=Count('tag_post')).order_by('-cnt')

        context = {
            'title': 'Область тегов',
            'tags': count_tag,
        }
        return render(request, 'publication_app/tags.html', context)


class GetTag(View):

    @staticmethod
    def get(request, tag):

        our_tag = Tag.objects.filter(tag=tag)
        id_tag = None
        name_tag = None
        for i in our_tag:
            id_tag = i.pk
            name_tag = i.tag

        posts = Post.objects.filter(tag__id=id_tag)

        tags = Tag.objects.all()

        paginator = Paginator(posts, 3)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {
            'title': 'Посты по тегам',
            'name_text': f'Публикации по тегу "{name_tag}"',
            'page_obj': page_obj,
            'tags': tags,
            'name_tag': name_tag,
        }
        return render(request, 'publication_app/news.html', context)