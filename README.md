To prepare the Backend-application:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
(follow the prompts in the terminal)

To start the application:
python manage.py runserver

To access django admin panel in the browser:
http://127.0.0.1:8000/admin/

To start the Frontend:
navigate to /frontend
right click on index.html
click "open with live server"

Info:
To get, create or delete an appointment you have to login first.

To run in-built tests:
python manage.py test
see the test coverage in /htmlcov