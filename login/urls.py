from django.urls import path
from polls import views

app_name = 'login'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='result'),
    path('<int:question_id>/vote', views.vote, name='vote'),
]

