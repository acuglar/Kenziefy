from django.urls import path
from .views import SampleView, ParamView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<str:name>/', ParamView.as_view()),
    # path('<route>/<id:pk>/', _View.as_view())  > comumente id:pk
    # terminar com '/' como padrão de construção de rotas
]
