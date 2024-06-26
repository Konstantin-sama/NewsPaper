from email.headerregistry import Group

from allauth.account.forms import SignupForm
from django.forms import ModelForm, BooleanField

from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='text')  # или же true-false поле

    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categoryType', 'check_box']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        # ДОБЫВИТЬ ПРИВЕДСТВЕННОЕ ПИСЬМО ТУТ
        return user
