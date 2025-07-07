from django.urls import path

from parserexample.parser import views

app_name = 'parser'

urlpatterns = [
    path('', views.ParserView.as_view(), name='parser'),
    path('list', views.ParserListView.as_view(), name='list'),
]