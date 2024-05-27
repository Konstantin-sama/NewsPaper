# from django.core.management.base import BaseCommand, CommandError
#
#
# class Command(BaseCommand):
#     help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
#     missing_args_message = 'Недостаточно аргументов'
#     requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
#
#     def add_arguments(self, parser):
#         # Positional arguments
#         parser.add_argument('argument', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         # здесь можете писать любой код, который выполняется при вызове вашей команды
#         self.stdout.write(str(options['argument']))

# команда в терминале
# python manage.py base_command 1 2 3 4


from django.core.management.base import BaseCommand

from simpleapp.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all news from category {category.name}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Could not find category"))

# no
