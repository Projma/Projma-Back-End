# Projma-Backend
Backend repository of Projma project.

## Run api on your localhost
python 3.9 and postgres must be installed befor running api

1- create python virtual environment 
```
python -m venv env
```
2- clone the project
3- get .env file from repo owner and put this file in ProjmaBackend folder(the folder that contains settings.py)
4- activate virtual env
5- cd to Base Folder(the folder that contains manage.py file)
6- install requirements
```
pip install -r requirements.txt
```
7- setup database
```
python manage.py makemigrations
python manage.py migrate
```
8- create superuser for admin panel
```
python manage.py createsuperuser
```
9- run api
```
python manage.py runserver
```
now project is running :)
you can read api document at:
```
http://127.0.0.1:8000/swagger/
```
and access models and database with the superuser you created before at:
```
http://127.0.0.1:8000/admin/
```

shokhosh.