# Тестирование проекта Yatube
## _Описание_
1. **Тестирование Models: «Unittest в Django: тестирование моделей»**
2. **Тестирование URLs: «Unittest в Django: тестирование URLs»**
![This is an image](https://pictures.s3.yandex.net/resources/S05_01_1629250721.png)
3. **Проверка namespase:name и шаблонов: «Unittest в Django: тестирование Views»**
![This is an image](https://pictures.s3.yandex.net/resources/Untitled_2_1629250743.png)
4. **Тестирование контекста: «Unittest в Django: тестирование views»**
![This is an image](https://pictures.s3.yandex.net/resources/Untitled_3_1629250762.png)
5. **Дополнительная проверка при создании поста: «Unittest в Django: тестирование Views»**  
Проверяем, что если при создании поста указать группу, то этот пост появляется
- на главной странице сайта,
- на странице выбранной группы,
- в профайле пользователя.
Проверяем, что этот пост не попал в группу, для которой не был предназначен.

6. **Тестирование Forms: «Unittest в Django: тестирование Forms»**  
Тесты, которые проверяют, что
- при отправке валидной формы со страницы создания поста ***reverse('posts:create_post')*** создаётся новая запись в базе данных;
- при отправке валидной формы со страницы редактирования поста ***reverse('posts:post_edit', args=('post_id',))***  
происходит изменение поста с ***post_id*** в базе данных.

## Технологии
- Python 3.7.9
- Django 2.2.16
- Django Rest Framework 3.12.4
- Pytest 6.2.4

## Установка
1. **Клонируйте репозиторий:**
```sh
git clone https://github.com/Alexandra1624/hw04_tests.git
```

2. **Cоздать и активировать виртуальное окружение:**
```sh
python -m venv venv
source venv/Scripts/activate
```

3. **Обновить pip и установить зависимости из файла requirements.txt:**
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. **Выполнить миграции:**
```sh
cd yatube
python manage.py migrate
```

5. **Создать суперпользователя:**
```sh
python manage.py createsuperuser
```

6. **Проверка тестов Unittest:**
```sh
python manage.py test
```

7. **Запустить проект:**
```sh
python manage.py runserver
```
Сервер запущен на странице:     
http://localhost:8000       

 ## Автор

**_Александра Радионова_**  
https://github.com/Alexandra1624  
https://t.me/alexandra_R1624  
sashamain@yandex.ru
