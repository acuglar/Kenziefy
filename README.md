# Kenziefy 001_django_introduction

## Inicializando um projeto
```sh
python3 -m venv env
source env/bin/activate
pip install djangorestframework
# djangorestframework instala também django
# djangorestframework estende padrão rest para o django

django-admin startproject Kenziefy .  # w '.' cria outro dir

python manage.py runserver  # Starting development server
```
### estrutura de pastas e arquivos
```py
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        # https://docs.djangoproject.com/en/3.2/ref/settings/
        # SECRET_KEY -> autenticação e criptografia. Valor precisa ser protegido em prod
        # ALLOWED_HOST -> hosts permitidos. [] -> localhost

        urls.py
        asgi.py
        wsgi.py
        # wsgi e asgi quando outro servidor que não o próprio django. e.g.: gunicorn
```
## application definition
> djangoprojects.com/.../settings

Add 'rest_framework' to your INSTALLED_APPS setting.
```py 
INSTALLED_APPS = [  # ferramentas e apps necessitam ter o contexto declarado
    ...,
    'rest_framework'  # renderizar templates   
]
```
## Inicializando um app
```sh
python manage.py startapp <app>
# id. ./manage.py startapp <app>
```

## Criando rotas
1. definindo rota em \<app>.view
2. ref \<app>.urls
3. ref \<app>.urls \<poroject>.urls

127.0.0.1:8000/api/sample/  
GET  
{"message": "Hello Django"}  

POST  
{"message": "This is a POST method"}

### Rotas com parametros
e.g. \<route>/<str: name>/

## ipdb
```
ipdb> serializer
SampleSerializer(data={'name': 'João', 'teste': 'teste'}):
    name = CharField()
    age = IntegerField()
ipdb> serializer.data
{'name': 'João'}
ipdb> request.data
{'name': 'João', 'teste': 'teste'}
```