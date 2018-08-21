# Django 2 factor Auth

A custom implementation of django two factor authentication that asks first time users
to provide their email addresses and allows login and authentication using google authenticator app found https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en


### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
django 1.11.15
django-two-factor-auth
```

### Installing

1) Install django

```
pip install django
```

2) Clone the project folder

```
git clone https://github.com/mwangistan/Django-Auth
```

2) Install django-two-factor-auth

```
pip install django-two-factor-auth
```


## Running the program on your local machine

1) To run the program makemigrations first

```
python manage.py makemigrations
```

2) Migrate the data

```
python manage.py migrate
```

3) Run the server

```
python manage.py runserver
```


## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django Two Factor Authentication](https://django-two-factor-auth.readthedocs.io/en/stable/index.html)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

