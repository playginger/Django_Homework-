DjangoHomework по теме DRF 


ДЗ 24.1 Вьюсеты и дженерики мы создали приложение users и сделали 3 модели (Пользователь, Курс, Урок)
Так же Описали CRUD для моделей курса и урока, но при этом для курса сделали через ViewSets, а для урока — через Generic-классы.

ДЗ 24.2 Добавил новую модель «Платежи» со следующими полями(пользователь, дата оплаты, оплаченный курс или урок, сумма оплаты, способ оплаты: наличные или перевод на счет.)
Записал в эту модель данные через инструмент фикстур или кастомную команду.
Для сериализатора модели курса реализовал поле вывода уроков.
Настроил фильтрацию для эндпоинтов вывода списка платежей с возможностями(менять порядок сортировки по дате оплаты, фильтровать по курсу или уроку, фильтровать по способу оплаты.)

ДЗ 25.1 Настроил в проекте использование JWT-авторизации и закройте каждый эндпоинт авторизацией.
Завел группу модераторов и опишите для нее права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые. Заложите функционал такой проверки в контроллеры.
Описал права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть и редактировать только свои курсы и уроки.

ДЗ 25.2 Для сохранения уроков и курсов реализовал дополнительную проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.
То есть ссылки на видео можно прикреплять в материалы, а ссылки на сторонние образовательные платформы или личные сайты нельзя.
Добавил модель подписки на обновления курса для пользователя.
Реализовал эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.
При этом при выборке данных по курсу пользователю необходимо присылать признак подписки текущего пользователя на курс. То есть давать информацию, подписан пользователь на обновления курса или нет.
Реализовал пагинацию для вывода всех уроков и курсов.
Написал тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.
Сохранил результат проверки покрытия тестами.

ДЗ 26.1 Подключил и настроил вывод документации для проекта.
Подключить возможность оплаты курсов через https://stripe.com/docs/api.

ДЗ 26.2 Настроил проект для работы с Celery. Также настроил celery-beat для выполнения последующих задач.
Добавил асинхронную рассылку писем пользователям об обновлении материалов курса.
С помощью celery-beat реализовал фоновую задачу, которая будет проверять пользователей по дате последнего входа по полю 
last_login и, если пользователь не заходил более месяца, блокировать его с помощью флага is_active .

ДЗ 27.1 Установил Docker.
Описал Dockerfile для запуска контейнера с проектом.

ДЗ 27.2 Описал файл docker-compose для запуска всех частей проекта единой командой.