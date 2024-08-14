# library
 Django-приложение для библиотеки, которое позволяет читателям выбрать интересующую книгу из каталога библиотеки, взять ее почитать, а потом вернуть.

### Запуск проекта
Для Windows:

```shell
git clone https://github.com/pasha-danilevich/library.git
python -m venv env
env/Scripts/activate
python -m pip install --upgrade pip
cd library/src
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Для корректной работы приложения необходимо:
 * создать super user
```shell
python manage.py createsuperuser
```
 * сгенерировать записи
```shell
python manage.py generate_data
```
Запустить сервер разработки
```shell
python manage.py runserver
```
Функционал:

1. Получение списка книг (название, автор, жанр)
   
```http://127.0.0.1:8000/api/books/```

2. Взять книгу

```http://127.0.0.1:8000/borrow/<int:book_id>/```

3. Вернуть книгу

```http://127.0.0.1:8000/return/<int:book_id>/```

4. Получить список книг на руках (название, дата, когда взял, количество дней, сколько книга на руках у должника)

```http://127.0.0.1:8000/my-books/```

5. Список должников

```http://127.0.0.1:8000/debtors-list/```

