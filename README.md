# NewsPaper
HomeWork 

Газета (wip)
Этот проект использует фреймворк Django для создания веб-портала, на котором пользователи могут читать и отправлять новости и статьи, комментировать и оценивать их. Пользователь может подписаться на категорию и получать электронные письма, когда в эту категорию добавляются розы. Они также еженедельно получают электронное письмо со всеми новыми публикациями в категории, на которую они подписаны.
Регистрация, аутентификация и авторизация реализованы с помощью библиотеки django-allauth.
Рассылка подписчикам по электронной почте и планирование работы реализованы с помощью задач celery. Кроме того, сигналы django и задания планировщика настраиваются и комментируются в качестве альтернативы.
Эта работа находится в стадии разработки.

NewsPaper (wip)
This project uses Django framework to create a web-portal where users can read and submit news and articles, comment and rate them. A user can subscribe to a category and receive emails when posts are added to this category. They also receive a weekly email with all the new posts in the category they subscribed to.
Signup, authentication and authorization implemented with django-allauth library.
Subscriber emailing and scheduling implemented with celery tasks. Also, django signals and apscheduler jobs set up and commented out as an alternative.
This is a work in progress.
