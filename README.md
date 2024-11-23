# ew-django
experiments with Django

[[back-end]] [[python]]

## create

[Getting started | Django documentation | Django](https://docs.djangoproject.com/en/4.2/intro/).
it is not clear and understandable for me. we should use a lot of links to find correct commands.

-
```shell
mkdir ew-django && cd !$
python3 -m venv .venv
source ./.venv/bin/activate
pip install django
django-admin startproject base .
./manage.py migrate
./manage.py createsuperuser --username admin --email ""
./manage.py runserver
```
### alternative (poetry)
-
```shell
mkdir ew-django && cd !$
poetry init
```
-
(optional) make virtual environment files in project directory:
```shell
cat <<EOT > ./poetry.toml
[virtualenvs]
create = true
in-project = true
path = ".venv"
EOT
```
alternative:
```shell
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true
poetry config virtualenvs.path ".venv"
```
-
```shell
poetry shell
poetry add django
django-admin startproject base .
./manage.py migrate
./manage.py createsuperuser --username admin --email ""
./manage.py runserver
```
## run (dev)

```shell
./manage.py runserver
```
## api

[Home - Django REST framework](https://www.django-rest-framework.org/).
[Quickstart - Django REST framework](https://www.django-rest-framework.org/tutorial/quickstart/).

[drf-spectacular — drf-spectacular documentation](https://drf-spectacular.readthedocs.io/en/latest/index.html)

-
```shell
cat <<EOT > ./requirements.txt
django
djangorestframework
drf-spectacular
gunicorn
EOT
pip install -r ./requirements.txt
```
-
add to `./src/base/settings.py`:
```python
# ...

# Web API

INSTALLED_APPS += [
    'drf_spectacular',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API Title',
    'DESCRIPTION': 'Project API Description',
    'VERSION': '0.0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    # TODO: add other settings
}
```
-
add to `./src/base/urls.py`:
```python
# ...

# Web API

from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # necessary to add login link to drf view

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```
-
```shell
./manage.py migrate
```
### crud example

[Quickstart - Django REST framework](https://www.django-rest-framework.org/tutorial/quickstart/).

-
```shell
./manage.py startapp some_app
```
-
`./src/some_app/models.py`:
```python
from django.contrib.auth.models import User
from django.db import models


class SomeEntity(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user}"
```
-
`./src/some_app/serializers.py`:
```python
from rest_framework import serializers

from some_app.models import SomeEntity


class SomeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeEntity
        fields = "__all__"
```
-
`./src/some_app/views.py`:
```python
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from some_app.models import SomeEntity
from some_app.serializers import SomeEntitySerializer


class SomeEntityViewSet(viewsets.ModelViewSet):
    queryset = SomeEntity.objects.all()
    serializer_class = SomeEntitySerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="some_parameter",
                description="some description",
                required=True,
                type=str,
            ),
        ],
        responses={200: SomeEntitySerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="some-action")
    def some_action(self, request):
        some_parameter = request.query_params.get("some_parameter")

        if not some_parameter:
            return Response({"error": "some_parameter id required."}, status=400)

        try:
            some_intity_s = self.queryset.filter(
                # ...
            )
            serializer = self.get_serializer(some_intity_s, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "some eror."}, status=400)
```
-
add to `./src/base/urls.py`:
```python
# ...

# Some App

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from some_app.views import SomeEntityViewSet

router = DefaultRouter()
router.register(r'some_entity', SomeEntityViewSet, basename='some_entity')

urlpatterns += [
    path('api/', include(router.urls)),
]
```
-
add to `./src/base/settings.py`:
```python
# ...

# Some App

INSTALLED_APPS += [
    'some_app',
]
```
-
```shell
./manage.py makemigrations
./manage.py migrate
```
## security

- Clear and essential information to understand. Security of web pages and data is a frequent topic of discussion and a common question in interviews. It's also one of the key requirements for clients and users.
	- (eng) [Authentication - Django REST framework](https://www.django-rest-framework.org/api-guide/authentication/)
	- (rus) [Аутентификация - Django REST Framework](https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/authentication).
- [Getting started — Simple JWT 5.2.2.post30+gfaf92e8 documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html).
- [Getting started — Django OAuth Toolkit 2.3.0 documentation](https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html).

The following information is not actual and will be changed.

-
```shell
poetry add djangorestframework-simplejwt
```
-
```python
INSTALLED_APPS = [
    # ...
    'rest_framework_simplejwt.token_blacklist'
	]

# ...

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ],
    # ...
}


SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```
-
```python
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # necessary to add login link to drf view

    path('api/ping/', views.ping),
    path('api/ping-secure/', views.ping_secure, name='api-ping-secure'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

```
## docker layer
-
add to `./src/base/settings.py`:
```python
# ...

# Deploy layer

STATIC_ROOT = BASE_DIR / 'static'

```
-
```sh
./manage.py collectstatic
```
-
`./Dockerfile`:
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "base.wsgi:application"]
```
-
`./.dockerignore`:
```.dockerignore
# Exclude Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Exclude local environment files
*.env
*.env.*

# Exclude virtual environments
.venv/
venv/
env/
*.egg-info/

# Exclude static and media files (collected or uploaded outside the container)
static/
media/

# Exclude logs and temporary files
*.log
*.bak
*.swp
*.tmp
*.pid

# Exclude Docker-related files
Dockerfile
docker-compose.yml

# Exclude Git and version control files
.git/
.gitignore

# Exclude IDE and editor config files
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Exclude build artifacts
build/
dist/
*.egg
*.tar.gz
*.zip

```
-
`./nginx.conf`:
```conf
server {
    listen 80;

    location / {
        proxy_pass http://django-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /usr/share/nginx/html/static/;
    }
}
```
-
`./docker-compose.yml`:
```yml
version: '3.8'

services:
  django-app:
    build:
      context: .
    container_name: django-app
    volumes:
      - ./db.sqlite3:/app/db.sqlite3

  nginx:
    image: nginx:latest
    container_name: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./static:/usr/share/nginx/html/static:ro
    ports:
      - "80:80"
    depends_on:
      - django-app
```
## deploy

[How to deploy Django | Django documentation | Django](https://docs.djangoproject.com/en/4.2/howto/deployment/).

### gunicorn
```shell
pip install gunicorn
gunicorn base.wsgi
```
### daphne
```shell
pip install daphne
daphne base.wsgi:application
```
### hypercorn
```shell
pip install hypercorn
hypercorn base.wsgi:application
```
### uvicorn
```shell
pip install uvicorn
uvicorn bsae.wsgi:application
```
- [ ] there is an error. should find solution.
### gunicorn + uvicorn
```shell
pip install gunicorn uvicorn
gunicorn base.asgi:application -k uvicorn.workers.UvicornWorker
```
###
[Deployment checklist | Django documentation | Django](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/). review settings, with security, performance, and operations in mind.
```shell
./manage.py check --deploy
```
## extensions, tools and other

- A useful tool for debugging Django applications. While I found it helpful at times, I’ve only used it a couple of times in practice.
	- [Django Debug Toolbar — Django Debug Toolbar 4.4.6 documentation](https://django-debug-toolbar.readthedocs.io/en/latest/index.html).
