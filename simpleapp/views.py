from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category
from .tasks import send_mail_for_sub_once


# импортируем наш кэш


# logger = logging.getLogger(name)
# logger.debug()
# logger.info()
# logger.warning()
# logger.error()
# logger.critical()
# Например, для регистрации сообщения с ошибкой, можно выполнить такой вызов:
# logger.error("Hello! I'm error in your app. Enjoy:)")
# Используя символ точки, можно создавать отношения наследования между логгерами.
# Например, запись:
# logger = logging.getLogger('project.app.some_name')
# Например, обработчик логгера project может также обрабатывать сообщения к project.app и project.some_name.


# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # код, выполняемый до формирования ответа (или другого middleware)
#
#         response = self.get_response(request)
#
#         # код, выполняемый после формирования запроса (или нижнего слоя)
#
#         return response


# class MobileOrFullMiddleware: # Шаблоны для этих версий хранятся в каталогах full/ и mobile/.
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.mobile:
#             prefix = "mobile/"
#         else:
#             prefix = "full/"
#         response.template_name = prefix + response.template_name
#         return response


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # news = objects_list по умолчанию
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'  # <p>Рейтинг - {{ new.rating }}</p> или {object.rating}

    # queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'new-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)

        return obj


# до кэширования PostDetail
# class PostDetail(DetailView):
#     model = Post
#     template_name = 'new.html'
#     context_object_name = 'new'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для добавления объекта
class PostAdd(CreateView):  # PermissionRequiredMixin
    model = Post
    template_name = 'add.html'
    context_object_name = 'add'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


# дженерик для редактирования объекта
class PostUpdateView(UpdateView):  # (PermissionRequiredMixin) чтобы регистрироваться
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
    # который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):  # PermissionRequiredMixin
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news/'
    permission_required = ('news.delete_post',)


def get_object(self, **kwargs):
    id = self.kwargs.get('pk')
    return Post.objects.get(pk=id)


@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'protected_page.html'


@login_required
def add_subscribe(request, pk):  # ++ (request,**kwargs)
    # +- pk = request.GET.get('pk', ) # -+ pk = kwargs.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, pk):
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')


def send_mail_for_sub(instance):
    print('Представления - начало')
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    sub_text = instance.text

    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    print('Адреса рассылки:')
    for pos in subscribers:
        print(pos.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        print('**********************', subscriber.email, '**********************')
        print(subscriber)
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})

        sub_username = subscriber.username
        sub_useremail = subscriber.email

        print()
        print(html_content)
        print()

        send_mail_for_sub_once.delay(sub_username, sub_useremail, html_content)

    print('Представления - конец')

    return redirect('/news/')
