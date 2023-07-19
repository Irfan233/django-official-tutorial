from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/newChoice/", views.newChoice, name="newChoice"),
    path("<int:question_id>/reset/", views.reset, name="reset"),
    path("newQues/", views.newQues, name="newQues"),
    path("newQues/", views.newQues, name="newQues"),
    path("editQues<int:id>/", views.editQues, name='editQues'),
    path("deleteQues<int:id>/", views.deleteQues, name='deleteQues'),
]
